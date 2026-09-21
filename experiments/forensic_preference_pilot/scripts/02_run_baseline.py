from __future__ import annotations

import argparse
import json
import re
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

import torch
from transformers import AutoModelForImageTextToText, AutoProcessor

from common import append_jsonl, read_jsonl


PROMPT = """You are a forensic image analyst. Decide whether the image is real or fake.
Return exactly one JSON object with keys verdict, rationale, and evidence_regions.
verdict must be real, fake, or insufficient. rationale must be a short reason tied to
visible evidence. evidence_regions must contain one object with bbox [x1,y1,x2,y2]
normalized to 0..1000 and an evidence string when verdict is real or fake. Use an
empty evidence_regions list for insufficient. Do not use markdown fences or text outside JSON."""


def parse_json(text: str) -> tuple[dict | None, str | None]:
    match = re.search(r"\{.*\}", text.strip(), flags=re.DOTALL)
    if not match:
        return None, "no_json_object"
    try:
        value = json.loads(match.group(0))
    except json.JSONDecodeError as exc:
        return None, f"json_decode:{exc.msg}"
    return value if isinstance(value, dict) else None, None


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the fixed forensic prompt on original images")
    parser.add_argument("--model", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--max-pixels", type=int, default=1024 * 1024)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    output = Path(args.output)
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    processor = AutoProcessor.from_pretrained(args.model, min_pixels=256 * 28 * 28, max_pixels=args.max_pixels)
    model = AutoModelForImageTextToText.from_pretrained(
        args.model, dtype=torch.bfloat16, device_map="cuda", low_cpu_mem_usage=True
    ).eval()
    rows = read_jsonl(args.manifest)
    end = None if args.limit is None else args.start + args.limit
    selected = rows[args.start:end]
    for offset, row in enumerate(selected, args.start + 1):
        try:
            messages = [{"role": "user", "content": [{"type": "image", "image": row["image_path"]}, {"type": "text", "text": PROMPT}]}]
            started = time.perf_counter()
            inputs = processor.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_dict=True, return_tensors="pt").to(model.device)
            with torch.inference_mode():
                generated = model.generate(**inputs, max_new_tokens=256, do_sample=False)
            prompt_length = inputs["input_ids"].shape[1]
            raw = processor.batch_decode(generated[:, prompt_length:], skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
            parsed, error = parse_json(raw)
            append_jsonl(output, {
                "sample_id": str(row["sample_id"]),
                "image_path": row["image_path"],
                "model_path": str(args.model),
                "prompt": PROMPT,
                "raw_output": raw,
                "parsed_output": parsed,
                "parse_status": "ok" if parsed is not None else "failed",
                "parse_error": error,
                "generation_seconds": time.perf_counter() - started,
                "generated_at": datetime.now(timezone.utc).isoformat(),
            })
            print(json.dumps({"done": offset, "sample_id": row["sample_id"], "parse_status": "ok" if parsed is not None else "failed"}), flush=True)
            del inputs, generated
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except Exception as exc:
            failure = {
                "sample_id": str(row.get("sample_id")),
                "image_path": row.get("image_path"),
                "sample_index": offset - 1,
                "error_type": type(exc).__name__,
                "error": str(exc),
                "traceback": traceback.format_exc(),
            }
            append_jsonl(str(output) + ".failures.jsonl", failure)
            print(json.dumps(failure, ensure_ascii=False), flush=True)
            raise


if __name__ == "__main__":
    main()
