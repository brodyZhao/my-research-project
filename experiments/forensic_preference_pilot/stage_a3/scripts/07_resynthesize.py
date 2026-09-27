#!/usr/bin/env python3
"""反事实重合成算子：用扩散 inpainting 重新生成指定区域（本方案的核心仪器）。

## 为什么必须换掉旧算子

| 旧算子 | 实际行为 | 后果 |
|---|---|---|
| Gaussian blur | 往区域里**加入** blur artifact | edition1 实证 `delta_gt < 0` 达 54/80 |
| 黑块遮挡 | 引入 OOD 遮挡，测试的是"模型对黑块的反应" | 两个算子都不成立 |

而 `x_restore(E) = forged·(1−M) + pristine·M` 需要 pristine —— 纯 AI 生成图
（SynthScars / GenImage）**原理上没有**。这正是本项目此前卡死的根因。

## 本算子的定义

    x_resynth(E) = Inpaint(x_forged, mask=M_E, prompt=P_frozen)
    以图像其余部分为条件，重新生成 E 区域 → E 内的伪迹被"重写掉"
    不需要 pristine

算子自伪影（生成模型自身纹理特征）在目标区 E 与**等面积语义匹配对照** E′ 上同量出现，
由 specificity gap = Δs(E) − Δs(E′) 抵消。这是算子成立的前提，必须按 Phase 1.2 验证。

## 冻结的算子参数（不得对着结果调整）

    prompt = ""（空，最中性，不注入语义内容）
    negative_prompt = ""
    steps / guidance / seed 见命令行默认值，运行后写入 resynthesis.jsonl

## claimed 区域来源

SynthScars 的 baseline 由 Qwen3-VL 产出，**原生带 evidence_regions[].bbox**（归一化 0-1000），
直接光栅化即可，无需 GroundingDINO。
（若日后加入 FakeVLM 这类只输出文字的模型，两个模型必须走同一落地流程以保证可比性。）
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
    """按路径加载同目录脚本（文件名以数字开头，不能用常规 import）。"""
    path = SCRIPTS_DIR / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_build = _load_sibling("06_build_restorations")
find_project_root = _build.find_project_root
read_jsonl = _build.read_jsonl
load_mask = _build.load_mask
build_feature_map = _build.build_feature_map
semantic_controls = _build.semantic_controls
mask_to_box = _build.mask_to_box

PROJECT_ROOT = find_project_root(os.environ.get("FAITHPILOT_PROJECT_ROOT"))
sys.path.insert(0, str(PROJECT_ROOT))

from faithpilot.evidence import normalized_regions_to_mask  # noqa: E402

MASK_THRESHOLD = 127


def rasterize_claimed(image_size: tuple[int, int], parsed_output: dict) -> np.ndarray:
    """把 Qwen3-VL 的原生 evidence_regions 光栅化成掩码。

    复用 faithpilot.evidence.normalized_regions_to_mask（既有实现，勿重写）。
    """
    regions = (parsed_output or {}).get("evidence_regions") or []
    if not regions:
        raise ValueError("parsed_output 里没有 evidence_regions")
    mask_image = normalized_regions_to_mask(image_size, regions)
    mask = np.asarray(mask_image.convert("L")) > MASK_THRESHOLD
    if not mask.any():
        raise ValueError("光栅化后掩码为空")
    return mask


def random_region(shape: tuple[int, int], area: float, rng: np.random.Generator) -> np.ndarray:
    """生成与目标等面积的随机矩形区域（额外对照，测算子的一般效应）。"""
    height, width = shape
    box_area = max(1, int(round(area * height * width)))
    side = max(1, int(round(box_area**0.5)))
    side = min(side, height, width)
    top = int(rng.integers(0, max(1, height - side + 1)))
    left = int(rng.integers(0, max(1, width - side + 1)))
    mask = np.zeros(shape, dtype=bool)
    mask[top : top + side, left : left + side] = True
    return mask


def equal_area_rect(
    target: np.ndarray, forbidden: np.ndarray, rng: np.random.Generator, attempts: int = 200
) -> np.ndarray | None:
    """降级对照：与 target 面积相等的正方形，随机放置在非重叠位置。

    仅当语义匹配对照（faithpilot.control_matching）找不到可行解时使用。
    来源会被记录为 fallback_random_rect，分析时必须分层报告，不得与语义对照混算。
    """
    height, width = target.shape
    side = max(1, int(round(float(target.mean()) * height * width) ** 0.5))
    side = min(side, height, width)
    for _ in range(attempts):
        top = int(rng.integers(0, max(1, height - side + 1)))
        left = int(rng.integers(0, max(1, width - side + 1)))
        mask = np.zeros(target.shape, dtype=bool)
        mask[top : top + side, left : left + side] = True
        if not np.logical_and(mask, forbidden).any():
            return mask
    return None


def _pad_to_multiple(
    image: Image.Image, mask: np.ndarray, multiple: int = 8
) -> tuple[Image.Image, np.ndarray, tuple[int, int]]:
    """SDXL 要求高宽能被 8 整除；SynthScars 有 450x450 的图。

    做法：右侧/下侧 padding 到 8 的倍数 → inpaint → 结果裁回原尺寸。
    `original` 变体不经过这条路径，保持原图不动，故原图与变体的差异只来自区域重绘。
    ⚠️ 贴边的区域会受 padding 影响，分析时对贴边样本单独标记。
    """
    width, height = image.size
    padded_width = ((width + multiple - 1) // multiple) * multiple
    padded_height = ((height + multiple - 1) // multiple) * multiple
    if (padded_width, padded_height) == (width, height):
        return image, mask, (width, height)
    padded_image = Image.new("RGB", (padded_width, padded_height))
    padded_image.paste(image, (0, 0))
    padded_mask = np.zeros((padded_height, padded_width), dtype=bool)
    padded_mask[:height, :width] = mask
    return padded_image, padded_mask, (width, height)


def run_inpaint(pipe, image: Image.Image, mask: np.ndarray, args):
    """对一个区域执行重合成。返回原始尺寸的 PIL Image。

    mask 白区 = 需要重绘的区域。
    """
    working_image, working_mask, original_size = _pad_to_multiple(image, mask)
    mask_image = Image.fromarray((working_mask.astype(np.uint8) * 255), mode="L").convert("RGB")
    generator = torch.Generator(device=args.device).manual_seed(args.seed)
    result = pipe(
        prompt=args.prompt,
        negative_prompt=args.negative_prompt,
        image=working_image,
        mask_image=mask_image,
        num_inference_steps=args.steps,
        guidance_scale=args.guidance,
        generator=generator,
        height=working_image.height,
        width=working_image.width,
    ).images[0]
    return result.crop((0, 0, original_size[0], original_size[1]))


def save_crop(image: Image.Image, mask: np.ndarray, path: Path, pad_ratio: float = 0.5) -> None:
    """保存区域附近的裁剪（含边界上下文），供盲审判断"伪迹是否被移除/有无接缝"。"""
    x0, y0, x1, y1 = mask_to_box(mask)
    pad_x = int((x1 - x0) * pad_ratio)
    pad_y = int((y1 - y0) * pad_ratio)
    left = max(0, x0 - pad_x)
    top = max(0, y0 - pad_y)
    right = min(image.width, x1 + pad_x)
    bottom = min(image.height, y1 + pad_y)
    image.crop((left, top, right, bottom)).save(path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Counterfactual re-synthesis operator")
    parser.add_argument("--generations", required=True, help="Qwen3-VL 输出（含 parsed_output.evidence_regions）")
    parser.add_argument("--candidates", required=True, help="candidate_manifest.jsonl（含 image_path 与 GT 掩码）")
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--model", default="diffusers/stable-diffusion-xl-1.0-inpainting-0.1")
    parser.add_argument(
        "--variant",
        default="fp16",
        help="权重变体。只下了 fp16 权重时必须显式指定，否则 diffusers 会去找 "
        "diffusion_pytorch_model.safetensors 而报 OSError。留空字符串表示用默认权重。",
    )
    parser.add_argument("--num-controls", type=int, default=3)
    parser.add_argument("--context-radius-ratio", type=float, default=0.02)
    parser.add_argument("--steps", type=int, default=30)
    parser.add_argument("--guidance", type=float, default=7.5)
    parser.add_argument("--prompt", default="")
    parser.add_argument("--negative-prompt", default="")
    parser.add_argument("--seed", type=int, default=20260921)
    parser.add_argument("--dino-model", default="models/dinov2-small")
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    if args.device == "cuda" and not torch.cuda.is_available():
        raise SystemExit(
            "没有可用 GPU。扩散 inpainting 在 CPU 上不可行 —— "
            "请把实例切到有卡模式后重跑。"
        )

    source_root = Path(args.source_root)
    out_dir = Path(args.out_dir)
    for name in ("images", "masks", "crops_before", "crops_after"):
        (out_dir / name).mkdir(parents=True, exist_ok=True)

    def resolve(value: str) -> Path:
        path = Path(value)
        return path if path.is_absolute() else source_root / path

    # 生成结果按 sample_id 索引
    gen_by_id = {str(row["sample_id"]): row for row in read_jsonl(resolve(args.generations))}
    candidates = read_jsonl(resolve(args.candidates))
    if args.limit is not None:
        candidates = candidates[: args.limit]

    from diffusers import AutoPipelineForInpainting  # 延迟导入，避免无 GPU 时的额外开销

    dtype = torch.float16 if args.device == "cuda" else torch.float32
    load_kwargs: dict = {"torch_dtype": dtype}
    if args.variant:
        load_kwargs["variant"] = args.variant
    pipe = AutoPipelineForInpainting.from_pretrained(args.model, **load_kwargs)
    pipe = pipe.to(args.device)
    pipe.set_progress_bar_config(disable=True)

    dino_processor = _build.AutoImageProcessor.from_pretrained(resolve(args.dino_model))
    dino_model = _build.AutoModel.from_pretrained(resolve(args.dino_model)).eval().to("cpu")

    records = []
    # 增量落盘：40 分钟的长任务若中途异常，不能把已完成的成果一起丢掉
    output = out_dir / "resynthesis.jsonl"
    output_handle = output.open("w", encoding="utf-8")

    for index, candidate in enumerate(candidates, 1):
        sample_id = str(candidate["sample_id"])
        generation = gen_by_id.get(sample_id)
        if generation is None or generation.get("parse_status") != "ok":
            records.append({"sample_id": sample_id, "error": "no_parsed_generation"})
            continue

        image_path = resolve(candidate["image_path"])
        image = Image.open(image_path).convert("RGB")
        try:
            claimed = rasterize_claimed(image.size, generation.get("parsed_output") or {})
        except ValueError as exc:
            records.append({"sample_id": sample_id, "error": f"claimed:{exc}"})
            continue

        radius = max(1, round(min(image.size) * args.context_radius_ratio))
        feature = build_feature_map(dino_processor, dino_model, image, torch.device("cpu"))
        controls = semantic_controls(image, claimed, feature, radius, args.num_controls)
        control_source = "semantic_matched"
        if not controls:
            # 降级：等面积矩形对照。来源会记录，分析时分层，不与语义对照混算。
            fallback = []
            forbidden = _build.dilate_mask(claimed, radius)
            fallback_rng = np.random.default_rng(args.seed)
            for _ in range(args.num_controls):
                mask = equal_area_rect(claimed, forbidden, fallback_rng)
                if mask is None:
                    break
                fallback.append(
                    {
                        "mask": mask,
                        "cosine_similarity": float("nan"),
                        "appearance_distance": float("nan"),
                        "offset_xy": [0, 0],
                        "candidate_count": 0,
                    }
                )
                forbidden = np.logical_or(forbidden, mask)
            controls = fallback
            control_source = "fallback_random_rect" if controls else "none"
        if not controls:
            records.append({"sample_id": sample_id, "error": "no_control"})
            continue

        claimed_area = float(claimed.mean())
        rng = np.random.default_rng(args.seed)
        regions: dict[str, np.ndarray] = {"claimed": claimed}
        for control_index, control in enumerate(controls, 1):
            regions[f"control_{control_index}"] = control["mask"]
        regions["random"] = random_region(claimed.shape, claimed_area, rng)

        gt_value = candidate.get("evidence_mask_path") or candidate.get("gt_mask_path")
        gt_mask = None
        if gt_value:
            try:
                gt_mask = load_mask(resolve(gt_value), image.size)
                regions["gt"] = gt_mask
            except Exception:
                gt_mask = None

        paths: dict[str, str] = {}
        for region_name, region_mask in regions.items():
            mask_path = out_dir / "masks" / f"{sample_id}__{region_name}.png"
            Image.fromarray((region_mask.astype(np.uint8) * 255), mode="L").save(mask_path)
            save_crop(image, region_mask, out_dir / "crops_before" / f"{sample_id}__{region_name}.png")

            result = run_inpaint(pipe, image, region_mask, args)
            image_out = out_dir / "images" / f"{sample_id}__resynth_{region_name}.png"
            result.save(image_out)
            save_crop(result, region_mask, out_dir / "crops_after" / f"{sample_id}__{region_name}.png")
            paths[f"resynth_{region_name}"] = str(image_out)

        # 未改动副本，供打分的 noop 噪声底
        original_out = out_dir / "images" / f"{sample_id}__original.png"
        image.save(original_out)
        paths["original"] = str(original_out)

        record = {
            "sample_id": sample_id,
            "dataset": candidate.get("source"),
            "image_path": candidate["image_path"],
            "variant_paths": paths,
            "claimed_area_ratio": claimed_area,
            "control_source": control_source,
            "control_areas": [float(c["mask"].mean()) for c in controls],
            "control_cosine": [round(c["cosine_similarity"], 4) for c in controls],
            "gt_area_ratio": float(gt_mask.mean()) if gt_mask is not None else None,
            "operator": {
                "model": args.model,
                "prompt": args.prompt,
                "negative_prompt": args.negative_prompt,
                "steps": args.steps,
                "guidance": args.guidance,
                "seed": args.seed,
            },
            "error": None,
        }
        records.append(record)
        output_handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        output_handle.flush()
        print(json.dumps({"done": index, "total": len(candidates), "sample_id": sample_id}), flush=True)

    output_handle.close()
    # 末尾重写一次完整清单，把错误行也纳入
    with output.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    valid = [r for r in records if not r.get("error")]
    summary = {
        "n": len(records),
        "n_valid": len(valid),
        "operator": {"model": args.model, "steps": args.steps, "guidance": args.guidance,
                     "seed": args.seed, "prompt": args.prompt},
        "num_controls": args.num_controls,
        "claimed_area_ratio_median": float(np.median([r["claimed_area_ratio"] for r in valid])) if valid else None,
        "mean_control_area_delta": float(
            np.mean([abs(r["claimed_area_ratio"] - float(np.mean(r["control_areas"]))) for r in valid])
        ) if valid else None,
        "error_counts": {},
        "output": str(output),
    }
    counts: dict[str, int] = {}
    for record in records:
        if record.get("error"):
            key = str(record["error"]).split(":")[0]
            counts[key] = counts.get(key, 0) + 1
    summary["error_counts"] = counts

    # 对照来源分布：语义匹配 vs 降级矩形。分析时必须分层，不得混算。
    source_counts: dict[str, int] = {}
    for record in valid:
        key = str(record.get("control_source", "unknown"))
        source_counts[key] = source_counts.get(key, 0) + 1
    summary["control_source_counts"] = source_counts
    (out_dir / "resynthesis_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
