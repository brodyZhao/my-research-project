#!/usr/bin/env python3
"""Gate 7：解释是否真的针对图像生成（解释接地性检验）。

为什么必须有这道门：edition3 的整套空间分析（§A3.6–A3.8）都建立在
"每个样本有自己的 claimed evidence"之上。如果模型对绝大多数样本给出**同一句**
解释，那么：
  - claimed 区域在样本间几乎不变 → IoU(claimed, GT) 无方差，散点图与
    correct-but-unfaithful 单元格无法成立
  - 特异性检验退化：claimed 区域是个常数，谈不上"这张图的证据"
这不是分析做得不够好，而是前提不成立。所以必须在建管线之前先查。

本脚本同时给出一个**不需要任何图像干预**的接地性证据：
把同一批样本的 pristine 真实图喂给同一模型，比较
  (a) 真实图上是否仍给出与伪造图**逐字相同**的解释
  (b) 真实图上是否仍判 fake（假阳性率）
若 (a) 很高或 (b) 很高，说明解释与判定都不依赖图像内容本身。

输入：
  --forged  伪造图 baseline（label=1，含 raw_output）
  --real    pristine 真实图 baseline（label=0，sample_id 与 forged 对齐）
输出：JSON 判定，含 Gate 7 结论。
"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path

import numpy as np

TEMPLATE_MIN_UNIQUE_RATE = 0.50


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


def normalize(text: str) -> str:
    """归一化后再比：只留小写字母与空格。"""
    return re.sub(r"[^a-z ]", "", (text or "").lower()).strip()


def bootstrap_ci(values: np.ndarray, resamples: int, seed: int) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    means = np.asarray(
        [rng.choice(values, size=len(values), replace=True).mean() for _ in range(resamples)]
    )
    return float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))


def diversity(rows: list[dict], field: str) -> dict:
    texts = [normalize(row.get(field) or "") for row in rows]
    counter = Counter(texts)
    top_text, top_count = counter.most_common(1)[0] if counter else ("", 0)
    return {
        "n": len(texts),
        "n_unique": len(counter),
        "unique_rate": len(counter) / len(texts) if texts else None,
        "top_share": top_count / len(texts) if texts else None,
        "top_text": top_text[:200],
        "mouth_share": sum(1 for t in texts if "mouth" in t) / len(texts) if texts else None,
    }


def is_fake(row: dict) -> bool | None:
    """与 04_gate0_accuracy.py 一致的两路判据。"""
    if row.get("forced_verdict_mean") is not None:
        return row["forced_verdict_mean"] == "fake"
    forced = row.get("forced_score")
    if isinstance(forced, dict):
        likelihoods = forced.get("log_likelihoods") or {}
        if "fake" in likelihoods and "real" in likelihoods:
            return float(likelihoods["fake"]) - float(likelihoods["real"]) > 0
        if forced.get("p_fake") is not None:
            return float(forced["p_fake"]) > 0.5
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate 7: are explanations actually image-grounded?")
    parser.add_argument("--forged", required=True)
    parser.add_argument("--real", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--label", default=None)
    parser.add_argument("--text-field", default="raw_output")
    parser.add_argument("--min-unique-rate", type=float, default=TEMPLATE_MIN_UNIQUE_RATE)
    parser.add_argument("--resamples", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20260921)
    args = parser.parse_args()

    forged_rows = read_jsonl(Path(args.forged))
    real_rows = read_jsonl(Path(args.real))

    forged_div = diversity(forged_rows, args.text_field)
    real_div = diversity(real_rows, args.text_field)

    real_decisions = [is_fake(row) for row in real_rows]
    real_decisions = [1.0 if value else 0.0 for value in real_decisions if value is not None]
    false_positive_rate = float(np.mean(real_decisions)) if real_decisions else None
    fp_ci = (
        bootstrap_ci(np.asarray(real_decisions), args.resamples, args.seed)
        if real_decisions
        else (None, None)
    )

    # 交叉比对：同一样本的真实版与伪造版
    forged_by_id = {str(row["sample_id"]): row for row in forged_rows}
    pairs = [
        (forged_by_id[str(row["sample_id"])], row)
        for row in real_rows
        if str(row["sample_id"]) in forged_by_id
    ]
    identical = sum(
        1
        for forged_row, real_row in pairs
        if normalize(forged_row.get(args.text_field) or "")
        == normalize(real_row.get(args.text_field) or "")
    )
    flips = 0
    comparable_flips = 0
    for forged_row, real_row in pairs:
        forged_verdict, real_verdict = is_fake(forged_row), is_fake(real_row)
        if forged_verdict is None or real_verdict is None:
            continue
        comparable_flips += 1
        if forged_verdict != real_verdict:
            flips += 1

    unique_rate = forged_div["unique_rate"] or 0.0
    gate7_pass = unique_rate >= args.min_unique_rate

    result = {
        "gate": "Gate 7 解释接地性",
        "label": args.label,
        "forged": {"input": str(args.forged), **forged_div},
        "real": {"input": str(args.real), **real_div},
        "real_false_positive": {
            "n": len(real_decisions),
            "rate": false_positive_rate,
            "bootstrap_ci95": [fp_ci[0], fp_ci[1]],
            "note": "真实未篡改图被判 fake 的比例；模型若在图上看不到差异，这里也不会低",
        },
        "cross_comparison": {
            "n_pairs": len(pairs),
            "identical_explanation_rate": identical / len(pairs) if pairs else None,
            "verdict_flip_rate": flips / comparable_flips if comparable_flips else None,
            "note": "真实版与伪造版解释逐字相同 → 解释与图像内容脱钩；判定翻转率低 → 判定也不依赖内容",
        },
        "criteria": {
            "min_unique_rate": args.min_unique_rate,
            "forged_unique_rate": unique_rate,
        },
        "verdict": "PASS" if gate7_pass else "FAIL",
        "interpretation": (
            "解释在样本间有足够变化，per-sample claimed-evidence 设计成立"
            if gate7_pass
            else "解释高度模板化 —— 每个样本没有自己的 claimed evidence，"
            "§A3.6–A3.8 的空间分析前提不成立，不得按原设计解读其结论"
        ),
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
