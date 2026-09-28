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
输出：Gate 0 判定 JSON，含按类别分层的 bootstrap 95% CI 与置换检验 p 值。
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import numpy as np

FAKE_LABEL = 1
REAL_LABEL = 0


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
            p_fake = min(max(float(forced["p_fake"]), 1e-12), 1 - 1e-12)
            log_odds = float(np.log(p_fake / (1 - p_fake)))
            return log_odds > 0, log_odds, "p_fake_two_way", forced.get("verdict_argmax")

    # Stage-A scored variant records wrap the original forced-choice score.
    original = (row.get("scores") or {}).get("original")
    if isinstance(original, dict):
        if original.get("log_odds_fake_real") is not None:
            log_odds = float(original["log_odds_fake_real"])
            return log_odds > 0, log_odds, "scores_original_log_odds", None
        likelihoods = original.get("log_likelihoods") or {}
        if "fake" in likelihoods and "real" in likelihoods:
            log_odds = float(likelihoods["fake"]) - float(likelihoods["real"])
            return log_odds > 0, log_odds, "scores_original_log_likelihoods", None

    raise ValueError(
        f"{row.get('sample_id')} 无法提取决策：需要 forced_verdict_mean、forced_score "
        "或 scores.original 的真假 log-odds"
    )


def balanced_accuracy(labels: np.ndarray, predictions: np.ndarray) -> float:
    real = labels == REAL_LABEL
    fake = labels == FAKE_LABEL
    if not real.any() or not fake.any():
        raise ValueError("balanced accuracy 需要 real(label=0) 和 fake(label=1) 两类样本")
    real_recall = float((predictions[real] == REAL_LABEL).mean())
    fake_recall = float((predictions[fake] == FAKE_LABEL).mean())
    return (real_recall + fake_recall) / 2


def roc_auc(labels: np.ndarray, scores: np.ndarray) -> float:
    """Mann–Whitney AUC with average ranks for ties; higher score means more fake."""
    positives = labels == FAKE_LABEL
    negatives = labels == REAL_LABEL
    if not positives.any() or not negatives.any():
        raise ValueError("AUROC 需要 real(label=0) 和 fake(label=1) 两类样本")
    order = np.argsort(scores, kind="mergesort")
    sorted_scores = scores[order]
    ranks = np.empty(len(scores), dtype=float)
    start = 0
    while start < len(scores):
        end = start + 1
        while end < len(scores) and sorted_scores[end] == sorted_scores[start]:
            end += 1
        ranks[order[start:end]] = (start + 1 + end) / 2
        start = end
    n_pos = int(positives.sum())
    n_neg = int(negatives.sum())
    rank_sum = float(ranks[positives].sum())
    return (rank_sum - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg)


def bootstrap_balanced_accuracy_ci(
    labels: np.ndarray, predictions: np.ndarray, resamples: int, seed: int
) -> tuple[float, float]:
    """Stratified image bootstrap, retaining each class's observed sample count."""
    real_idx = np.flatnonzero(labels == REAL_LABEL)
    fake_idx = np.flatnonzero(labels == FAKE_LABEL)
    if not len(real_idx) or not len(fake_idx):
        raise ValueError("balanced accuracy bootstrap 需要 real 与 fake 两类样本")
    rng = np.random.default_rng(seed)
    real_draws = rng.choice(real_idx, size=(resamples, len(real_idx)), replace=True)
    fake_draws = rng.choice(fake_idx, size=(resamples, len(fake_idx)), replace=True)
    real_recalls = (predictions[real_draws] == REAL_LABEL).mean(axis=1)
    fake_recalls = (predictions[fake_draws] == FAKE_LABEL).mean(axis=1)
    means = (real_recalls + fake_recalls) / 2
    return float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))


def permutation_p_balanced_accuracy(
    labels: np.ndarray, predictions: np.ndarray, permutations: int, seed: int
) -> float:
    """Upper-tail randomization test: observed balanced accuracy vs shuffled decisions."""
    observed = balanced_accuracy(labels, predictions)
    rng = np.random.default_rng(seed)
    extreme = 0
    for _ in range(permutations):
        if balanced_accuracy(labels, rng.permutation(predictions)) >= observed - 1e-15:
            extreme += 1
    return float((extreme + 1) / (permutations + 1))


