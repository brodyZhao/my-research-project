#!/usr/bin/env python3
"""为 FF++ 补建 GT 区域恢复图与等面积大对照 —— 本次干净实验的阳性对照。

## 为什么需要

FakeVLM 在 FF++ 上说出的区域是"嘴巴"这种小块（面积中位数 **2.35%**），
而真实伪迹区域（差分图派生）覆盖**整张脸**（该样本 **24.7%**）——大 10 倍。

若把 GT 恢复的效应与"按 claimed 匹配的小对照"相比，两者面积差 10 倍，阳性对照不干净。
所以必须给 GT 单独配等面积对照。

## 本脚本产出

    restore_gt        真实伪迹区域替换为 pristine 内容（逐像素，零生成伪影）
    control_gt_1..3   与 GT 等面积、不与 GT 重叠的对照区域，同样恢复

## ⚠️ 一个必须知道的性质（它不是缺陷，是内部一致性检查）

FF++ 是换脸：**pristine 与 forged 只在人脸区域内不同，背景逐像素相同**。
因此落在背景里的对照区域，恢复后图像与 original **完全相同** → Δs 应精确为 0。

如果实测 Δs(control_gt) ≠ 0，说明算子或打分出了问题，而不是模型行为。
这条写进协议作为强制检查项。

（同理，GT 区域几乎覆盖整张脸时，restore_gt 会接近 whole（原图本身），
  故 Δs(gt) 预期接近 Δs(whole)——两个阳性对照应当互相印证。）
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path

import numpy as np
from PIL import Image

SCRIPTS_DIR = Path(__file__).resolve().parent


def _load_sibling(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_build = _load_sibling("06_build_restorations")
_rr = _load_sibling("07_resynthesize")

find_project_root = _build.find_project_root
load_mask = _build.load_mask
dilate_mask = _build.dilate_mask
equal_area_rect = _rr.equal_area_rect
mask_to_box = _build.mask_to_box


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


def restore(forged: np.ndarray, pristine: np.ndarray, mask: np.ndarray) -> np.ndarray:
    result = forged.copy()
    result[mask] = pristine[mask]
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Build GT-region restorations for FF++")
    parser.add_argument("--restorations", required=True, help="06 的输出 restorations.jsonl")
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--num-controls", type=int, default=3)
    parser.add_argument("--seed", type=int, default=20260921)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    source_root = Path(args.source_root)

    def resolve(value: str) -> Path:
        path = Path(value)
        return path if path.is_absolute() else source_root / path

    rows = [row for row in read_jsonl(resolve(args.restorations)) if not row.get("error")]
    if args.limit is not None:
        rows = rows[: args.limit]

    out_dir = Path(args.out_dir)
    image_dir = out_dir / "images"
    mask_dir = out_dir / "masks"
    image_dir.mkdir(parents=True, exist_ok=True)
    mask_dir.mkdir(parents=True, exist_ok=True)

    records = []
    for index, row in enumerate(rows, 1):
        sample_id = row["sample_id"]
        gt_value = row.get("gt_mask_path")
        if not gt_value:
            records.append({"sample_id": sample_id, "error": "no_gt_mask_path"})
            continue

        variants = row.get("variant_paths") or {}
        forged_path = variants.get("original")
        pristine_path = variants.get("whole")
        if not forged_path or not pristine_path:
            records.append({"sample_id": sample_id, "error": "missing_original_or_whole"})
            continue

        forged_image = Image.open(resolve(forged_path)).convert("RGB")
        pristine_image = Image.open(resolve(pristine_path)).convert("RGB")
        forged = np.asarray(forged_image)
        pristine = np.asarray(pristine_image)
        if forged.shape != pristine.shape:
            records.append({"sample_id": sample_id, "error": "size_mismatch"})
            continue

        gt = load_mask(resolve(gt_value), forged_image.size)

        paths: dict[str, str] = {}
        Image.fromarray(restore(forged, pristine, gt)).save(
            image_dir / f"{sample_id}__restore_gt.png"
        )
        Image.fromarray((gt.astype(np.uint8) * 255), mode="L").save(
            mask_dir / f"{sample_id}__gt.png"
        )
        paths["restore_gt"] = str(image_dir / f"{sample_id}__restore_gt.png")

        # 与 GT 等面积、不重叠的对照。FF++ 里这些多半落在背景 → 恢复后与原图逐像素相同
        rng = np.random.default_rng(args.seed)
        forbidden = dilate_mask(gt, max(1, round(min(forged_image.size) * 0.02)))
        control_areas = []
        for control_index in range(1, args.num_controls + 1):
            control = equal_area_rect(gt, forbidden, rng)
            if control is None:
                break
            control_areas.append(float(control.mean()))
            Image.fromarray(restore(forged, pristine, control)).save(
                image_dir / f"{sample_id}__restore_gtcontrol_{control_index}.png"
            )
            Image.fromarray((control.astype(np.uint8) * 255), mode="L").save(
                mask_dir / f"{sample_id}__gtcontrol_{control_index}.png"
            )
            paths[f"restore_gtcontrol_{control_index}"] = (
                str(image_dir / f"{sample_id}__restore_gtcontrol_{control_index}.png")
            )
            forbidden = np.logical_or(forbidden, control)

        records.append(
            {
                "sample_id": sample_id,
                "dataset": row.get("dataset"),
                "method": row.get("method"),
                "variant_paths": paths,
                "gt_area_ratio": float(gt.mean()),
                "gt_control_areas": control_areas,
                "gt_control_area_delta": (
                    float(abs(float(gt.mean()) - float(np.mean(control_areas))))
                    if control_areas
                    else None
                ),
                "error": None if control_areas else "no_gt_control",
            }
        )
        if index % 25 == 0:
            print(json.dumps({"done": index, "total": len(rows)}), flush=True)

    output = out_dir / "gt_restorations.jsonl"
    with output.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    valid = [r for r in records if not r.get("error")]
    deltas = [r["gt_control_area_delta"] for r in valid if r["gt_control_area_delta"] is not None]
    summary = {
        "n": len(records),
        "n_valid": len(valid),
        "num_controls": args.num_controls,
        "gt_area_ratio_median": float(np.median([r["gt_area_ratio"] for r in valid])) if valid else None,
        "mean_gt_control_area_delta": float(np.mean(deltas)) if deltas else None,
        "note": (
            "FF++ 的 pristine 与 forged 只在人脸区域内不同；落在背景的对照恢复后应与 "
            "original 逐像素相同，故 Δs(gtcontrol) 预期精确为 0 —— 这是强制的一致性检查项"
        ),
        "output": str(output),
    }
    (out_dir / "gt_restorations_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
