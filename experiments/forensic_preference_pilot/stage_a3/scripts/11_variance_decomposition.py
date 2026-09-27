#!/usr/bin/env python3
"""方差分解：把 gap 的总方差拆成「算子随机性」与「样本异质性」两部分。

## 要回答的问题

`claimed_gap` 在 n=140 上不显著，但**阳性对照 gt_gap 也不显著**，所以结论不可判定。
可能是因为：
  (a) 真的没有效应
  (b) 有 0.4 量级的效应，但被算子自身的随机扰动淹没 → **加种子/加对照就能救**
  (c) 样本间异质性太大 → **只能靠扩 n**，且能算出需要多大 n

这两条路的成本差一个数量级，必须先分开。

## 模型

对每个 (样本, 区域) 在 K 个种子下各得到一个 Δs：

    Var(Δs) = σ²_sample + σ²_seed

σ²_seed 由「同一 (样本,区域) 跨种子的方差」估计（区域内方差），
σ²_sample 由「跨 (样本,区域) 的总方差减去 σ²_seed」估计。

gap = Δs(claimed) − mean(Δs(controls))，其方差中算子贡献为
    (1 + 1/Kc) · σ²_seed / S            Kc = 对照数，S = 平均的种子数

于是可以预测：在给定 (S, Kc, n) 下能检出的最小效应，以及为检出目标效应所需的 n。
"""

from __future__ import annotations

import argparse
import json
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


def deltas_for(path: Path) -> dict[tuple[str, str], float]:
    """返回 {(sample_id, region_name): Δs}。region_name 已去掉 resynth_ 前缀。"""
    result: dict[tuple[str, str], float] = {}
    for row in read_jsonl(path):
        scores = row.get("variant_scores") or {}
        original = log_odds(scores.get("original"))
        if original is None:
            continue
        for name, score in scores.items():
            if not name.startswith("resynth_"):
                continue
            value = log_odds(score)
            if value is not None:
                result[(row["sample_id"], name.replace("resynth_", ""))] = original - value
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Decompose gap variance into operator vs sample components")
    parser.add_argument("--scores", nargs="+", required=True, help="每个种子一个打分文件")
    parser.add_argument("--output", required=True)
    parser.add_argument("--num-controls", type=int, default=3)
    parser.add_argument("--target-effect", type=float, default=0.43, help="希望检出的 gap 效应量")
    args = parser.parse_args()

    per_seed = [deltas_for(Path(p)) for p in args.scores]
    if len(per_seed) < 2:
        raise ValueError("至少需要两个种子的打分文件才能估计算子随机性")

    # 收集每个 (样本, 区域) 跨种子的取值
    keys = set(per_seed[0])
    for other in per_seed[1:]:
        keys &= set(other)
    if not keys:
        raise ValueError("各种子之间没有共同的 (样本, 区域) 键，检查是否用了同一批样本")

    by_key: dict[tuple[str, str], list[float]] = {key: [] for key in keys}
    for table in per_seed:
        for key in keys:
            by_key[key].append(table[key])

    within_vars = [float(np.var(values, ddof=1)) for values in by_key.values() if len(values) > 1]
    sigma2_seed = float(np.mean(within_vars)) if within_vars else float("nan")

    all_values = np.asarray([v for values in by_key.values() for v in values], dtype=float)
    total_var = float(np.var(all_values, ddof=1))
    sigma2_sample = max(0.0, total_var - sigma2_seed)
    operator_share = sigma2_seed / total_var if total_var > 0 else float("nan")

    # gap 的方差：算子部分按 (1 + 1/Kc)/S 缩放，样本部分不随 S 变
    def gap_sd(seeds: int, controls: int) -> float:
        operator = (1.0 + 1.0 / controls) * sigma2_seed / seeds
        return float(np.sqrt(sigma2_sample + operator))

    # 80% 功效、双侧 α=0.05 所需 n ≈ (2.8 · SD / effect)²
    def required_n(seeds: int, controls: int, effect: float) -> float:
        sd = gap_sd(seeds, controls)
        return float((2.8 * sd / effect) ** 2) if effect > 0 else float("inf")

    scenarios = []
    for seeds in (1, 2, 3, 5):
        for controls in (3, 8):
            scenarios.append(
                {
                    "seeds_per_region": seeds,
                    "controls": controls,
                    "gap_sd": gap_sd(seeds, controls),
                    "min_detectable_effect_n140": 2.8 * gap_sd(seeds, controls) / np.sqrt(140),
                    "required_n_for_target": required_n(seeds, controls, args.target_effect),
                }
            )

    result = {
        "n_keys": len(keys),
        "n_samples": len({key[0] for key in keys}),
        "n_seeds": len(per_seed),
        "variance_components": {
            "total_variance_of_delta": total_var,
            "sigma2_seed_operator": sigma2_seed,
            "sigma2_sample_heterogeneity": sigma2_sample,
            "operator_variance_share": operator_share,
        },
        "interpretation": (
            "operator_variance_share 高 → 加种子/加对照即可提高分辨率；"
            "低 → 方差来自样本异质性，只能扩 n"
        ),
        "target_effect": args.target_effect,
        "scenarios": scenarios,
        "output_note": "required_n 按 80% 功效、双侧 α=0.05、配对差的正态近似估算",
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
