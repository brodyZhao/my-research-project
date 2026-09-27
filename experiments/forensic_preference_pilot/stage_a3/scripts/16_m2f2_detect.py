#!/usr/bin/env python3
"""M2F2-Det 最小推理包装层 —— 第一步只做 Gate 0（能否判真假）。

## 为什么需要这个包装层

M2F2-Det 的官方推理脚本（`llava/serve/cli_DDVQA_det.py`）有三处硬编码：
把图像目录写死成 `./utils/DDVQA_images/c40/test`、输出写死成 `outputs/DDVQA`、
以及只接受 HDF5/特定格式的数据。我们的图是 FF++ 原始 PNG，所以需要一个薄包装。

## 关键接口（从官方脚本逐字抄来，勿改）

    加载      load_deepfake_model(model_path, model_base, model_name, load_8bit, load_4bit, device=)
              model.load_deepfake_encoder(model.config.deepfake_model_path, verbose=True)
    prompt    "Assistant: A chat between a curious human and an artificial intelligence
               assistant. ... ###Human: <image>\\n <deepfake>\\n Determine the authenticity.
               Is the image real or fake? ###Assistant:"
    分词      tokenizer_hybrid_token(prompt, tokenizer, IMAGE_TOKEN_INDEX, DEEPFAKE_TOKEN_INDEX)
    生成      model.generate(..., images=[image], image_sizes=[image_size],
                            deepfake_inputs=[image], do_sample=False, num_beams=1,
                            max_new_tokens=512, use_cache=True, return_dict_in_generate=True)

## 运行环境（重要）

必须用 transformers 4.37 那个独立环境（`m2f2`），不能用主环境（transformers 5.x 会报
meta device 错误）。示例：

    PYTHONPATH=/tmp/M2F2_Det HF_ENDPOINT=https://hf-mirror.com \
    /root/miniconda3/envs/m2f2/bin/python 16_m2f2_detect.py \
        --manifest /tmp/ffpp_gate0_in.jsonl --model-path models/M2F2-Det \
        --output results/stage_a3/m2f2_ffpp_gate0.jsonl --limit 50
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import torch
from PIL import Image

PROMPT = (
    "Assistant: A chat between a curious human and an artificial intelligence assistant. "
    "The assistant gives helpful, detailed, and polite answers to the human's questions."
    "###Human: <image>\n <deepfake>\n Determine the authenticity. Is the image real or fake? "
    "###Assistant:"
)


def find_project_root(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).resolve()
    for parent in [Path(__file__).resolve().parent, *Path(__file__).resolve().parents]:
        if (parent / "faithpilot" / "__init__.py").is_file():
            return parent
    raise FileNotFoundError("找不到项目根")


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
    parser = argparse.ArgumentParser(description="M2F2-Det minimal inference wrapper (Gate 0)")
    parser.add_argument("--manifest", required=True, help="含 sample_id / image_path / label")
    parser.add_argument("--source-root", default=None)
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--max-new-tokens", type=int, default=128)
    args = parser.parse_args()

    # 这些 import 必须在 M2F2_Det 的代码目录可用时进行（由 PYTHONPATH 提供）
    from llava.constants import IMAGE_TOKEN_INDEX, DEEPFAKE_TOKEN_INDEX
    from llava.mm_utils import get_model_name_from_path, tokenizer_hybrid_token
    from llava.model.builder import load_deepfake_model

    project_root = find_project_root(args.source_root)
    source_root = Path(args.source_root) if args.source_root else project_root

    def resolve(value: str) -> str:
        path = Path(value)
        return str(path if path.is_absolute() else source_root / path)

    rows = read_jsonl(Path(args.manifest))
    if args.limit is not None:
        rows = rows[: args.limit]

    model_name = get_model_name_from_path(args.model_path)
    print(json.dumps({"model_name": model_name, "n": len(rows)}), flush=True)

    tokenizer, model, image_processor, context_len = load_deepfake_model(
        args.model_path, None, model_name, False, False, device="cuda"
    )
    model.eval()
    model = model.to("cuda")
    # config 里的 deepfake_model_path 是作者机器上的绝对路径，且官方未随权重发布该 .pth。
    # DenseNet121 编码器很可能已包含在 HF 的 safetensors 内（14.4G 对 7B fp16 有余量），
    # 该调用可能只是 stage-1 纯检测器流程才需要。故设为非致命，缺失时继续并在输出里标记。
    deepfake_encoder_loaded = False
    try:
        model.load_deepfake_encoder(model.config.deepfake_model_path, verbose=True)
        deepfake_encoder_loaded = True
    except FileNotFoundError as exc:
        print(json.dumps({"warning": "deepfake_encoder_ckpt_missing", "detail": str(exc)[:160]}), flush=True)
    print(json.dumps({"loaded": True, "context_len": context_len,
                      "deepfake_encoder_loaded": deepfake_encoder_loaded}), flush=True)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    handle = output.open("w", encoding="utf-8")

    for index, row in enumerate(rows, 1):
        image_path = resolve(row["image_path"])
        try:
            image = Image.open(image_path).convert("RGB")
            input_ids = tokenizer_hybrid_token(
                PROMPT, tokenizer, IMAGE_TOKEN_INDEX, DEEPFAKE_TOKEN_INDEX, return_tensors="pt"
            ).unsqueeze(0).to(model.device)
            with torch.inference_mode():
                generated = model.generate(
                    input_ids,
                    images=[image],
                    image_sizes=[image.size],
                    deepfake_inputs=[image],
                    do_sample=False,
                    num_beams=1,
                    max_new_tokens=args.max_new_tokens,
                    use_cache=True,
                    return_dict_in_generate=True,
                )
            text = tokenizer.decode(generated["sequences"][0]).strip()
            record = {
                "sample_id": row["sample_id"],
                "image_path": row["image_path"],
                "label": row.get("label"),
                "variant": row.get("variant"),
                "prompt": PROMPT,
                "raw_output": text,
            }
        except Exception as exc:
            record = {
                "sample_id": row.get("sample_id"),
                "image_path": row.get("image_path"),
                "label": row.get("label"),
                "error": f"{type(exc).__name__}: {exc}",
            }
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        handle.flush()
        if index % 10 == 0 or index == len(rows):
            print(json.dumps({"done": index, "total": len(rows), "label": row.get("label")}), flush=True)

    handle.close()
    print(json.dumps({"n": len(rows), "output": str(output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
