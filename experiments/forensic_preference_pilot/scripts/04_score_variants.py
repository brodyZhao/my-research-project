from __future__ import annotations

import argparse
import json
import math
import time
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
PREFIX = '{\n  "verdict": "'
CANDIDATES = ("real", "fake", "insufficient")


def candidate_log_likelihood(model, processor, image_path: str, candidate: str) -> float:
    messages = [{"role": "user", "content": [{"type": "image", "image": image_path}, {"type": "text", "text": PROMPT}]}]
    inputs = processor.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_dict=True, return_tensors="pt").to(model.device)
    prefix_ids = processor.tokenizer.encode(PREFIX, add_special_tokens=False)
    candidate_ids = processor.tokenizer.encode(candidate, add_special_tokens=False)
    continuation = torch.tensor([prefix_ids + candidate_ids], device=model.device, dtype=inputs["input_ids"].dtype)
    prompt_length = inputs["input_ids"].shape[1]
    model_inputs = dict(inputs)
    model_inputs["input_ids"] = torch.cat([inputs["input_ids"], continuation], dim=1)
    model_inputs["attention_mask"] = torch.cat([inputs["attention_mask"], torch.ones_like(continuation)], dim=1)
    if "mm_token_type_ids" in inputs:
        model_inputs["mm_token_type_ids"] = torch.cat([inputs["mm_token_type_ids"], torch.zeros_like(continuation)], dim=1)
    with torch.inference_mode():
        logits = model(**model_inputs).logits
    candidate_start = prompt_length + len(prefix_ids)
    prediction_logits = logits[:, candidate_start - 1 : candidate_start + len(candidate_ids) - 1, :]
    log_probs = torch.log_softmax(prediction_logits.float(), dim=-1)
    target = continuation[:, len(prefix_ids):]
    return float(log_probs.gather(2, target.unsqueeze(-1)).squeeze(-1).sum().item())


def score_image(model, processor, path: str) -> dict:
    log_likelihoods = {candidate: candidate_log_likelihood(model, processor, path, candidate) for candidate in CANDIDATES}
    maximum = max(log_likelihoods["real"], log_likelihoods["fake"])
    denominator = sum(math.exp(log_likelihoods[name] - maximum) for name in ("real", "fake"))
    p_fake = math.exp(log_likelihoods["fake"] - maximum) / denominator
    return {"p_fake": p_fake, "log_likelihoods": log_likelihoods, "log_odds_fake_real": log_likelihoods["fake"] - log_likelihoods["real"]}


def main() -> None:
    parser = argparse.ArgumentParser(description="Score locked intervention variants with forced verdict probabilities")
    parser.add_argument("--model", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--max-pixels", type=int, default=1024 * 1024)
    args = parser.parse_args()
    output = Path(args.output)
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    processor = AutoProcessor.from_pretrained(args.model, min_pixels=256 * 28 * 28, max_pixels=args.max_pixels)
    model = AutoModelForImageTextToText.from_pretrained(
        args.model, dtype=torch.bfloat16, device_map="cuda", low_cpu_mem_usage=True
    ).eval()
    for index, row in enumerate(read_jsonl(args.manifest), 1):
        paths = row["variant_paths"]
        control_names = sorted(
            name for name in paths
            if name.startswith("claimed_control_blur_") or name.startswith("gt_control_blur_")
        )
        variant_names = ["original", "noop", "claimed_target_blur", *[name for name in control_names if name.startswith("claimed_")]]
        if "gt_target_blur" in paths:
            variant_names.append("gt_target_blur")
            variant_names.extend(name for name in control_names if name.startswith("gt_"))
        missing = [name for name in variant_names if name not in paths]
        if missing:
            raise ValueError(f"{row['sample_id']} missing variants: {missing}")
        started = time.perf_counter()
        scores = {name: score_image(model, processor, paths[name]) for name in variant_names}
        result = dict(row)
        result.update({"model_path": str(args.model), "prompt": PROMPT, "scores": scores, "scoring_seconds": time.perf_counter() - started, "scored_at": datetime.now(timezone.utc).isoformat()})
        append_jsonl(output, result)
        print(json.dumps({"done": index, "sample_id": row["sample_id"], "seconds": round(result["scoring_seconds"], 2)}), flush=True)


if __name__ == "__main__":
    main()
