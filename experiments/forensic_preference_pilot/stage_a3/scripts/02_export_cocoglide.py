#!/usr/bin/env python3
"""把 CocoGlide 导出为图片文件 + 统一 pair manifest（与 01_export_inpaintcoco.py 同格式）。

数据契约（2026-09-21 实测确认，勿凭记忆改动）：
  extracted/{real,fake,mask}/  +  table.csv
  table.csv 列名：real, fake, mask, prompt（utf-8-sig，带 BOM）

  ⚠️ 三个目录的文件基名并不一致，必须用 table.csv 配对：
       real/dining table_114871.png
       fake/glide_inpainting_val2017_114871_up.png
       mask/dining table_114871_mask.png
     按基名匹配会直接 FileNotFoundError（已踩过）。

  全部 256x256；mask 为单通道 'L'，二值，> 127 判正。
  mask 外与 pristine 逐像素一致（GLIDE 是真合成图，区域外原样复制，
  不像 SD2 会把整图过一遍 VAE）→ pair_quality_ratio 中位数 210.9，
  恢复后与 pristine 逐像素相同，恢复过程零伪影。

输出布局（相对 --out-root）：
  images/<sample_id>__pristine.png
  images/<sample_id>__forged.png
  masks/<sample_id>__gt.png          单通道 0/255
  metadata/pairs_cocoglide.jsonl
  metadata/export_summary.json
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

import numpy as np
from PIL import Image

# 预先注册的准入条件（edition3 §A3.1）。改这里等于改协议，必须同步改文档。
MASK_THRESHOLD = 127
AREA_MIN = 0.02
AREA_MAX = 0.30

COCO_ID_PATTERN = re.compile(r"val2017_(\d+)")


def rel_to_source(path: Path, source_root: Path) -> str:
    """manifest 内路径统一相对项目根，与 SynthScars 流水线约定一致。"""
    try:
        return str(path.relative_to(source_root))
    except ValueError:
        return str(path)


def pair_quality(pristine: np.ndarray, forged: np.ndarray, mask: np.ndarray) -> dict:
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Export CocoGlide to images + pair manifest")
    parser.add_argument("--extracted-dir", required=True, help="含 real/ fake/ mask/ table.csv 的目录")
    parser.add_argument("--out-root", required=True)
    parser.add_argument("--source-root", required=True, help="manifest 路径的解析根（通常是远端项目根）")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    extracted = Path(args.extracted_dir)
    table_path = extracted / "table.csv"
    if not table_path.is_file():
        raise FileNotFoundError(f"缺少配对表: {table_path}")

    with table_path.open(newline="", encoding="utf-8-sig") as handle:
        table = list(csv.DictReader(handle))
    if not table:
        raise ValueError("table.csv 为空")
    if args.limit is not None:
        table = table[: args.limit]

    out_root = Path(args.out_root)
    source_root = Path(args.source_root)
    image_dir = out_root / "images"
    mask_dir = out_root / "masks"
    metadata_dir = out_root / "metadata"
    for directory in (image_dir, mask_dir, metadata_dir):
        directory.mkdir(parents=True, exist_ok=True)

    records: list[dict] = []
    for index, row in enumerate(table):
        sample_id = f"cocoglide_{index:04d}"
        pristine_path = extracted / row["real"]
        forged_path = extracted / row["fake"]
        mask_path = extracted / row["mask"]
        for path, label in (
            (pristine_path, "pristine"),
            (forged_path, "forged"),
            (mask_path, "mask"),
        ):
            if not path.is_file():
                raise FileNotFoundError(f"{sample_id} 缺少 {label}: {path}")

        pristine = np.asarray(Image.open(pristine_path).convert("RGB"))
        forged = np.asarray(Image.open(forged_path).convert("RGB"))
        mask = np.asarray(Image.open(mask_path).convert("L")) > MASK_THRESHOLD

        if pristine.shape != forged.shape:
            raise ValueError(f"{sample_id} 尺寸不一致: {pristine.shape} vs {forged.shape}")
        if mask.shape != pristine.shape[:2]:
            raise ValueError(f"{sample_id} mask 尺寸 {mask.shape} 与图像 {pristine.shape[:2]} 不一致")
        if not mask.any() or mask.all():
            raise ValueError(f"{sample_id} mask 退化（全 0 或全 1）")

        pristine_rel = Path("images") / f"{sample_id}__pristine.png"
        forged_rel = Path("images") / f"{sample_id}__forged.png"
        gt_rel = Path("masks") / f"{sample_id}__gt.png"
        Image.fromarray(pristine).save(out_root / pristine_rel)
        Image.fromarray(forged).save(out_root / forged_rel)
        Image.fromarray((mask.astype(np.uint8) * 255), mode="L").save(out_root / gt_rel)

        area = float(mask.mean())
        coco_match = COCO_ID_PATTERN.search(row["fake"])
        record = {
            "sample_id": sample_id,
            "dataset": "CocoGlide",
            "split": "test",
            "pristine_path": rel_to_source(out_root / pristine_rel, source_root),
            "forged_path": rel_to_source(out_root / forged_rel, source_root),
            "gt_mask_path": rel_to_source(out_root / gt_rel, source_root),
            "claimed_mask_path": None,  # 由 04/05 步骤回填
            "label": 1,  # 1 = fake
            "source_image_id": int(coco_match.group(1)) if coco_match else None,
            "manipulation_type": "diffusion_inpainting",
            "generator": "glide",
            "concept": row.get("prompt"),
            "mask_area_ratio": area,
            "area_eligible": bool(AREA_MIN <= area <= AREA_MAX),
        }
        record.update(pair_quality(pristine, forged, mask))
        records.append(record)

        if (index + 1) % 50 == 0:
            print(json.dumps({"exported": index + 1, "sample_id": sample_id}), flush=True)

    manifest_path = metadata_dir / "pairs_cocoglide.jsonl"
    with manifest_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    ratios = np.asarray([r["pair_quality_ratio"] for r in records], dtype=float)
    areas = np.asarray([r["mask_area_ratio"] for r in records], dtype=float)
    eligible = np.asarray([r["area_eligible"] for r in records], dtype=bool)
    summary = {
        "dataset": "CocoGlide",
        "n": len(records),
        "mask_threshold": MASK_THRESHOLD,
        "pre_registered_area_band": [AREA_MIN, AREA_MAX],
        "area_eligible_count": int(eligible.sum()),
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
