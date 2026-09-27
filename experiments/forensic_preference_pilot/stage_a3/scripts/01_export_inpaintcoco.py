#!/usr/bin/env python3
"""把 InpaintCOCO 的 parquet 分片导出为图片文件 + 统一 pair manifest。

数据契约（2026-09-21 实测确认，勿凭记忆改动）：
  parquet 字段 coco_image / inpaint_image / mask 均为 struct{bytes, path}
  三张图都是 512x512 RGB
  mask 三通道恒等（退化为灰度），取值以 {0,255} 为主，含少量抗锯齿灰边
  → M_gt 的推导规则固定为：mask.max(axis=2) > 127

同时计算配对质量指标（edition3 §A3.1），供 03_validate_pairs.py 复用：
  mean_abs_diff_inside_gt / mean_abs_diff_outside_gt / pair_quality_ratio

输出布局（相对 --out-root）：
  images/<sample_id>__pristine.png
  images/<sample_id>__forged.png
  masks/<sample_id>__gt.png          单通道 0/255
  metadata/pairs_inpaintcoco.jsonl
  metadata/export_summary.json
"""

from __future__ import annotations

import argparse
import io
import json
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq
from PIL import Image


# 与 edition3 的推导规则绑定；改这里等于改数据契约，必须同步改文档
MASK_THRESHOLD = 127


def decode(entry: dict) -> np.ndarray:
    """parquet 的 struct{bytes,path} -> RGB uint8 数组。"""
    image = Image.open(io.BytesIO(entry["bytes"]))
    return np.asarray(image.convert("RGB"))


def mask_from_rgb(mask_rgb: np.ndarray) -> np.ndarray:
    """RGB 三通道恒等的 mask -> 单通道 bool。"""
    return mask_rgb.max(axis=2) > MASK_THRESHOLD


def pair_quality(pristine: np.ndarray, forged: np.ndarray, mask: np.ndarray) -> dict:
    """edition3 §A3.1：inside 应远大于 outside。"""
    difference = np.abs(
        pristine.astype(np.int16) - forged.astype(np.int16)
    ).mean(axis=2)
    inside = float(difference[mask].mean()) if mask.any() else float("nan")
    outside = float(difference[~mask].mean()) if (~mask).any() else float("nan")
    return {
        "mean_abs_diff_inside_gt": inside,
        "mean_abs_diff_outside_gt": outside,
        "pair_quality_ratio": inside / (outside + 1e-6),
    }


