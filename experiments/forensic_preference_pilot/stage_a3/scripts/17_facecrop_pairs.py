#!/usr/bin/env python3
"""把 FF++ 配对裁剪成人脸特写，对齐 M2F2-Det 期望的输入格式。

## 为什么需要

M2F2-Det 的训练数据（DDVQA c40）是 **224×224 的紧贴人脸裁剪**；
而我们的 FF++ 来自 FakeClue，是 **256×256 的全景帧**（人在画面里很小）。
实测：在它的原生格式上判假率 0.64–0.94，在我们的全景帧上只有 0.326。→ 输入格式不匹配。

## 关键：真图与假图必须用【同一个框】

换脸保留背景与姿态，所以人脸位置在真/假图上一致。
用 forged 图检测出的人脸框，**同时裁 pristine**，像素对齐得以保留 ——
这是后续做逐像素恢复（restore_claimed / restore_control）的前提。

## 人脸检测器

用 GroundingDINO（本项目已装好并验证过），query = "the face."。
不引入新的检测器依赖。

输出：<out-dir>/images/<sample_id>__{forged,pristine}.jpg （224×224），以及裁剪清单。
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path

import numpy as np
import torch
from PIL import Image

SCRIPTS_DIR = Path(__file__).resolve().parent


def _load_sibling(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_build = _load_sibling("06_build_restorations")
find_project_root = _build.find_project_root

PROJECT_ROOT = find_project_root(os.environ.get("FAITHPILOT_PROJECT_ROOT"))
sys.path.insert(0, str(PROJECT_ROOT))

OUTPUT_SIZE = 224
MARGIN = 0.35  # 人脸框外扩比例，让裁剪包含发际/下巴，接近 FF++ 的标准人脸裁剪


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


def square_box(box: tuple[float, float, float, float], size: tuple[int, int], margin: float):
    """把人脸框扩成正方形并加上边距，裁到图像范围内。"""
    width, height = size
    x1, y1, x2, y2 = box
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    side = max(x2 - x1, y2 - y1) * (1 + margin)
    half = side / 2
    left = max(0, int(round(cx - half)))
    top = max(0, int(round(cy - half)))
    right = min(width, int(round(cx + half)))
    bottom = min(height, int(round(cy + half)))
    # 若贴边导致非正方形，向内平移
    side_px = min(right - left, bottom - top)
    if right - left > side_px:
        left = min(left, width - side_px)
        right = left + side_px
    if bottom - top > side_px:
        top = min(top, height - side_px)
        bottom = top + side_px
    return left, top, right, bottom


def main() -> None:
    parser = argparse.ArgumentParser(description="Face-crop FF++ pairs for M2F2-Det input format")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--model-path", default="models/grounding-dino-tiny")
    parser.add_argument("--query", default="the face.")
    parser.add_argument("--threshold", type=float, default=0.25)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    from transformers import AutoProcessor, GroundingDinoForObjectDetection

    source_root = Path(args.source_root)
    out_dir = Path(args.out_dir)
    image_dir = out_dir / "images"
    image_dir.mkdir(parents=True, exist_ok=True)

    def resolve(value: str) -> Path:
        path = Path(value)
        return path if path.is_absolute() else source_root / path

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    processor = AutoProcessor.from_pretrained(str(resolve(args.model_path)))
    detector = (
        GroundingDinoForObjectDetection.from_pretrained(str(resolve(args.model_path)), dtype=torch.float32)
        .to(device)
        .eval()
    )

    rows = [row for row in read_jsonl(resolve(args.manifest)) if not row.get("error")]
    if args.limit is not None:
        rows = rows[: args.limit]

    records = []
    for index, row in enumerate(rows, 1):
        sample_id = row["sample_id"]
        variants = row.get("variant_paths") or {}
        forged_path = variants.get("original")
        pristine_path = variants.get("whole")
        if not forged_path or not pristine_path:
            records.append({"sample_id": sample_id, "error": "missing_original_or_whole"})
            continue

        forged = Image.open(resolve(forged_path)).convert("RGB")
        pristine = Image.open(resolve(pristine_path)).convert("RGB")

        inputs = processor(images=forged, text=args.query, return_tensors="pt").to(device)
        with torch.inference_mode():
            outputs = detector(**inputs)
        result = processor.post_process_grounded_object_detection(
            outputs, inputs.input_ids, threshold=args.threshold, text_threshold=args.threshold,
            target_sizes=[(forged.height, forged.width)],
        )[0]
        boxes = result["boxes"].cpu().numpy()
        scores = result["scores"].cpu().numpy()
        if not len(boxes):
            records.append({"sample_id": sample_id, "error": "no_face_detected"})
            continue
        best = boxes[int(np.argmax(scores))]
        crop = square_box(tuple(float(v) for v in best), forged.size, MARGIN)
        if crop[2] - crop[0] < 16 or crop[3] - crop[1] < 16:
            records.append({"sample_id": sample_id, "error": f"degenerate_crop:{crop}"})
            continue

        forged_crop = forged.crop(crop).resize((OUTPUT_SIZE, OUTPUT_SIZE), Image.Resampling.BICUBIC)
        pristine_crop = pristine.crop(crop).resize((OUTPUT_SIZE, OUTPUT_SIZE), Image.Resampling.BICUBIC)
        forged_out = image_dir / f"{sample_id}__forged.jpg"
        pristine_out = image_dir / f"{sample_id}__pristine.jpg"
        forged_crop.save(forged_out, quality=95)
        pristine_crop.save(pristine_out, quality=95)

        records.append(
            {
                "sample_id": sample_id,
                "dataset": row.get("dataset"),
                "method": row.get("method"),
                "forged_crop": str(forged_out),
                "pristine_crop": str(pristine_out),
                "face_box": [float(v) for v in best],
                "face_score": float(scores[int(np.argmax(scores))]),
                "crop_box": list(crop),
                "error": None,
            }
        )
        if index % 25 == 0:
            print(json.dumps({"done": index, "total": len(rows)}), flush=True)

    output = out_dir / "facecrop_manifest.jsonl"
    with output.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    valid = [r for r in records if not r.get("error")]
    counts: dict[str, int] = {}
    for record in records:
        if record.get("error"):
            key = str(record["error"]).split(":")[0]
            counts[key] = counts.get(key, 0) + 1
    summary = {
        "n": len(records), "n_valid": len(valid),
        "output_size": OUTPUT_SIZE, "margin": MARGIN, "query": args.query,
        "error_counts": counts, "output": str(output),
    }
    (out_dir / "facecrop_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
