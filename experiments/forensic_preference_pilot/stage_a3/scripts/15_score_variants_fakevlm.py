#!/usr/bin/env python3
"""用 FakeVLM 自己对变体打分（通用变体名）。

## 为什么必须单独一个脚本

FakeVLM 是 LLaVA 架构，prompt 模板与 Qwen3-VL 不同。用 Qwen3-VL 的打分器
（`scripts/score_qwen3vl_variants.py` 的 `score_image`）去打 FakeVLM 会直接报错：

    ValueError: Image features and image tokens do not match, tokens: 575, features: 2359296

（已实测踩过。）必须走 `faithpilot.fakevlm_adapter` 的 `configure_llava_processor`
+ `score_completion`，与既有 `scripts/score_fakevlm_variants.py` 完全一致。

## 与原脚本的差别

原脚本的 `VARIANTS` 是写死的六个 V3 名称；本脚本**读取 manifest 里实际有的变体**，
以便复用到 `restore_*` 等新算子。

## 输出兼容性

产出 `log_likelihoods = {"fake": fake.mean, "real": real.mean}`，
使得 09_measure_effects.py 的 `log_odds = ll[fake] − ll[real]` 等于 FakeVLM 的
`log_odds_mean` —— 与既有 FF++ Gate 0 的数值同尺度，可直接对比。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import torch
from PIL import Image
from transformers import AutoProcessor, LlavaForConditionalGeneration


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

from faithpilot.fakevlm_adapter import configure_llava_processor, score_completion  # noqa: E402


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
    parser = argparse.ArgumentParser(description="Score variants with FakeVLM (LLaVA)")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--fake-completion", default=" This is a fake image.")
    parser.add_argument("--real-completion", default=" This is a real image.")
    parser.add_argument("--variants", nargs="*", default=None, help="不给则打 manifest 里全部变体")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    source_root = Path(args.source_root)

    def resolve(value: str) -> str:
        path = Path(value)
        return str(path if path.is_absolute() else source_root / path)

    rows = [row for row in read_jsonl(Path(args.manifest)) if not row.get("error")]
    if args.limit is not None:
        rows = rows[: args.limit]

    device = torch.device("cuda")
    processor = AutoProcessor.from_pretrained(args.model_path)
    model = LlavaForConditionalGeneration.from_pretrained(
        args.model_path, torch_dtype=torch.bfloat16, low_cpu_mem_usage=True,
        attn_implementation="sdpa",
    ).eval().to(device)
    configure_llava_processor(processor, model)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    handle = output.open("w", encoding="utf-8")

    for index, row in enumerate(rows, 1):
        variants = row.get("variant_paths") or {}
        if args.variants:
            variants = {name: variants[name] for name in args.variants if name in variants}
        scores = {}
        for name, path in variants.items():
            try:
                image = Image.open(resolve(path)).convert("RGB")
                fake = score_completion(model, processor, image, args.fake_completion, device)
                real = score_completion(model, processor, image, args.real_completion, device)
                scores[name] = {
                    "path": path,
                    # 与 09 的 log_odds() 对齐：fake − real = log_odds_mean
                    "log_likelihoods": {"fake": fake.mean, "real": real.mean},
                    "fake_mean": fake.mean,
                    "real_mean": real.mean,
                    "log_odds_mean": fake.mean - real.mean,
                }
            except Exception as exc:  # 单变体失败不拖垮整样本
                scores[name] = {"error": f"{type(exc).__name__}: {exc}"}
        record = {
            "sample_id": row["sample_id"],
            "dataset": row.get("dataset"),
            "model_id": "lingcco/fakeVLM",
            "model_path": args.model_path,
            "control_source": row.get("control_source"),
            "claimed_area_ratio": row.get("claimed_area_ratio"),
            "gt_area_ratio": row.get("gt_area_ratio"),
            "n_variants": len(scores),
            "variant_scores": scores,
        }
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        handle.flush()
        if index % 10 == 0 or index == len(rows):
            print(json.dumps({"done": index, "total": len(rows), "sample_id": row["sample_id"]}), flush=True)

    handle.close()
    print(json.dumps({"n": len(rows), "output": str(output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
