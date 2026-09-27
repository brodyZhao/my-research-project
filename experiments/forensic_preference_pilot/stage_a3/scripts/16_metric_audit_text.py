#!/usr/bin/env python3
"""指标审计（文本部分）：现有解释指标能否察觉"解释是模板"？

背景（edition3 §7）：审计文档把待答问题写成两半，edition2 只测了前半
（判定是否依赖声称证据）。这是后半：

    现有解释指标会不会**系统性高估**证据—判断忠实性？

做法：对同一批样本，同时计算
  (A) 模型解释 vs 训练数据参考解释的 ROUGE-L
      —— 这正是 LEGION / FakeVLM 一类工作评测解释质量用的指标
  (B) 模型解释之间的**自相似度**（两两 ROUGE-L）+ 唯一率
      —— 一个朴素的模板探测器

若 (A) 给出不低的分，而 (B) 显示解释高度自相似，则说明
**(A) 这类指标对"模板化"不敏感**，即它们测的不是忠实性。

不需要 GPU：纯文本 LCS 计算。
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
import re
from collections import Counter
from pathlib import Path

BETA = 1.2  # ROUGE-L 标准 F 度量的 beta


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
    """只保留小写字母与空格，便于词级 LCS。"""
    return re.sub(r"[^a-z ]", " ", (text or "").lower()).strip()


def tokens(text: str) -> list[str]:
    return normalize(text).split()


def lcs_length(first: list[str], second: list[str]) -> int:
    """经典 DP。序列长度在百词量级，无需优化。"""
    if not first or not second:
        return 0
    previous = [0] * (len(second) + 1)
    for i in range(1, len(first) + 1):
        current = [0] * (len(second) + 1)
        for j in range(1, len(second) + 1):
            if first[i - 1] == second[j - 1]:
                current[j] = previous[j - 1] + 1
            else:
                current[j] = max(previous[j], current[j - 1])
        previous = current
    return previous[-1]


def rouge_l(hypothesis: str, reference: str) -> float | None:
    hyp, ref = tokens(hypothesis), tokens(reference)
    if not hyp or not ref:
        return None
    lcs = lcs_length(hyp, ref)
    if lcs == 0:
        return 0.0
    recall = lcs / len(ref)
    precision = lcs / len(hyp)
    beta_squared = BETA**2
    return (1 + beta_squared) * recall * precision / (recall + beta_squared * precision)


def build_reference_index(fakeclue_specs: list[tuple[str, Path]]) -> dict[tuple[str, str, str, str], str]:
    """FakeClue 条目 -> 参考解释。

    键 = (split, method, video, frame)，与 12_build_ffpp_pairs.py 的 sample_id 编码一致。

    ⚠️ 注意：FakeClue 元数据里 `image` 字段形如 `ff++/fake/FaceSwap/c23/frames/049_946/092.png`，
    **不含 split 前缀**（train/test 只体现在文件名上）。所以 split 必须由调用方按文件传入。
    """
    pattern = re.compile(
        r"^ff\+\+/fake/(?P<method>[^/]+)/c23/frames/(?P<video>\d+)_\d+/(?P<frame>\d+)\.png$"
    )
    index: dict[tuple[str, str, str, str], str] = {}
    for split, path in fakeclue_specs:
        data = json.loads(path.read_text(encoding="utf-8"))
        for row in data:
            match = pattern.match(str(row.get("image", "")))
            if not match:
                continue
            answers = [c["value"] for c in (row.get("conversations") or []) if c.get("from") == "gpt"]
            if not answers:
                continue
            key = (split, match.group("method"), match.group("video"), match.group("frame"))
            index.setdefault(key, answers[0])
    return index


def main() -> None:
    parser = argparse.ArgumentParser(description="Metric audit (text): does ROUGE-L notice templating?")
    parser.add_argument("--model-explanations", required=True)
    parser.add_argument(
        "--fakeclue-jsons",
        nargs="+",
        required=True,
        help="格式 split:path，例如 train:data/raw/FakeClue_metadata/data_json/train.json",
    )
    parser.add_argument("--output", required=True)
    parser.add_argument("--label", default=None)
    parser.add_argument("--text-field", default="raw_output")
    parser.add_argument("--sample-pairs", type=int, default=3000, help="自相似度抽样的对数")
    parser.add_argument("--seed", type=int, default=20260921)
    args = parser.parse_args()

    rows = read_jsonl(Path(args.model_explanations))
    specs: list[tuple[str, Path]] = []
    for value in args.fakeclue_jsons:
        if ":" not in value:
            raise ValueError(f"--fakeclue-jsons 需要 split:path 格式，收到 {value!r}")
        split, path = value.split(":", 1)
        specs.append((split, Path(path)))
    index = build_reference_index(specs)
    print(json.dumps({"reference_index_size": len(index), "model_rows": len(rows)}), flush=True)

    paired: list[tuple[str, str, str]] = []
    for row in rows:
        sample_id = str(row["sample_id"])
        # ffpp_{split}_{video}_{frame}_{method}
        parts = sample_id.split("_")
        if len(parts) < 5 or parts[0] != "ffpp":
            continue
        split, video, frame, method = parts[1], parts[2], parts[3], "_".join(parts[4:])
        reference = index.get((split, method, video, frame))
        if reference:
            paired.append((sample_id, row.get(args.text_field) or "", reference))

    if not paired:
        raise ValueError("没有匹配到任何参考解释，检查 sample_id 编码与 FakeClue 路径正则")

    rouge_scores = [score for _, hyp, ref in paired if (score := rouge_l(hyp, ref)) is not None]

    texts = [hyp for _, hyp, _ in paired]
    unique = len(set(normalize(t) for t in texts))

    rng = random.Random(args.seed)
    pairs = list(itertools.combinations(range(len(texts)), 2))
    rng.shuffle(pairs)
    pairs = pairs[: args.sample_pairs]
    self_similarity = [score for i, j in pairs if (score := rouge_l(texts[i], texts[j])) is not None]

    def describe(values: list[float]) -> dict:
        if not values:
            return {"n": 0}
        ordered = sorted(values)
        n = len(ordered)
        return {
            "n": n,
            "mean": sum(ordered) / n,
            "median": ordered[n // 2],
            "p90": ordered[int(0.9 * (n - 1))],
            "max": ordered[-1],
        }

    result = {
        "audit": "解释指标是否对模板化不敏感",
        "label": args.label,
        "n_matched": len(paired),
        "A_rouge_l_vs_reference": describe(rouge_scores),
        "B_self_similarity_rouge_l": describe(self_similarity),
        "explanation_uniqueness": {
            "n": len(texts),
            "n_unique": unique,
            "unique_rate": unique / len(texts),
        },
        "interpretation_hint": (
            "若 A 的均值明显高于 0（说明解释与参考'看起来像'）而 B 的均值也高"
            "（说明解释彼此几乎一样），则现有 ROUGE-L 类指标无法区分"
            "'逐图真实解释'与'单一模板'，即它测的不是忠实性。"
        ),
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