def rel_to_source(path: Path, source_root: Path) -> str:
    """manifest 内路径统一相对项目根，便于任何在项目根启动的脚本直接解析。

    与 SynthScars 流水线的既有约定一致（形如 data/... 的相对路径）。
    若 out-root 不在 source-root 之下，退回绝对路径并保持可用。
    """
    try:
        return str(path.relative_to(source_root))
    except ValueError:
        return str(path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Export InpaintCOCO parquet shards to images + pair manifest")
    parser.add_argument("--parquet-dir", required=True, help="含 test-0000*-of-00003.parquet 的目录")
    parser.add_argument("--out-root", required=True)
    parser.add_argument("--source-root", required=True, help="manifest 里路径的解析根（通常是远端项目根）")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument(
        "--shard-glob",
        default="test-0000*-of-00003.parquet",
        help="分片文件名模式；默认按 InpaintCOCO 官方命名",
    )
    args = parser.parse_args()

    parquet_dir = Path(args.parquet_dir)
    shards = sorted(parquet_dir.glob(args.shard_glob))
    if not shards:
        raise FileNotFoundError(f"未在 {parquet_dir} 找到匹配 {args.shard_glob} 的分片")

    out_root = Path(args.out_root)
    source_root = Path(args.source_root)
    image_dir = out_root / "images"
    mask_dir = out_root / "masks"
    metadata_dir = out_root / "metadata"
    for directory in (image_dir, mask_dir, metadata_dir):
        directory.mkdir(parents=True, exist_ok=True)

    records: list[dict] = []
    index = 0
    for shard in shards:
        parquet_file = pq.ParquetFile(shard)
        for batch in parquet_file.iter_batches(batch_size=16):
            for row in batch.to_pylist():
                if args.limit is not None and index >= args.limit:
                    break
                sample_id = f"inpaintcoco_test_{index:05d}"
                pristine = decode(row["coco_image"])
                forged = decode(row["inpaint_image"])
                mask = mask_from_rgb(decode(row["mask"]))

                # 逐样本质量问题记录为剔除原因，不中断整批导出。
                # 一个退化 mask 不应该杀掉其余 1259 个样本。
                reasons: list[str] = []
                if pristine.shape != forged.shape:
                    reasons.append(f"size_mismatch:{pristine.shape}vs{forged.shape}")
                if mask.shape != pristine.shape[:2]:
                    reasons.append(f"mask_size_mismatch:{mask.shape}")
                if not mask.any():
                    reasons.append("degenerate_mask:all_zero")
                elif mask.all():
                    reasons.append("degenerate_mask:all_one")

                record: dict = {
                    "sample_id": sample_id,
                    "dataset": "InpaintCOCO",
                    "split": "test",
                    "source_root_relative": True,
                    "label": 1,  # 1 = fake（与 SynthScars 流水线一致）
                    "source_image_id": row.get("coco_details", {}).get("id"),
                    "manipulation_type": "diffusion_inpainting",
                    "generator": "stable-diffusion-2-inpainting",
                    "concept": row.get("concept"),
                    "coco_caption": row.get("coco_caption"),
                    "inpaint_caption": row.get("inpaint_caption"),
                    "guidance_scale": row.get("inpaint_details", {}).get("guidance_scale"),
                    "num_inference_steps": row.get("inpaint_details", {}).get("num_inference_steps"),
                    "coco_url": row.get("coco_details", {}).get("coco_url"),
                }

                if reasons:
                    record.update(
                        {
                            "pristine_path": None,
                            "forged_path": None,
                            "gt_mask_path": None,
                            "claimed_mask_path": None,
                            "mask_area_ratio": None,
                            "mean_abs_diff_inside_gt": None,
                            "mean_abs_diff_outside_gt": None,
                            "pair_quality_ratio": None,
                        }
                    )
                else:
                    pristine_rel = Path("images") / f"{sample_id}__pristine.png"
                    forged_rel = Path("images") / f"{sample_id}__forged.png"
                    gt_rel = Path("masks") / f"{sample_id}__gt.png"
                    Image.fromarray(pristine).save(out_root / pristine_rel)
                    Image.fromarray(forged).save(out_root / forged_rel)
                    Image.fromarray((mask.astype(np.uint8) * 255), mode="L").save(out_root / gt_rel)
                    # 注意：必须经 rel_to_source 转成相对项目根的路径。
                    # 直接写 str(pristine_rel) 会得到 "images/..."（相对 out-root），
                    # 下游按项目根解析就会全部 file_not_found —— 已踩过这个坑。
                    record.update(
                        {
                            "pristine_path": rel_to_source(out_root / pristine_rel, source_root),
                            "forged_path": rel_to_source(out_root / forged_rel, source_root),
                            "gt_mask_path": rel_to_source(out_root / gt_rel, source_root),
                            "claimed_mask_path": None,  # 由 04/05 步骤回填
                            "mask_area_ratio": float(mask.mean()),
                        }
                    )
                    record.update(pair_quality(pristine, forged, mask))

                record["exclusion_reasons"] = reasons
                record["eligible"] = not reasons
                records.append(record)

                index += 1
                if index % 50 == 0:
                    print(json.dumps({"exported": index, "sample_id": sample_id}), flush=True)
            if args.limit is not None and index >= args.limit:
                break
        if args.limit is not None and index >= args.limit:
            break

    manifest_path = metadata_dir / "pairs_inpaintcoco.jsonl"
    with manifest_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    valid = [r for r in records if r["eligible"]]
    ratios = np.asarray([r["pair_quality_ratio"] for r in valid], dtype=float)
    areas = np.asarray([r["mask_area_ratio"] for r in valid], dtype=float)
    reason_counts: dict[str, int] = {}
    for record in records:
        for reason in record["exclusion_reasons"]:
            reason_counts[reason.split(":")[0]] = reason_counts.get(reason.split(":")[0], 0) + 1
    summary = {
        "dataset": "InpaintCOCO",
        "n": len(records),
        "n_eligible": len(valid),
        "n_excluded": len(records) - len(valid),
        "exclusion_reason_counts": reason_counts,
        "shards": [str(s.name) for s in shards],
        "mask_threshold": MASK_THRESHOLD,
        "source_root": str(source_root),
        "pair_quality_ratio": {
            "min": float(ratios.min()),
            "median": float(np.median(ratios)),
            "max": float(ratios.max()),
            "below_2": int((ratios < 2).sum()),
        },
        "mask_area_ratio": {
            "min": float(areas.min()),
            "median": float(np.median(areas)),
            "max": float(areas.max()),
        },
        "manifest": str(manifest_path),
    }
    (metadata_dir / "export_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
