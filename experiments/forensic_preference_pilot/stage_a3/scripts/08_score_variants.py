#!/usr/bin/env python3
"""对重合成变体做 forced-choice 打分。

## 两个关键设计

**1. 必须把 `original` 也一起打分。**
   必要性定义为 Δs(E) = s(original) − s(resynth_E)。若 s(original) 取自别的运行
   （不同 prompt / 不同模型加载），两边就不可比。本脚本在**同一次运行、同一个
   prompt、同一个模型实例**下把所有变体（含 original）全部打分，差值在运行内自洽。

**2. 打分数学复用远程既有实现**（scripts/score_qwen3vl_variants.py 的 score_image），
   不重写 —— 保证与既往 Gate 0 的口径一致。

输出：每样本每变体的 p_fake / log_likelihoods / verdict_argmax，以及算子参数透传。
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path

import torch
from transformers import AutoModelForImageTextToText, AutoProcessor

SCRIPTS_DIR = Path(__file__).resolve().parent


def find_project_root(explicit: str | None) -> Path:
    if explicit:
        candidate = Path(explicit).resolve()
        if (candidate / "faithpilot" / "__init__.py").is_file():
            return candidate
        raise FileNotFoundError(f"{candidate} 下没有 faithpilot 包")
    for parent in [Path(__file__).resolve().parent, *Path(__file__).resolve().parents]:
        if (parent / "faithpilot" / "__init__.py").is_file():
            return parent
    raise FileNotFoundError("向上找不到 faithpilot 包，请用 --project-root 指定")


PROJECT_ROOT = find_project_root(os.environ.get("FAITHPILOT_PROJECT_ROOT"))
sys.path.insert(0, str(PROJECT_ROOT))

from faithpilot.prompts import FORENSICS_PROMPTS  # noqa: E402


def load_scorer():
    """加载远程既有的 score_image（打分数学的唯一来源，勿重写）。"""
    path = PROJECT_ROOT / "scripts" / "score_qwen3vl_variants.py"
    spec = importlib.util.spec_from_file_location("score_qwen3vl_variants", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["score_qwen3vl_variants"] = module
    spec.loader.exec_module(module)
    return module.score_image


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


def main() -> None:
    parser = argparse.ArgumentParser(description="Score resynthesis variants with forced-choice log-odds")
    parser.add_argument("--manifest", required=True, help="07_resynthesize.py 的输出")
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--prompt-profile", choices=tuple(FORENSICS_PROMPTS), default="v2")
    parser.add_argument("--max-pixels", type=int, default=1024 * 1024)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    score_image = load_scorer()
    _, prompt = FORENSICS_PROMPTS[args.prompt_profile]
    prompt_version = FORENSICS_PROMPTS[args.prompt_profile][0]

    source_root = Path(args.source_root)

    def resolve(value: str) -> str:
        path = Path(value)
        return str(path if path.is_absolute() else source_root / path)

    processor = AutoProcessor.from_pretrained(
        args.model, min_pixels=256 * 28 * 28, max_pixels=args.max_pixels
    )
    model = AutoModelForImageTextToText.from_pretrained(
        args.model, dtype=torch.bfloat16, device_map="cuda", low_cpu_mem_usage=True
    ).eval()

    rows = read_jsonl(Path(args.manifest))
    rows = [row for row in rows if not row.get("error")]
    if args.limit is not None:
        rows = rows[: args.limit]

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    handle = output.open("w", encoding="utf-8")

    for index, row in enumerate(rows, 1):
        variants = row.get("variant_paths") or {}
        scores = {}
        for name, path in variants.items():
            try:
                scores[name] = score_image(model, processor, resolve(path), prompt)
            except Exception as exc:  # 单个变体失败不拖垮整样本
                scores[name] = {"error": f"{type(exc).__name__}: {exc}"}
        record = {
            "sample_id": row["sample_id"],
            "dataset": row.get("dataset"),
            "score_prompt_version": prompt_version,
            "score_prompt": prompt,
            "model_path": args.model,
            "control_source": row.get("control_source"),
            "claimed_area_ratio": row.get("claimed_area_ratio"),
            "control_areas": row.get("control_areas"),
            "operator": row.get("operator"),
            "variant_scores": scores,
        }
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        handle.flush()
        if index % 10 == 0 or index == len(rows):
            print(json.dumps({"done": index, "total": len(rows), "sample_id": row["sample_id"]}), flush=True)

    handle.close()
    print(json.dumps({"n": len(rows), "prompt_version": prompt_version, "output": str(output)},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
