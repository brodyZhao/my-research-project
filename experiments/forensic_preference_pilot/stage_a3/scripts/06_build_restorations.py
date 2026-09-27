#!/usr/bin/env python3
"""构造反事实恢复图（edition3 §A3.3 / §A3.5）。

恢复算子：**直接像素替换**（协议 §8 要求优先于 blur / inpainting）
    x_restore(E) = forged * (1 - M_E) + pristine * M_E

每个样本生成以下变体：

  original       篡改图副本（Variant 0）
  noop           与 original 逐像素相同 —— 用于测打分管线的噪声底
  restore_claimed 恢复模型声称区域
  restore_control_{i}  恢复第 i 个匹配对照区域（i = 1..K）
  whole          pristine 原图本身（§A3.5 全图对照）
  suff_claimed   把声称区域从伪造图注入原图（充分性 / 阳性对照）

对照区选取复用 `faithpilot.control_matching` 的**冻结 DINOv2 特征打分**：
    score = cosine(target_feat, cand_feat) - appearance_weight * ||target_app - cand_app||
候选必须与 target 等形状且不与 target（及其膨胀）重叠。
原函数只返回最优的一个，这里扩展为取 top-K 个**互不重叠**的对照：
选完一个就把它（膨胀后）并入 forbidden，再选下一个。

⚠️ 需要 GPU 吗：不需要。DINOv2-small 在 CPU 上即可（88MB 权重）。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModel

def find_project_root(explicit: str | None) -> Path:
    """定位含 faithpilot 包的项目根。

    不要硬编码 parents[N]：本脚本在本地仓库与远程主机上的目录深度不同
    （远程是 <root>/stage_a3/scripts/，本地是
    <repo>/experiments/forensic_preference_pilot/stage_a3/scripts/），
    数错一层就会 ModuleNotFoundError。改为向上搜索特征目录。
    """
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

from faithpilot.control_matching import (  # noqa: E402
    _appearance,
    _appearance_maps,
    _bbox,
    _candidate_masks,
    _pool_feature,
    dilate_mask,
)

MASK_THRESHOLD = 127
# 与 prepare_strict_interventions.py 保持一致的常数，便于对照
APPEARANCE_WEIGHT = 0.15
MAX_CANDIDATES = 800


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


def load_mask(path: Path, size: tuple[int, int]) -> np.ndarray:
    mask = np.asarray(Image.open(path).convert("L").resize(size, Image.Resampling.NEAREST)) > MASK_THRESHOLD
    if not mask.any():
        raise ValueError(f"掩码为空: {path}")
    return mask


def build_feature_map(processor, model, image: Image.Image, device) -> np.ndarray:
    inputs = processor(images=image, return_tensors="pt")
    inputs = {key: value.to(device) for key, value in inputs.items()}
    with torch.inference_mode():
        tokens = model(**inputs).last_hidden_state[:, 1:, :]
    patch_count = tokens.shape[1]
    side = round(patch_count**0.5)
    if side * side != patch_count:
        raise ValueError(f"DINO patch 数异常: {patch_count}")
    return tokens[0].reshape(side, side, -1).float().cpu().numpy()


def semantic_controls(
    image: Image.Image,
    target: np.ndarray,
    feature: np.ndarray,
    exclusion_radius: int,
    k: int,
) -> list[dict]:
    """取 top-K 个互不重叠的语义匹配对照，打分公式与 faithpilot 完全一致。"""
    forbidden = dilate_mask(target, exclusion_radius)
    x0, y0, x1, y1 = _bbox(target)
    dense_stride = max(4, min(x1 - x0, y1 - y0) // 4)
    bounded_stride = int(np.ceil(np.sqrt(target.size / max(MAX_CANDIDATES, 1))))
    stride = max(dense_stride, bounded_stride)

    target_feature = _pool_feature(feature, target)
    target_feature = target_feature / max(float(np.linalg.norm(target_feature)), 1e-12)
    image_array = np.asarray(image.convert("RGB"))
    rgb, edge_map = _appearance_maps(image_array)
    target_appearance = _appearance(rgb, edge_map, target)

    selected: list[dict] = []
    for _ in range(k):
        best = None
        count = 0
        for candidate, offset in _candidate_masks(target, forbidden, stride):
            count += 1
            candidate_feature = _pool_feature(feature, candidate)
            candidate_feature = candidate_feature / max(float(np.linalg.norm(candidate_feature)), 1e-12)
            cosine = float(np.dot(target_feature, candidate_feature))
            appearance_distance = float(
                np.linalg.norm(target_appearance - _appearance(rgb, edge_map, candidate))
            )
            score = cosine - APPEARANCE_WEIGHT * appearance_distance
            if best is None or score > best["score"]:
                best = {
                    "score": score,
                    "mask": candidate,
                    "cosine_similarity": cosine,
                    "appearance_distance": appearance_distance,
                    "offset_xy": list(offset),
                    "candidate_count": count,
                }
        if best is None:
            break
        selected.append(best)
        forbidden = np.logical_or(forbidden, dilate_mask(best["mask"], exclusion_radius))
    return selected


def restore(forged: np.ndarray, pristine: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """直接像素替换：mask 内取 pristine，mask 外取 forged。"""
    result = forged.copy()
    result[mask] = pristine[mask]
    return result


def inject(pristine: np.ndarray, forged: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """充分性方向：把 mask 内的伪造内容注入原图。"""
    result = pristine.copy()
    result[mask] = forged[mask]
    return result


def mask_to_box(mask: np.ndarray) -> tuple[int, int, int, int]:
    return _bbox(mask)


def iou(first: np.ndarray, second: np.ndarray) -> float:
    union = np.logical_or(first, second).sum()
    return float(np.logical_and(first, second).sum() / union) if union else 0.0


def box_mask(box: tuple[int, int, int, int], shape: tuple[int, int]) -> np.ndarray:
    x0, y0, x1, y1 = box
    mask = np.zeros(shape, dtype=bool)
    mask[y0:y1, x0:x1] = True
    return mask


def main() -> None:
    parser = argparse.ArgumentParser(description="Build counterfactual restoration variants")
    parser.add_argument("--manifest", required=True, help="含 forged_path / pristine_path")
    parser.add_argument(
        "--grounding",
        default=None,
        help="05 的输出；按 sample_id join 拿到 claimed_mask_path。"
        "不传则要求 manifest 自带 claimed_mask_path",
    )
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--num-controls", type=int, default=3)
    parser.add_argument("--dino-model", default="models/dinov2-small")
    parser.add_argument("--context-radius-ratio", type=float, default=0.02)
    parser.add_argument("--gt-jsonl", default=None, help="可选：sample_id -> gt_mask_path 的映射表")
    parser.add_argument(
        "--threads",
        type=int,
        default=8,
        help="torch CPU 线程数。默认压到 8：128 核机器上不限制会线程爆炸导致挂死",
    )
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    source_root = Path(args.source_root)
    out_dir = Path(args.out_dir)
    image_dir = out_dir / "images"
    mask_dir = out_dir / "masks"
    for directory in (image_dir, mask_dir):
        directory.mkdir(parents=True, exist_ok=True)

    def resolve(value: str) -> Path:
        path = Path(value)
        return path if path.is_absolute() else source_root / path

    gt_lookup: dict[str, str] = {}
    if args.gt_jsonl:
        for row in read_jsonl(resolve(args.gt_jsonl)):
            if row.get("gt_mask_path") and not row.get("error"):
                gt_lookup[str(row["sample_id"])] = row["gt_mask_path"]

    # 05 的输出只有 sample_id + claimed_mask_path，用 join 拿过来即可，
    # 不必为了补字段重跑一遍推理（CPU 上 GroundingDINO 跑不动）
    claimed_lookup: dict[str, str] = {}
    if args.grounding:
        for row in read_jsonl(resolve(args.grounding)):
            if row.get("claimed_mask_path"):
                claimed_lookup[str(row["sample_id"])] = row["claimed_mask_path"]

    torch.set_num_threads(args.threads)
    device = torch.device("cpu")
    processor = AutoImageProcessor.from_pretrained(resolve(args.dino_model))
    dinov2 = AutoModel.from_pretrained(resolve(args.dino_model)).eval().to(device)

    rows = read_jsonl(resolve(args.manifest))
    if args.limit is not None:
        rows = rows[: args.limit]

    records = []
    for index, row in enumerate(rows, 1):
        sample_id = str(row["sample_id"])
        forged_path, pristine_path = resolve(row["forged_path"]), resolve(row["pristine_path"])
        claimed_value = row.get("claimed_mask_path") or claimed_lookup.get(sample_id)
        if not claimed_value:
            records.append({"sample_id": sample_id, "error": "no_claimed_mask"})
            continue
        claimed_path = resolve(claimed_value)

        forged_image = Image.open(forged_path).convert("RGB")
        pristine_image = Image.open(pristine_path).convert("RGB")
        forged = np.asarray(forged_image)
        pristine = np.asarray(pristine_image)
        if forged.shape != pristine.shape:
            records.append({"sample_id": sample_id, "error": "size_mismatch"})
            continue

        claimed = load_mask(claimed_path, forged_image.size)
        radius = max(1, round(min(forged_image.size) * args.context_radius_ratio))
        feature = build_feature_map(processor, dinov2, forged_image, device)
        controls = semantic_controls(forged_image, claimed, feature, radius, args.num_controls)
        if not controls:
            records.append({"sample_id": sample_id, "error": "no_control_found"})
            continue

        paths = {}
        Image.fromarray(forged).save(image_dir / f"{sample_id}__original.png")
        Image.fromarray(forged).save(image_dir / f"{sample_id}__noop.png")
        Image.fromarray(pristine).save(image_dir / f"{sample_id}__whole.png")
        paths["original"] = f"images/{sample_id}__original.png"
        paths["noop"] = f"images/{sample_id}__noop.png"
        paths["whole"] = f"images/{sample_id}__whole.png"

        Image.fromarray(restore(forged, pristine, claimed)).save(
            image_dir / f"{sample_id}__restore_claimed.png"
        )
        Image.fromarray((claimed.astype(np.uint8) * 255), mode="L").save(
            mask_dir / f"{sample_id}__claimed.png"
        )
        paths["restore_claimed"] = f"images/{sample_id}__restore_claimed.png"

        Image.fromarray(inject(pristine, forged, claimed)).save(
            image_dir / f"{sample_id}__suff_claimed.png"
        )
        paths["suff_claimed"] = f"images/{sample_id}__suff_claimed.png"

        control_areas = []
        for control_index, control in enumerate(controls, 1):
            control_mask = control["mask"]
            control_areas.append(float(control_mask.mean()))
            Image.fromarray(restore(forged, pristine, control_mask)).save(
                image_dir / f"{sample_id}__restore_control_{control_index}.png"
            )
            Image.fromarray((control_mask.astype(np.uint8) * 255), mode="L").save(
                mask_dir / f"{sample_id}__control_{control_index}.png"
            )
            paths[f"restore_control_{control_index}"] = (
                f"images/{sample_id}__restore_control_{control_index}.png"
            )

        record = {
            "sample_id": sample_id,
            "dataset": row.get("dataset"),
            "split": row.get("split"),
            "method": row.get("method"),
            "variant_paths": {key: str(out_dir / value) for key, value in paths.items()},
            "claimed_mask_path": str(mask_dir / f"{sample_id}__claimed.png"),
            "num_controls": len(controls),
            "claimed_area_ratio": float(claimed.mean()),
            "control_area_ratios": control_areas,
            "control_area_mean": float(np.mean(control_areas)),
            "control_cosine": [round(c["cosine_similarity"], 4) for c in controls],
            "context_radius": radius,
            "error": None,
        }

        gt_value = gt_lookup.get(sample_id)
        if gt_value:
            gt = load_mask(resolve(gt_value), forged_image.size)
            record["gt_mask_path"] = gt_value
            record["gt_mask_source"] = "derived_from_diff"
            record["gt_area_ratio"] = float(gt.mean())
            record["iou_claimed_vs_gtmask"] = iou(claimed, gt)
            record["iou_claimed_vs_gtbox"] = iou(
                claimed, box_mask(mask_to_box(gt), claimed.shape)
            )

        records.append(record)
        if index % 25 == 0:
            print(json.dumps({"done": index, "total": len(rows)}), flush=True)

    output = out_dir / "restorations.jsonl"
    with output.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    valid = [r for r in records if not r.get("error")]
    areas = np.asarray([r["claimed_area_ratio"] for r in valid]) if valid else np.asarray([0.0])
    ious = [r["iou_claimed_vs_gtmask"] for r in valid if r.get("iou_claimed_vs_gtmask") is not None]
    summary = {
        "n": len(records),
        "n_valid": len(valid),
        "num_controls": args.num_controls,
        "claimed_area_ratio": {
            "min": float(areas.min()),
            "median": float(np.median(areas)),
            "max": float(areas.max()),
        },
        "iou_claimed_vs_gtmask_median": float(np.median(ious)) if ious else None,
        "mean_control_area_delta": float(
            np.mean([abs(r["claimed_area_ratio"] - r["control_area_mean"]) for r in valid])
        ) if valid else None,
        "output": str(output),
    }
    (out_dir / "restorations_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
