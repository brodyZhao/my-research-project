#!/usr/bin/env python3
"""落地仪器：把模型的自然语言解释转成区域（edition3 §A3.2b 方案 A）。

背景：FakeVLM 冻结的官方 prompt 只输出文字解释，没有 bbox/mask；而 Qwen3-VL 原生
输出 evidence_regions。为让两个模型的 M_claimed 定义完全一致（避免把仪器差异当成
模型差异），两者都必须走本脚本，Qwen3-VL 的原生框只作次级变体单独报告。

冻结的 query 构造规则（不得对着结果调整）：
  解释文本 → 去掉开头的 verdict 句（this is a fake/real image）
          → 小写化 → 句末补 "."
          → 整段作为 GroundingDINO 的 text query

冻结的取框规则：
  score 最高的单框；score < --threshold 记为 no_region
  面积占比 > 40% 标为 overlocalized（依 MODEL_ADAPTER_SPEC.md）

输出（相对 --out-dir）：
  masks/<sample_id>__claimed_box.png        光栅化的单框，供 restoration 构造
  grounding.jsonl                           每样本的框、分数、面积、no_region 标记
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from transformers import AutoProcessor, GroundingDinoForObjectDetection

VERDICT_PREFIX = re.compile(r"^\s*this is a[n]?\s+(?:fake|real|synthetic|authentic)\s+image\s*[.!:,]?\s*", re.IGNORECASE)
MASK_THRESHOLD = 127
OVERLOCALIZED_AREA = 0.40


def build_query(text: str) -> str:
    """按冻结规则构造 GroundingDINO 的 text query。"""
    stripped = VERDICT_PREFIX.sub("", text or "").strip()
    if not stripped:
        stripped = (text or "").strip()
    stripped = stripped.lower().rstrip()
    if not stripped.endswith("."):
        stripped = stripped + "."
    return stripped


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


def mask_iou(first: np.ndarray, second: np.ndarray) -> float:
    intersection = np.logical_and(first, second).sum()
    union = np.logical_or(first, second).sum()
    return float(intersection / union) if union else 0.0


def box_to_mask(box: tuple[float, float, float, float], size: tuple[int, int]) -> np.ndarray:
    width, height = size
    x1, y1, x2, y2 = box
    mask = np.zeros((height, width), dtype=bool)
    left = int(max(0, min(width, round(x1))))
    right = int(max(0, min(width, round(x2))))
    top = int(max(0, min(height, round(y1))))
    bottom = int(max(0, min(height, round(y2))))
    if right > left and bottom > top:
        mask[top:bottom, left:right] = True
    return mask


def mask_to_box(mask: np.ndarray) -> tuple[int, int, int, int] | None:
    ys, xs = np.where(mask)
    if not len(ys):
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Ground model explanations into regions (plan A)")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--source-root", required=True, help="解析 manifest 相对路径的根")
    parser.add_argument("--model-path", default="models/grounding-dino-tiny")
    parser.add_argument("--text-field", default="raw_output", help="存放解释文本的字段")
    parser.add_argument("--threshold", type=float, default=0.25, help="冻结的取框阈值 τ")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--save-masks", action="store_true", default=True)
    args = parser.parse_args()

    source_root = Path(args.source_root)
    out_dir = Path(args.out_dir)
    mask_dir = out_dir / "masks"
    mask_dir.mkdir(parents=True, exist_ok=True)

    processor = AutoProcessor.from_pretrained(args.model_path)
    # 无卡模式下没有 GPU，必须能退化到 CPU（GroundingDINO-tiny 在 CPU 上可跑）
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = (
        GroundingDinoForObjectDetection.from_pretrained(args.model_path, dtype=torch.float32)
        .to(device)
        .eval()
    )
    print(json.dumps({"device": str(device)}), flush=True)

    rows = read_jsonl(Path(args.manifest))
    if args.limit is not None:
        rows = rows[: args.limit]

    records = []
    for index, row in enumerate(rows, 1):
        sample_id = str(row["sample_id"])
        image_path = Path(row.get("image_path") or row["forged_path"])
        if not image_path.is_absolute():
            image_path = source_root / image_path
        image = Image.open(image_path).convert("RGB")
        width, height = image.size

        text = row.get(args.text_field) or ""
        query = build_query(text)

        inputs = processor(images=image, text=query, return_tensors="pt").to(device)
        with torch.inference_mode():
            outputs = model(**inputs)
        result = processor.post_process_grounded_object_detection(
            outputs, inputs.input_ids, threshold=args.threshold,
            text_threshold=args.threshold, target_sizes=[(height, width)],
        )[0]
        boxes = result["boxes"].cpu().numpy()
        scores = result["scores"].cpu().numpy()

        record = {
            "sample_id": sample_id,
            "dataset": row.get("dataset"),
            "split": row.get("split"),
            "method": row.get("method"),
            "label": row.get("label"),
            # 透传下游（06_build_restorations）需要的路径字段，避免额外做一次 join
            "image_path": row.get("image_path"),
            "forged_path": row.get("forged_path"),
            "pristine_path": row.get("pristine_path"),
            "gt_mask_path": row.get("gt_mask_path"),
            "query": query,
            "n_boxes": int(len(boxes)),
            "no_region": bool(len(boxes) == 0),
            "claimed_bbox": None,
            "claimed_score": None,
            "claimed_area_ratio": None,
            "overlocalized": None,
            "claimed_mask_path": None,
            "iou_box_vs_gtmask": None,
            "iou_box_vs_gtbox": None,
        }

        if len(boxes):
            best = int(np.argmax(scores))
            box = tuple(float(v) for v in boxes[best])
            box_mask = box_to_mask(box, (width, height))
            area_ratio = float(box_mask.mean())
            record.update(
                {
                    "claimed_bbox": list(box),
                    "claimed_score": float(scores[best]),
                    "claimed_area_ratio": area_ratio,
                    "overlocalized": bool(area_ratio > OVERLOCALIZED_AREA),
                }
            )
            if args.save_masks:
                mask_path = mask_dir / f"{sample_id}__claimed_box.png"
                Image.fromarray((box_mask.astype(np.uint8) * 255), mode="L").save(mask_path)
                record["claimed_mask_path"] = str(mask_path)

            gt_value = row.get("gt_mask_path")
            if gt_value:
                gt_path = Path(gt_value)
                if not gt_path.is_absolute():
                    gt_path = source_root / gt_path
                gt = np.asarray(Image.open(gt_path).convert("L")) > MASK_THRESHOLD
                if gt.shape == box_mask.shape:
                    record["iou_box_vs_gtmask"] = mask_iou(box_mask, gt)
                    gt_box = mask_to_box(gt)
                    if gt_box:
                        record["iou_box_vs_gtbox"] = mask_iou(box_mask, box_to_mask(gt_box, (width, height)))

        records.append(record)
        if index % 25 == 0:
            print(
                json.dumps(
                    {
                        "done": index,
                        "total": len(rows),
                        "no_region_so_far": sum(1 for r in records if r["no_region"]),
                    }
                ),
                flush=True,
            )

    output = out_dir / "grounding.jsonl"
    with output.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    n = len(records)
    no_region = sum(1 for r in records if r["no_region"])
    placed = [r for r in records if not r["no_region"]]
    summary = {
        "model_path": args.model_path,
        "threshold": args.threshold,
        "text_field": args.text_field,
        "n": n,
        "no_region": no_region,
        "no_region_rate": no_region / n if n else None,
        "gate6_no_region_ok": (no_region / n if n else 1.0) <= 0.30,
        "overlocalized": sum(1 for r in records if r.get("overlocalized")),
        "claimed_area_ratio": {
            "median": float(np.median([r["claimed_area_ratio"] for r in placed])) if placed else None,
            "max": float(max(r["claimed_area_ratio"] for r in placed)) if placed else None,
        },
        "iou_vs_gtmask": {
            "median": float(np.median([r["iou_box_vs_gtmask"] for r in records if r["iou_box_vs_gtmask"] is not None]))
            if any(r["iou_box_vs_gtmask"] is not None for r in records) else None,
        },
        "iou_vs_gtbox": {
            "median": float(np.median([r["iou_box_vs_gtbox"] for r in records if r["iou_box_vs_gtbox"] is not None]))
            if any(r["iou_box_vs_gtbox"] is not None for r in records) else None,
        },
        "output": str(output),
    }
    (out_dir / "grounding_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
