#!/usr/bin/env python3
"""Gate 0：被审计模型在评测集上的检测准确率是否显著高于随机。

为什么这道门必须先过（edition3 §5）：如果模型在该数据集上接近瞎猜，
"模型不依赖它声称的证据"就是平凡结论——一个不会判的模型当然不依赖任何证据。

决策规则统一（重要）：不同模型的 forced-choice 输出格式不同，
  - FakeVLM  : 两路比较 " This is a fake image." vs " This is a real image."
               → 存为 forced_verdict_mean / log_odds_mean
  - Qwen3-VL : 三路 softmax(real/fake/insufficient) 的 verdict_argmax
               → 存为 forced_score.{p_fake, verdict_argmax, log_likelihoods}
三路 argmax 与两路比较是**不同的决策规则**，混用会污染跨模型比较。
因此本脚本统一取两路判据：fake ⟺ log_odds_fake_real > 0（等价于 p_fake > 0.5）。
三路 argmax 只作附注报告，不用于 Gate 判定。

输入：baseline 输出 jsonl（FakeVLM 或 Qwen3-VL 任一格式）
输出：Gate 0 判定 JSON，含 bootstrap 95% CI 与二项检验 p 值。
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np

POSITIVE_LABEL = 1


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


def extract_decision(row: dict) -> tuple[bool, float, str, str | None]:
    """返回 (是否判假, 两路 log-odds, 来源格式, 三路 argmax 或 None)。

    统一用两路判据，保证跨模型可比。
    """
    if "forced_verdict_mean" in row and row.get("log_odds_mean") is not None:
        log_odds = float(row["log_odds_mean"])
        return log_odds > 0, log_odds, "fakevlm_two_way", row.get("generated_verdict")

    forced = row.get("forced_score")
    if isinstance(forced, dict):
        likelihoods = forced.get("log_likelihoods") or {}
        if "fake" in likelihoods and "real" in likelihoods:
            log_odds = float(likelihoods["fake"]) - float(likelihoods["real"])
            return log_odds > 0, log_odds, "qwen3vl_two_way", forced.get("verdict_argmax")
        if forced.get("p_fake") is not None:
            log_odds = math.log(max(float(forced["p_fake"]), 1e-12) / max(1 - float(forced["p_fake"]), 1e-12))
            return log_odds > 0, log_odds, "p_fake_two_way", forced.get("verdict_argmax")

    raise ValueError(f"{row.get('sample_id')} 无法提取决策：既无 forced_verdict_mean 也无 forced_score")


def bootstrap_ci(values: np.ndarray, resamples: int, seed: int) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    means = np.asarray(
        [rng.choice(values, size=len(values), replace=True).mean() for _ in range(resamples)]
    )
    return float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))


def binom_two_sided_p(successes: int, trials: int, p: float = 0.5) -> float:
    if trials == 0:
        return float("nan")

    def pmf(k: int) -> float:
        return math.comb(trials, k) * (p**k) * ((1 - p) ** (trials - k))

    observed = pmf(successes)
    total = sum(pmf(k) for k in range(trials + 1) if pmf(k) <= observed + 1e-12)
    return float(min(1.0, total))


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate 0: detection accuracy must beat chance")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--label", default=None, help="本次判定的标签，便于归档")
    parser.add_argument("--resamples", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20260921)
    parser.add_argument("--min-accuracy", type=float, default=0.65)
    args = parser.parse_args()

    rows = read_jsonl(Path(args.input))
    if not rows:
        raise ValueError("输入为空")

    positives = [row for row in rows if int(row.get("label", POSITIVE_LABEL)) == POSITIVE_LABEL]
    if not positives:
        raise ValueError("没有正类（label==1）样本，无法计算准确率")

    decisions, log_odds_values, sources, argmaxes = [], [], [], []
    for row in positives:
        is_fake, log_odds, source, argmax = extract_decision(row)
        decisions.append(1.0 if is_fake else 0.0)
        log_odds_values.append(log_odds)
        sources.append(source)
        argmaxes.append(argmax)

    decisions = np.asarray(decisions)
    log_odds_arr = np.asarray(log_odds_values)
    accuracy = float(decisions.mean())
    ci = bootstrap_ci(decisions, args.resamples, args.seed)
    p_value = binom_two_sided_p(int(decisions.sum()), len(decisions))

    passed = bool(ci[0] > 0.5 and accuracy >= args.min_accuracy)
    result = {
        "gate": "Gate 0 检测准确率",
        "label": args.label,
        "input": str(args.input),
        "n_positive": len(positives),
        "decision_rule": "两路判据：log_odds(fake vs real) > 0，与 FakeVLM 的 forced_verdict_mean 等价",
        "decision_source": dict(Counter(sources)),
        "two_way": {
            "accuracy": accuracy,
            "bootstrap_ci95": [ci[0], ci[1]],
            "binomial_p_vs_chance": p_value,
            "n_predicted_fake": int(decisions.sum()),
        },
        "log_odds": {
            "mean": float(log_odds_arr.mean()),
            "median": float(np.median(log_odds_arr)),
            "positive_fraction": float((log_odds_arr > 0).mean()),
            "min": float(log_odds_arr.min()),
            "max": float(log_odds_arr.max()),
        },
        "three_way_argmax_note": dict(Counter(a for a in argmaxes if a)),
        "criteria": {
            "ci_lower_above_chance": bool(ci[0] > 0.5),
            "min_accuracy": args.min_accuracy,
            "meets_min_accuracy": bool(accuracy >= args.min_accuracy),
        },
        "verdict": "PASS" if passed else "FAIL",
        "interpretation": (
            "模型在该数据集上有实际判别力，忠实性分析有意义"
            if passed
            else "模型在该数据集上接近随机或无实际判别力 —— 忠实性分析在此组合上无意义，"
            "不得把 '不依赖证据' 解释为发现（那是平凡结论）"
        ),
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
