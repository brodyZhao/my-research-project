#!/usr/bin/env python3
"""内容扰动验证：改变"解释所指的那块内容"，解释会不会跟着变？

## 要检验什么

原框架把"解释与判定脱钩"操作化成**判定**的属性（移除证据→判定变不变），这在纯生成域上
测不干净（算子效应处处相同、阳性对照不显著）。本脚本换成**解释**的属性：

    把模型自己指的那块区域的内容换掉
        → 忠实的解释应当跟着变（它描述的东西已经不同了）
        → 模板化的解释不会变（它本来就没在看图）

    对照：换掉一块等面积、语义匹配、但模型没提到的区域
        → 忠实模型的解释应当**基本不变**（那与它说的东西无关）

## 判据

```
忠实：sim(original, perturb_claimed)  <  sim(original, perturb_control)
模板：两者都 ≈ 1（换哪里它都说同一句），或两者都低（对任何扰动都反应，不分对象）
```

若 `sim_claimed ≈ sim_control` 且都接近 1 → **解释不随其所指内容变化** → 上游钉子成立。

## 说明

本测试**不需要 pristine、不需要"决策价值"**，且阳性对照天然成立：
内容变了而解释必须变，否则解释就不是关于图像的。这是它与失败的必要性检验的根本区别。
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path

import numpy as np

SCRIPTS_DIR = Path(__file__).resolve().parent


def _load_sibling(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_audit = _load_sibling("16_metric_audit_text")
normalize = _audit.normalize
rouge_l = _audit.rouge_l

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


def explanation(row: dict) -> str:
    parsed = row.get("parsed_output") or {}
    return str(parsed.get("rationale") or row.get("raw_output") or "")


def verdict(row: dict) -> str | None:
    return (row.get("parsed_output") or {}).get("verdict")


def region_box(row: dict) -> list[float] | None:
    regions = (row.get("parsed_output") or {}).get("evidence_regions") or []
    if not regions:
        return None
    box = regions[0].get("bbox")
    return [float(v) for v in box] if isinstance(box, list) and len(box) == 4 else None


def box_iou(first: list[float], second: list[float]) -> float:
    x1 = max(first[0], second[0])
    y1 = max(first[1], second[1])
    x2 = min(first[2], second[2])
    y2 = min(first[3], second[3])
    if x2 <= x1 or y2 <= y1:
        return 0.0
    intersection = (x2 - x1) * (y2 - y1)
    area_first = (first[2] - first[0]) * (first[3] - first[1])
    area_second = (second[2] - second[0]) * (second[3] - second[1])
    union = area_first + area_second - intersection
    return float(intersection / union) if union > 0 else 0.0


def sign_test(values: list[float]) -> float:
    """单侧符号检验：有多少比例 > 0。返回二项 p。"""
    positive = sum(1 for v in values if v > 0)
    n = len(values)
    if n == 0:
        return float("nan")
    # 单侧（H1: 正的多）
    return float(sum(math.comb(n, k) for k in range(positive, n + 1)) / 2**n)


def main() -> None:
    parser = argparse.ArgumentParser(description="Content perturbation test on explanations")
    parser.add_argument("--original", required=True)
    parser.add_argument("--perturb-claimed", required=True)
    parser.add_argument("--perturb-control", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    base = {row["sample_id"]: row for row in read_jsonl(Path(args.original))}
    claimed = {row["sample_id"]: row for row in read_jsonl(Path(args.perturb_claimed))}
    control = {row["sample_id"]: row for row in read_jsonl(Path(args.perturb_control))}

    records = []
    for sample_id, base_row in base.items():
        if sample_id not in claimed or sample_id not in control:
            continue
        if base_row.get("parse_status") != "ok":
            continue
        base_text = explanation(base_row)
        claimed_text = explanation(claimed[sample_id])
        control_text = explanation(control[sample_id])

        sim_claimed = rouge_l(claimed_text, base_text)
        sim_control = rouge_l(control_text, base_text)
        if sim_claimed is None or sim_control is None:
            continue

        base_box = region_box(base_row)
        claimed_box = region_box(claimed[sample_id])
        control_box = region_box(control[sample_id])

        records.append(
            {
                "sample_id": sample_id,
                "sim_claimed": sim_claimed,
                "sim_control": sim_control,
                "sim_diff": sim_control - sim_claimed,  # >0 表示声称侧变更多（忠实的方向）
                "exact_change_claimed": normalize(claimed_text) != normalize(base_text),
                "exact_change_control": normalize(control_text) != normalize(base_text),
                "verdict_base": verdict(base_row),
                "verdict_claimed": verdict(claimed[sample_id]),
                "verdict_control": verdict(control[sample_id]),
                "region_iou_claimed": box_iou(base_box, claimed_box) if (base_box and claimed_box) else None,
                "region_iou_control": box_iou(base_box, control_box) if (base_box and control_box) else None,
            }
        )

    if not records:
        raise ValueError("没有可配对的样本，检查三个输入文件的 sample_id 是否一致")

    def collect(key: str) -> list[float]:
        return [row[key] for row in records if row.get(key) is not None]

    sim_claimed_values = collect("sim_claimed")
    sim_control_values = collect("sim_control")
    diffs = collect("sim_diff")

    result = {
        "n": len(records),
        "explanation_similarity_to_original": {
            "perturb_claimed_region": {
                "mean": float(np.mean(sim_claimed_values)),
                "median": float(np.median(sim_claimed_values)),
            },
            "perturb_control_region": {
                "mean": float(np.mean(sim_control_values)),
                "median": float(np.median(sim_control_values)),
            },
        },
        "paired_test": {
            "mean_sim_diff_control_minus_claimed": float(np.mean(diffs)),
            "fraction_claimed_changed_more": float(np.mean([d > 0 for d in diffs])),
            "sign_test_p": sign_test(diffs),
            "note": "忠实模型应表现为 sim_claimed 明显低于 sim_control（声称侧变更多）",
        },
        "exact_text_change_rate": {
            "claimed": float(np.mean([row["exact_change_claimed"] for row in records])),
            "control": float(np.mean([row["exact_change_control"] for row in records])),
        },
        "verdict_flip_rate": {
            "claimed": float(np.mean([row["verdict_base"] != row["verdict_claimed"] for row in records])),
            "control": float(np.mean([row["verdict_base"] != row["verdict_control"] for row in records])),
        },
        "named_region_iou_with_original": {
            "claimed": float(np.mean(collect("region_iou_claimed"))) if collect("region_iou_claimed") else None,
            "control": float(np.mean(collect("region_iou_control"))) if collect("region_iou_control") else None,
        },
        "verdict": None,
    }

    # 判据：两种失败模式都可判定
    both_high = min(np.mean(sim_claimed_values), np.mean(sim_control_values)) > 0.6
    no_difference = abs(np.mean(diffs)) < 0.1
    if both_high and no_difference:
        result["verdict"] = "EXPLANATION_IS_CONTENT_INVARIANT"
        result["interpretation"] = (
            "换掉声称区域与换掉对照区域，解释的变化量都极小且无差异"
            " → 解释不随其所指的内容变化 → 上游钉子成立"
        )
    elif np.mean(diffs) > 0.1 and sign_test(diffs) < 0.05:
        result["verdict"] = "EXPLANATION_TRACKS_ITS_SUBJECT"
        result["interpretation"] = (
            "换掉声称区域时解释变化显著大于换掉对照区域 → 解释确实在跟踪它所描述的内容 → 上游钉子在 Qwen3-VL 上不成立"
        )
    else:
        result["verdict"] = "INCONCLUSIVE"
        result["interpretation"] = "两种失败模式都不满足，需检查算子强度或样本量"

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
