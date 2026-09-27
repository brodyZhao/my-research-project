#!/usr/bin/env python3
"""计算必要性与特异性效应量（edition3 §3 指标定义）。

    s(I)                    = logP(fake|I) − logP(real|I)        ← 两路 log-odds，不用 p_fake
    Δs(E)                   = s(original) − s(resynth_E)         必要性
    Δs(control)             = mean_i Δs(control_i)
    gap(E)                  = Δs(E) − Δs(control)                特异性
    额外记录                 Δs(random)（算子一般效应）、Δs(gt)（已知伪迹的效应）

为什么用 log-odds：edition1 实测 p_fake 已饱和（均值 0.785、63/80 ≥ 0.5），
差值被天花板压住，均值/中位数相差 24 倍。log-odds 无界，不受此限。

统计：bootstrap 95% CI、paired sign-flip、positive fraction、median；
多重比较用 Holm 校正。

另计算 IoU(claimed, gt) 以划分 correct-but-unfaithful 单元格
（IoU 高 × gap 低 = 模型"说对了位置"但判定不依赖它）。
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image

MASK_THRESHOLD = 127
FAKE_OR_REAL = ("fake", "real")


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


def log_odds(score: dict | None) -> float | None:
    """s(I) = logP(fake) − logP(real)，取自 forced-choice 的 candidate log-likelihood。"""
    if not isinstance(score, dict) or "log_likelihoods" not in score:
        return None
    likelihoods = score["log_likelihoods"]
    if not all(name in likelihoods for name in FAKE_OR_REAL):
        return None
    return float(likelihoods["fake"]) - float(likelihoods["real"])


def bootstrap_ci(values: np.ndarray, resamples: int, seed: int) -> list[float | None]:
    if not len(values):
        return [None, None]
    rng = np.random.default_rng(seed)
    means = np.asarray(
        [rng.choice(values, size=len(values), replace=True).mean() for _ in range(resamples)]
    )
    return [float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))]


def sign_flip(values: np.ndarray, resamples: int, seed: int) -> float | None:
    if not len(values):
        return None
    rng = np.random.default_rng(seed)
    observed = abs(float(values.mean()))
    extreme = sum(
        1
        for _ in range(resamples)
        if abs(float((values * rng.choice([-1, 1], size=len(values))).mean())) >= observed
    )
    return float((extreme + 1) / (resamples + 1))


def summarize(values: list[float], resamples: int, seed: int) -> dict:
    arr = np.asarray([v for v in values if v is not None and math.isfinite(v)], dtype=float)
    if not len(arr):
        return {"n": 0}
    return {
        "n": int(len(arr)),
        "mean": float(arr.mean()),
        "median": float(np.median(arr)),
        "bootstrap_ci95": bootstrap_ci(arr, resamples, seed),
        "sign_flip_p": sign_flip(arr, resamples, seed + 1000),
        "positive_fraction": float((arr > 0).mean()),
    }


def holm(pvalues: dict[str, float]) -> dict[str, float]:
    """Holm 校正。输入 name -> 未校正 p。"""
    items = sorted(pvalues.items(), key=lambda kv: kv[1])
    m = len(items)
    adjusted: dict[str, float] = {}
    running = 0.0
    for rank, (name, pvalue) in enumerate(items):
        candidate = min(1.0, pvalue * (m - rank))
        running = max(running, candidate)
        adjusted[name] = running
    return adjusted


def iou(path_a: Path, path_b: Path) -> float | None:
    if not (path_a.is_file() and path_b.is_file()):
        return None
    first = np.asarray(Image.open(path_a).convert("L")) > MASK_THRESHOLD
    second = np.asarray(Image.open(path_b).convert("L")) > MASK_THRESHOLD
    if first.shape != second.shape:
        return None
    union = np.logical_or(first, second).sum()
    return float(np.logical_and(first, second).sum() / union) if union else None


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute necessity and specificity effects")
    parser.add_argument("--scores", required=True, help="08_score_variants.py 的输出")
    parser.add_argument("--masks-dir", default=None, help="含 <sample_id>__claimed.png / __gt.png 的目录")
    parser.add_argument("--output", required=True)
    parser.add_argument("--csv", required=True)
    parser.add_argument("--resamples", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20260921)
    parser.add_argument("--iou-high", type=float, default=0.5)
    parser.add_argument("--gap-low", type=float, default=0.5, help="gap 低于此值视为'判定不依赖'（log-odds 单位）")
    # 变体名可配置：不同实验的算子不同（resynth_* 生成式重合成 / restore_* 逐像素恢复）
    parser.add_argument("--claimed-name", default="resynth_claimed")
    parser.add_argument("--control-prefix", default="resynth_control_")
    parser.add_argument("--gt-name", default="resynth_gt")
    parser.add_argument("--gtcontrol-prefix", default=None, help="GT 专用的等面积大对照前缀（面积匹配 GT）")
    parser.add_argument("--whole-name", default=None, help="整图替换变体名；有 pristine 的域用它作最强阳性对照")
    parser.add_argument("--noop-name", default=None, help="与原图逐像素相同的变体名；用于确认打分为确定性")
    args = parser.parse_args()

    rows = read_jsonl(Path(args.scores))
    masks_dir = Path(args.masks_dir) if args.masks_dir else None

    per_sample = []
    for row in rows:
        scores = row.get("variant_scores") or {}
        original = log_odds(scores.get("original"))
        if original is None:
            continue

        def delta(name: str) -> float | None:
            value = log_odds(scores.get(name))
            return None if value is None else original - value

        claimed = delta(args.claimed_name)
        control_values = [delta(name) for name in scores if name.startswith(args.control_prefix)]
        control_values = [v for v in control_values if v is not None]
        control = float(np.mean(control_values)) if control_values else None

        gt_delta = delta(args.gt_name)
        gt_control = None
        if args.gtcontrol_prefix:
            gt_control_values = [delta(n) for n in scores if n.startswith(args.gtcontrol_prefix)]
            gt_control_values = [v for v in gt_control_values if v is not None]
            gt_control = float(np.mean(gt_control_values)) if gt_control_values else None
        # GT 的对照优先用面积匹配 GT 的那批；没有则退回 claimed 匹配的对照（并标记，便于分层报告）
        gt_control_used = gt_control if gt_control is not None else control
        gt_control_source = (
            "gt_area_matched" if gt_control is not None else ("claimed_matched_fallback" if control is not None else None)
        )

        item = {
            "sample_id": row["sample_id"],
            "dataset": row.get("dataset"),
            "control_source": row.get("control_source"),
            "s_original": original,
            "delta_claimed": claimed,
            "delta_control": control,
            "delta_random": delta("resynth_random"),
            "delta_gt": gt_delta,
            "delta_gt_control": gt_control,
            "delta_gt_control_source": gt_control_source,
            "delta_whole": delta(args.whole_name) if args.whole_name else None,
            "delta_noop": delta(args.noop_name) if args.noop_name else None,
            "n_controls": len(control_values),
            "claimed_area_ratio": row.get("claimed_area_ratio"),
            "gt_area_ratio": row.get("gt_area_ratio"),
            "claimed_gap": (claimed - control) if (claimed is not None and control is not None) else None,
            # 阳性对照的特异性：真实伪迹区域相对【面积匹配于它】的对照的超出量。
            # 必须面积匹配——FakeVLM 声称的区域中位数仅 2.35%，而 GT 覆盖整张脸，差 10 倍。
            "gt_gap": (
                gt_delta - gt_control_used
                if (gt_delta is not None and gt_control_used is not None)
                else None
            ),
            "iou_claimed_gt": None,
        }
        if masks_dir is not None:
            item["iou_claimed_gt"] = iou(
                masks_dir / f"{row['sample_id']}__claimed.png",
                masks_dir / f"{row['sample_id']}__gt.png",
            )
        per_sample.append(item)

    def collect(key: str) -> list[float]:
        return [row[key] for row in per_sample if row.get(key) is not None]

    summary_keys = (
        "delta_claimed", "delta_control", "claimed_gap",
        "delta_gt", "delta_gt_control", "gt_gap",
        "delta_whole", "delta_noop", "delta_random",
    )
    summaries = {
        key: summarize(collect(key), args.resamples, args.seed + offset)
        for offset, key in enumerate(summary_keys)
    }
    pvalues = {
        key: summaries[key]["sign_flip_p"]
        for key in ("delta_claimed", "claimed_gap", "gt_gap")
        if summaries[key].get("sign_flip_p") is not None
    }

    # correct-but-unfaithful：IoU 高（说对位置）× gap 低（判定不依赖）
    cell = [
        row for row in per_sample
        if row.get("iou_claimed_gt") is not None
        and row["iou_claimed_gt"] >= args.iou_high
        and row.get("claimed_gap") is not None
        and row["claimed_gap"] <= args.gap_low
    ]
    high_iou = [
        row for row in per_sample
        if row.get("iou_claimed_gt") is not None and row["iou_claimed_gt"] >= args.iou_high
    ]

    result = {
        "n": len(per_sample),
        "score_prompt_version": rows[0].get("score_prompt_version") if rows else None,
        "metric": "log-odds 差值（不用饱和 p_fake）",
        "summaries": summaries,
        "holm_adjusted_p": holm(pvalues) if pvalues else {},
        "correct_but_unfaithful": {
            "criteria": {"iou_claimed_gt_min": args.iou_high, "claimed_gap_max": args.gap_low},
            "n_high_iou": len(high_iou),
            "n_cell": len(cell),
            "fraction_of_high_iou": (len(cell) / len(high_iou)) if high_iou else None,
            "sample_ids": [row["sample_id"] for row in cell[:20]],
        },
        "control_source_counts": {},
    }
    counts: dict[str, int] = {}
    for row in per_sample:
        key = str(row.get("control_source"))
        counts[key] = counts.get(key, 0) + 1
    result["control_source_counts"] = counts

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    csv_path = Path(args.csv)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(per_sample[0]) if per_sample else ["sample_id"])
        writer.writeheader()
        writer.writerows(per_sample)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
