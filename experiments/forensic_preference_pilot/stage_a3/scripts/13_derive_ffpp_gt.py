#!/usr/bin/env python3
"""为 FakeClue-FF++ 派生 GT 掩码（原图 vs 篡改图的差分图）。

为什么需要：FakeClue 不提供 mask，而 `IoU(claimed, GT)` 和 `x_restore_gt` 都要用 GT。
FF++ 的 real/fake 帧是像素对齐的，所以差分图直接定位了被改动区域，可作代理 GT。

⚠️ 循环性警告（必须随结果一起报告，不得隐去）：
   掩码由差分图派生，所以"掩码内差异 >> 掩码外差异"这条 pair_quality 指标
   对本数据集的派生掩码是**恒真的、无信息量的**。因此本脚本
   不输出 pair_quality_ratio 作为质量证据，改为输出：
     - diff_threshold（所用阈值）
     - mask_area_ratio
     - 保留的连通域数量与最大连通域占比
     - 覆盖率（diff > 阈值的像素中，有多少落进最终掩码）
   并保存 overlay 供人工盲审。

输出（相对 --out-dir）：
  masks/<sample_id>__gt.png        派生掩码（单通道 0/255）
  overlays/<sample_id>.jpg         原图 + 掩码轮廓，供盲审
  ffpp_gt.jsonl                    每样本的派生元数据
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

MASK_THRESHOLD = 127


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_number} 不是 JSON 对象")
            rows.append(value)
    return rows


def derive_mask(
    pristine: np.ndarray,
    forged: np.ndarray,
    diff_threshold: float,
    min_component_ratio: float,
    keep_largest_only: bool,
) -> tuple[np.ndarray, dict]:
    difference = np.abs(pristine.astype(np.int16) - forged.astype(np.int16)).max(axis=2)
    raw = difference > diff_threshold

    labeled, count = ndimage.label(raw)
    if count == 0:
        return np.zeros(raw.shape, dtype=bool), {
            "n_components": 0,
            "kept_components": 0,
            "largest_component_ratio": 0.0,
            "coverage_of_raw": 0.0,
        }

    sizes = ndimage.sum(raw, labeled, index=np.arange(1, count + 1))
    order = np.argsort(-sizes)
    largest_ratio = float(sizes[order[0]] / raw.sum()) if raw.sum() else 0.0

    kept = np.zeros(raw.shape, dtype=bool)
    kept_components = 0
    for rank, component_index in enumerate(order, 1):
        size = sizes[component_index]
        if keep_largest_only and rank > 1:
            break
        if size / raw.size < min_component_ratio and rank > 1:
            continue
        kept |= labeled == (component_index + 1)
        kept_components += 1

    if not kept.any():
        kept = labeled == (order[0] + 1)
        kept_components = 1

    kept = ndimage.binary_fill_holes(kept)
    return kept, {
        "n_components": int(count),
        "kept_components": int(kept_components),
        "largest_component_ratio": largest_ratio,
        "coverage_of_raw": float(kept[raw].mean()) if raw.any() else 0.0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Derive GT masks for FF++ pairs from difference maps")
    parser.add_argument("--manifest", required=True, help="pairs_ffpp.jsonl")
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--diff-threshold", type=float, default=25.0)
    parser.add_argument("--min-component-ratio", type=float, default=0.002)
    parser.add_argument("--keep-largest-only", action="store_true", default=False)
    parser.add_argument("--save-overlays", action="store_true", default=True)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    source_root = Path(args.source_root)
    out_dir = Path(args.out_dir)
    mask_dir = out_dir / "masks"
    overlay_dir = out_dir / "overlays"
    mask_dir.mkdir(parents=True, exist_ok=True)
    if args.save_overlays:
        overlay_dir.mkdir(parents=True, exist_ok=True)

    rows = read_jsonl(Path(args.manifest))
    if args.limit is not None:
        rows = rows[: args.limit]

    records = []
    for index, row in enumerate(rows, 1):
        sample_id = row["sample_id"]
        pristine_path = Path(row["pristine_path"])
        forged_path = Path(row["forged_path"])
        if not pristine_path.is_absolute():
            pristine_path = source_root / pristine_path
        if not forged_path.is_absolute():
            forged_path = source_root / forged_path

        pristine_image = Image.open(pristine_path).convert("RGB")
        forged_image = Image.open(forged_path).convert("RGB")
        if pristine_image.size != forged_image.size:
            records.append({"sample_id": sample_id, "error": "size_mismatch"})
            continue

        pristine = np.asarray(pristine_image)
        forged = np.asarray(forged_image)
        mask, stats = derive_mask(
            pristine, forged, args.diff_threshold,
            args.min_component_ratio, args.keep_largest_only,
        )

        mask_path = mask_dir / f"{sample_id}__gt.png"
        Image.fromarray((mask.astype(np.uint8) * 255), mode="L").save(mask_path)

        if args.save_overlays:
            overlay = forged.copy()
            edge = ndimage.binary_dilation(mask, iterations=2) & ~mask
            overlay[edge] = (255, 0, 0)
            Image.fromarray(overlay).save(overlay_dir / f"{sample_id}.jpg", quality=88)

        record = {
            "sample_id": sample_id,
            "dataset": row.get("dataset"),
            "split": row.get("split"),
            "method": row.get("method"),
            "gt_mask_path": str(mask_path),
            "gt_mask_source": "derived_from_diff",
            "diff_threshold": args.diff_threshold,
            "mask_area_ratio": float(mask.mean()),
            "error": None,
        }
        record.update(stats)
        records.append(record)

        if index % 500 == 0:
            print(json.dumps({"done": index, "total": len(rows)}), flush=True)

    output = out_dir / "ffpp_gt.jsonl"
    with output.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    valid = [r for r in records if not r.get("error")]
    areas = np.asarray([r["mask_area_ratio"] for r in valid]) if valid else np.asarray([0.0])
    summary = {
        "n": len(records),
        "n_valid": len(valid),
        "diff_threshold": args.diff_threshold,
        "mask_area_ratio": {
            "min": float(areas.min()),
            "median": float(np.median(areas)),
            "max": float(areas.max()),
        },
        "area_band_0.02_0.30": int(((areas >= 0.02) & (areas <= 0.30)).sum()),
        "kept_components_median": float(np.median([r["kept_components"] for r in valid])) if valid else None,
        "coverage_of_raw_median": float(np.median([r["coverage_of_raw"] for r in valid])) if valid else None,
        "caveat": (
            "掩码由差分图派生，故 mask 内外的差异对比对本掩码无信息量。"
            "gt_mask_source=derived_from_diff，涉及 GT 的结论只能作次要结果报告。"
        ),
        "output": str(output),
    }
    (out_dir / "ffpp_gt_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
