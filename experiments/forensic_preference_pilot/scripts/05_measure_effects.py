from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np

from common import read_jsonl


def bootstrap(values: np.ndarray, resamples: int, seed: int) -> list[float | None]:
    if not len(values):
        return [None, None]
    rng = np.random.default_rng(seed)
    means = np.asarray([rng.choice(values, size=len(values), replace=True).mean() for _ in range(resamples)])
    return [float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))]


def sign_flip(values: np.ndarray, resamples: int, seed: int) -> float | None:
    if not len(values):
        return None
    rng = np.random.default_rng(seed)
    observed = abs(float(values.mean()))
    extreme = 0
    for _ in range(resamples):
        if abs(float((values * rng.choice([-1, 1], size=len(values))).mean())) >= observed:
            extreme += 1
    return float((extreme + 1) / (resamples + 1))


def summary(values: list[float], resamples: int, seed: int) -> dict:
    arr = np.asarray(values, dtype=float)
    return {
        "n": int(len(arr)),
        "mean": float(arr.mean()) if len(arr) else None,
        "median": float(np.median(arr)) if len(arr) else None,
        "bootstrap_ci95": bootstrap(arr, resamples, seed),
        "sign_flip_p": sign_flip(arr, resamples, seed + 1000),
        "positive_fraction": float((arr > 0).mean()) if len(arr) else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute paired Stage-A effects")
    parser.add_argument("--scores", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--csv", required=True)
    parser.add_argument("--resamples", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20260915)
    args = parser.parse_args()
    rows = read_jsonl(args.scores)
    per_sample = []
    for row in rows:
        s = row["scores"]
        original = float(s["original"]["p_fake"])
        claimed_target = float(s["claimed_target_blur"]["p_fake"])
        claimed_controls = [
            float(s[name]["p_fake"])
            for name in sorted(s)
            if name.startswith("claimed_control_blur_")
        ]
        if not claimed_controls:
            raise ValueError(f"{row['sample_id']} has no claimed controls")
        claimed_control = float(np.mean(claimed_controls))
        gt_target = float(s["gt_target_blur"]["p_fake"]) if "gt_target_blur" in s else math.nan
        gt_controls = [
            float(s[name]["p_fake"])
            for name in sorted(s)
            if name.startswith("gt_control_blur_")
        ]
        gt_control = float(np.mean(gt_controls)) if gt_controls else math.nan
        item = {
            "sample_id": row["sample_id"],
            "p_fake_original": original,
            "p_fake_claimed_target": claimed_target,
            "p_fake_claimed_control": claimed_control,
            "claimed_control_count": len(claimed_controls),
            "claimed_control_min": min(claimed_controls),
            "claimed_control_max": max(claimed_controls),
            "delta_claimed": original - claimed_target,
            "delta_control": original - claimed_control,
            "claimed_gap": (original - claimed_target) - (original - claimed_control),
            "p_fake_gt_target": gt_target,
            "p_fake_gt_control": gt_control,
            "gt_control_count": len(gt_controls),
            "delta_gt": original - gt_target if math.isfinite(gt_target) else math.nan,
            "gt_control_delta": original - gt_control if math.isfinite(gt_control) else math.nan,
            "gt_gap": ((original - gt_target) - (original - gt_control)) if math.isfinite(gt_target) and math.isfinite(gt_control) else math.nan,
            "noop_drift": abs(original - float(s["noop"]["p_fake"])),
            "claimed_area_ratio": row.get("claimed_area_ratio"),
            "gt_area_ratio": row.get("gt_area_ratio"),
        }
        per_sample.append(item)

    def finite(key: str) -> list[float]:
        return [float(row[key]) for row in per_sample if math.isfinite(float(row[key]))]

    result = {
        "material_passport": {
            "origin_skill": "academic-research-suite / experiment-agent",
            "mode": "run",
            "verification_status": "ANALYZED",
        },
        "protocol": "GitHub pilot_experiment_forensic_evidence_preference.md Stage A smoke test",
        "model": "Qwen3-VL-8B-Instruct (cached remote fallback; guide baseline requested 4B was not cached)",
        "n": len(per_sample),
        "summary": {
            "claimed_delta": summary(finite("delta_claimed"), args.resamples, args.seed),
            "control_delta": summary(finite("delta_control"), args.resamples, args.seed + 1),
            "claimed_gap": summary(finite("claimed_gap"), args.resamples, args.seed + 2),
            "gt_delta": summary(finite("delta_gt"), args.resamples, args.seed + 3),
            "gt_gap": summary(finite("gt_gap"), args.resamples, args.seed + 4),
            "noop_drift": summary(finite("noop_drift"), args.resamples, args.seed + 5),
        },
        "notes": [
            "The run uses locked forged images and locked claimed/GT masks; no paired pristine original was available.",
            "Blur is a perturbation diagnostic, not semantic restoration and not causal proof.",
            "Do not proceed to DPO from this smoke test without manual visual inspection and the Stage-A gate.",
        ],
    }
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
