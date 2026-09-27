#!/usr/bin/env python3
"""合并 CocoGlide 与 InpaintCOCO 的 pair manifest，施加预先注册的准入条件，生成分析用清单。

准入条件（edition3 §A3.1，预先注册，不得事后调整）：
  1. 0.02 <= mask_area_ratio <= 0.30
     —— 面积 >0.30 时"恢复 GT 区域"近似"整图替换"，A3.5 的局部/全图对照退化
  2. pair_quality_ratio >= --min-pair-quality-ratio
     —— 配对不严格则恢复无意义（CocoGlide 中位数 210.9；InpaintCOCO 中位数 10.3）
  3. 三元组文件存在且尺寸自洽

claimed 区域的面积准入（claimed_area_ratio <= 0.30，edition3 §A3.2c）在此阶段
无法判定，因为 claimed 区域要等 05 步落地之后才有。该条由 03 之后的步骤施加。

划分：按 source_image 分组后再划分，避免同源近重复跨集（edition2 §4）。
分组键为 f"{dataset}:{source_image_id}"，组内所有样本进同一集。

输出：
  <out-dir>/pairs_all.jsonl        全部配对（带 eligible 标志与剔除原因）
  <out-dir>/pairs_eligible.jsonl   仅通过的配对，供下游使用
  <out-dir>/manifest_summary.json
"""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image


AREA_MIN_DEFAULT = 0.02
AREA_MAX_DEFAULT = 0.30


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


def check_files(row: dict, source_root: Path) -> str | None:
    """返回 None 表示通过，否则返回剔除原因。"""
    paths = {}
    for key in ("pristine_path", "forged_path", "gt_mask_path"):
        value = row.get(key)
        if not value:
            return f"missing_field:{key}"
        resolved = Path(value)
        if not resolved.is_absolute():
            resolved = source_root / resolved
        if not resolved.is_file():
            return f"file_not_found:{key}"
        paths[key] = resolved

    with Image.open(paths["pristine_path"]) as pristine, Image.open(paths["forged_path"]) as forged:
        if pristine.size != forged.size:
            return f"size_mismatch:{pristine.size}!={forged.size}"
        reference_size = pristine.size
    with Image.open(paths["gt_mask_path"]) as mask:
        if mask.size != reference_size:
            return f"mask_size_mismatch:{mask.size}!={reference_size}"
    return None


def assign_splits(rows: list[dict], ratios: tuple[float, float, float], seed: int) -> None:
    """按 source image 分组划分，组内不可跨集。"""
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        groups[f"{row['dataset']}:{row['source_image_id']}"].append(row)

    keys = sorted(groups)
    random.Random(seed).shuffle(keys)

    total = len(rows)
    train_target = ratios[0] * total
    val_target = ratios[1] * total

    running = 0
    for key in keys:
        if running < train_target:
            split = "train"
        elif running < train_target + val_target:
            split = "val"
        else:
            split = "test"
        for row in groups[key]:
            row["split"] = split
        running += len(groups[key])


def main() -> None:
    parser = argparse.ArgumentParser(description="Build unified Stage-A.3 pair manifest")
    parser.add_argument("--inputs", nargs="+", required=True, help="各数据集的 pairs_*.jsonl")
    parser.add_argument("--source-root", required=True, help="manifest 相对路径的解析根")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--area-min", type=float, default=AREA_MIN_DEFAULT)
    parser.add_argument("--area-max", type=float, default=AREA_MAX_DEFAULT)
    parser.add_argument("--min-pair-quality-ratio", type=float, default=3.0)
    parser.add_argument("--split-ratios", nargs=3, type=float, default=(0.7, 0.15, 0.15))
    parser.add_argument("--seed", type=int, default=20260921)
    args = parser.parse_args()

    source_root = Path(args.source_root)
    rows: list[dict] = []
    for value in args.inputs:
        rows.extend(read_jsonl(Path(value)))
    if not rows:
        raise ValueError("未读到任何配对")

    duplicates = [key for key, count in Counter(r["sample_id"] for r in rows).items() if count > 1]
    if duplicates:
        raise ValueError(f"sample_id 重复: {duplicates[:5]}")

    for row in rows:
        reasons = []
        file_problem = check_files(row, source_root)
        if file_problem:
            reasons.append(file_problem)
        area = row.get("mask_area_ratio")
        if area is None or not (args.area_min <= float(area) <= args.area_max):
            reasons.append(f"area_out_of_band:{area}")
        quality = row.get("pair_quality_ratio")
        if quality is None or float(quality) < args.min_pair_quality_ratio:
            reasons.append(f"pair_quality_too_low:{quality}")
        row["exclusion_reasons"] = reasons
        row["eligible"] = not reasons
        # 兼容远程既有脚本：run_fakevlm_originals.py / score_*_variants.py 读的是
        # row["image_path"]。这里指伪造图（被审计对象），不要改成 pristine。
        row["image_path"] = row.get("forged_path")

    eligible = [row for row in rows if row["eligible"]]
    if not eligible:
        raise ValueError("没有任何配对通过准入条件")
    assign_splits(eligible, tuple(args.split_ratios), args.seed)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    all_path = out_dir / "pairs_all.jsonl"
    with all_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    eligible_path = out_dir / "pairs_eligible.jsonl"
    with eligible_path.open("w", encoding="utf-8") as handle:
        for row in eligible:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    def describe(values: list[float], label: str) -> dict:
        values = sorted(values)
        if not values:
            return {label: None}
        n = len(values)
        return {
            "n": n,
            "min": values[0],
            "median": values[n // 2],
            "max": values[-1],
        }

    summary = {
        "total_pairs": len(rows),
        "eligible_pairs": len(eligible),
        "excluded_pairs": len(rows) - len(eligible),
        "eligibility": {
            "area_band": [args.area_min, args.area_max],
            "min_pair_quality_ratio": args.min_pair_quality_ratio,
        },
        "by_dataset": {
            dataset: {
                "total": sum(1 for r in rows if r["dataset"] == dataset),
                "eligible": sum(1 for r in eligible if r["dataset"] == dataset),
            }
            for dataset in sorted({r["dataset"] for r in rows})
        },
        "exclusion_reason_counts": dict(
            Counter(reason.split(":")[0] for r in rows for reason in r["exclusion_reasons"])
        ),
        "split_counts": dict(Counter(r["split"] for r in eligible)),
        "eligible_mask_area_ratio": describe([float(r["mask_area_ratio"]) for r in eligible], "area"),
        "eligible_pair_quality_ratio": describe(
            [float(r["pair_quality_ratio"]) for r in eligible], "quality"
        ),
        "source_root": str(source_root),
        "seed": args.seed,
        "split_ratios": list(args.split_ratios),
        "outputs": {"all": str(all_path), "eligible": str(eligible_path)},
    }
    (out_dir / "manifest_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
