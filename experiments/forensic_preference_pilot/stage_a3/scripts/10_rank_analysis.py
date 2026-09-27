#!/usr/bin/env python3
"""秩检验：对重尾算子噪声免疫的稳健分析（edition4 补充分析 A）。

## 为什么需要它

均值差分析（09_measure_effects.py）显示 `claimed_gap ≈ 0`（p=0.89），但**阳性对照 gt_gap
也不显著**（p=0.29）——所以 null 结果不可证伪。根因是每样本 gap 的标准差高达 4.4（重尾），
n=140 只能检出 |gap| > 0.75。

**秩检验绕开这个问题**：不比较差值大小，只比较**区域内排序**。秩有界，不受重尾拖累。

## 检验设计

每样本有一组等面积、不重叠的区域：{claimed, control_1, control_2, control_3}。
若模型确实特异依赖它声称的区域，那么 `Δs(claimed)` 应当**系统性地排名靠前**。

    统计量 = claimed 的平均秩（1 = Δs 最大）
    零假设 = claimed 与其它三个对照可交换 → 平均秩的期望 = 2.5
    置换检验 = 在样本内随机重新指派哪个区域是"claimed"，重复 N 次得到零分布

对 `gt` 做同样的检验，作为**阳性对照**：若连真实伪迹区域都排不到前面，
则本仪器无效，`claimed` 的结论不得解读。

额外输出：claimed 排第一的比例（零假设 0.25），以及符号检验（claimed_gap > 0 的比例）。
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

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
    if not isinstance(score, dict):
        return None
    likelihoods = score.get("log_likelihoods")
    if not isinstance(likelihoods, dict):
        return None
    if not all(name in likelihoods for name in FAKE_OR_REAL):
        return None
    return float(likelihoods["fake"]) - float(likelihoods["real"])


def build_deltas(row: dict) -> dict[str, float] | None:
    """每样本：各区域相对 original 的 log-odds 下降量。"""
    scores = row.get("variant_scores") or {}
    original = log_odds(scores.get("original"))
    if original is None:
        return None
    deltas: dict[str, float] = {}
    for name, score in scores.items():
        if not name.startswith("resynth_"):
            continue
        value = log_odds(score)
        if value is not None:
            deltas[name.replace("resynth_", "")] = original - value
    return deltas


def target_ranks(
    samples: list[dict[str, float]], target: str, comparison: list[str]
) -> np.ndarray:
    """返回每样本中 target 在这组区域里的秩（1 = Δs 最大）。缺失则跳过该样本。"""
    ranks = []
    for deltas in samples:
        if target not in deltas:
            continue
        values = [deltas[name] for name in comparison if name in deltas]
        if target not in deltas or len(values) < len(comparison):
            continue
        ordered = sorted(values, reverse=True)
        ranks.append(ordered.index(deltas[target]) + 1)
    return np.asarray(ranks, dtype=float)


def permutation_null(
    samples: list[dict[str, float]],
    comparison: list[str],
    resamples: int,
    seed: int,
) -> np.ndarray:
    """零分布：在每样本内随机指派哪个区域是"被检验者"。"""
    rng = np.random.default_rng(seed)
    usable = [d for d in samples if all(name in d for name in comparison)]
    if not usable:
        return np.asarray([])
    values = np.asarray([[d[name] for name in comparison] for d in usable])
    means = []
    for _ in range(resamples):
        picks = rng.integers(0, len(comparison), size=len(usable))
        ranks = np.asarray(
            [(-values[i]).argsort().argsort()[picks[i]] + 1 for i in range(len(usable))]
        )
        means.append(float(ranks.mean()))
    return np.asarray(means)


def main() -> None:
    parser = argparse.ArgumentParser(description="Rank-based robust analysis")
    parser.add_argument("--scores", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--resamples", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=20260921)
    args = parser.parse_args()

    rows = read_jsonl(Path(args.scores))
    samples = [d for d in (build_deltas(row) for row in rows) if d]
    if not samples:
        raise ValueError("没有可用的样本（检查 variant_scores 是否含 original 与 log_likelihoods）")

    controls = ["control_1", "control_2", "control_3"]
    result: dict = {
        "n_samples": len(samples),
        "comparison_set": controls,
        "method": "样本内秩检验 + 置换零分布（对重尾噪声免疫）",
    }

    for target, label in (("claimed", "声称区域"), ("gt", "真实伪迹区域（阳性对照）")):
        comparison = [target] + controls
        ranks = target_ranks(samples, target, comparison)
        if not len(ranks):
            result[target] = {"n": 0}
            continue
        null = permutation_null(samples, comparison, args.resamples, args.seed)
        observed_mean = float(ranks.mean())
        null_mean = float(null.mean()) if len(null) else None
        p_value = (
            float((np.abs(null - null_mean) >= abs(observed_mean - null_mean)).mean())
            if len(null)
            else None
        )
        expected_top = 1.0 / len(comparison)
        result[target] = {
            "label": label,
            "n": int(len(ranks)),
            "mean_rank": observed_mean,
            "null_mean_rank": null_mean,
            "median_rank": float(np.median(ranks)),
            "p_permutation": p_value,
            "top1_fraction": float((ranks == 1).mean()),
            "top1_expected": expected_top,
            "top1_binomial_p": binom_two_sided(int((ranks == 1).sum()), len(ranks), expected_top),
            "rank_histogram": {int(k): int(v) for k, v in zip(*np.unique(ranks, return_counts=True))},
        }

    # 符号检验：claimed_gap > 0 的比例（等价于 claimed 是否比对照均值更靠前）
    signs = []
    for deltas in samples:
        if "claimed" not in deltas:
            continue
        present = [deltas[name] for name in controls if name in deltas]
        if not present:
            continue
        signs.append(1 if deltas["claimed"] > float(np.mean(present)) else 0)
    if signs:
        result["sign_test"] = {
            "n": len(signs),
            "positive_fraction": float(np.mean(signs)),
            "p_binomial_vs_half": binom_two_sided(int(np.sum(signs)), len(signs), 0.5),
        }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def binom_two_sided(successes: int, trials: int, p: float) -> float:
    if trials == 0:
        return float("nan")

    def pmf(k: int) -> float:
        return math.comb(trials, k) * (p**k) * ((1 - p) ** (trials - k))

    observed = pmf(successes)
    return float(min(1.0, sum(pmf(k) for k in range(trials + 1) if pmf(k) <= observed + 1e-12)))


if __name__ == "__main__":
    main()