def classification_metrics(labels: np.ndarray, predictions: np.ndarray, scores: np.ndarray) -> dict:
    counts = Counter(int(label) for label in labels)
    class_recalls = {}
    for label, name in ((REAL_LABEL, "real_recall"), (FAKE_LABEL, "fake_recall")):
        selected = labels == label
        if selected.any():
            class_recalls[name] = float((predictions[selected] == label).mean())
    if set(counts) != {REAL_LABEL, FAKE_LABEL}:
        present = sorted(counts)
        return {
            "status": "BLOCKED_SINGLE_CLASS",
            "n_by_label": {str(key): value for key, value in counts.items()},
            "accuracy": None,
            "balanced_accuracy": None,
            "auroc": None,
            "available_class_recall": class_recalls,
            "reason": "必须同时有 label=0 real 与 label=1 fake；单类 recall 不能验证真假判别能力。",
            "always_predict_present_class_baseline_recall": 1.0 if present else None,
        }
    real = labels == REAL_LABEL
    fake = labels == FAKE_LABEL
    confusion = {
        "true_real_pred_real": int(np.sum(real & (predictions == REAL_LABEL))),
        "true_real_pred_fake": int(np.sum(real & (predictions == FAKE_LABEL))),
        "true_fake_pred_real": int(np.sum(fake & (predictions == REAL_LABEL))),
        "true_fake_pred_fake": int(np.sum(fake & (predictions == FAKE_LABEL))),
    }
    return {
        "status": "COMPUTABLE",
        "n_by_label": {str(key): value for key, value in counts.items()},
        "confusion_matrix": confusion,
        "accuracy": float((predictions == labels).mean()),
        "balanced_accuracy": balanced_accuracy(labels, predictions),
        "real_recall": class_recalls["real_recall"],
        "fake_recall": class_recalls["fake_recall"],
        "auroc": roc_auc(labels, scores),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate 0: two-class balanced detection ability")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--label", default=None, help="本次判定的标签，便于归档")
    parser.add_argument("--resamples", type=int, default=2000)
    parser.add_argument("--permutations", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=20260921)
    parser.add_argument("--min-balanced-accuracy", "--min-accuracy", dest="min_balanced_accuracy", type=float, default=0.65)
    args = parser.parse_args()

    rows = read_jsonl(Path(args.input))
    if not rows:
        raise ValueError("输入为空")

    labels, decisions, log_odds_values, sources, argmaxes = [], [], [], [], []
    for row in rows:
        if "label" not in row or row["label"] is None:
            raise ValueError(f"{row.get('sample_id')} 缺少二分类 label；不能默认填成正类")
        label_value = int(row["label"])
        if label_value not in (REAL_LABEL, FAKE_LABEL):
            raise ValueError(f"{row.get('sample_id')} 的 label={label_value}；只接受 0=real, 1=fake")
        is_fake, log_odds, source, argmax = extract_decision(row)
        labels.append(label_value)
        decisions.append(FAKE_LABEL if is_fake else REAL_LABEL)
        log_odds_values.append(log_odds)
        sources.append(source)
        argmaxes.append(argmax)

    labels = np.asarray(labels, dtype=int)
    decisions = np.asarray(decisions)
    log_odds_arr = np.asarray(log_odds_values)
    metrics = classification_metrics(labels, decisions, log_odds_arr)
    if metrics["status"] == "COMPUTABLE":
        ci = bootstrap_balanced_accuracy_ci(labels, decisions, args.resamples, args.seed)
        p_value = permutation_p_balanced_accuracy(labels, decisions, args.permutations, args.seed + 1)
        passed = bool(
            ci[0] > 0.5
            and metrics["balanced_accuracy"] >= args.min_balanced_accuracy
            and p_value < 0.05
        )
    else:
        ci, p_value, passed = None, None, False

    result = {
        "gate": "Gate 0 二分类检测能力",
        "label": args.label,
        "input": str(args.input),
        "n": len(rows),
        "label_mapping": {"0": "real", "1": "fake"},
        "decision_rule": "fake iff log_odds(fake vs real) > 0",
        "decision_source": dict(Counter(sources)),
        "metrics": metrics,
        "balanced_accuracy_inference": {
            "stratified_bootstrap_ci95": [ci[0], ci[1]] if ci else None,
            "permutation_p_vs_random_association": p_value,
            "permutations": args.permutations if p_value is not None else None,
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
            "ci_lower_above_chance": bool(ci[0] > 0.5) if ci else False,
            "min_balanced_accuracy": args.min_balanced_accuracy,
            "meets_min_balanced_accuracy": bool(
                metrics.get("balanced_accuracy") is not None
                and metrics["balanced_accuracy"] >= args.min_balanced_accuracy
            ),
            "permutation_p_below_0_05": bool(p_value is not None and p_value < 0.05),
        },
        "verdict": ("PASS" if passed else "FAIL") if metrics["status"] == "COMPUTABLE" else "BLOCKED",
        "interpretation": (
            "模型在该数据集上有可测二分类判别力，忠实性分析准入"
            if passed
            else (
                "输入只有一个类别，不能估计真假二分类能力；补入真实类样本后再评估"
                if metrics["status"] != "COMPUTABLE"
                else "模型未通过预设 balanced accuracy 门槛；不得把无效检测器的零效应解释为不依赖证据"
            )
        ),
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
