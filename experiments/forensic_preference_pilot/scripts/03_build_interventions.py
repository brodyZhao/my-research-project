from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

from common import read_jsonl, write_jsonl


def load_mask(path: str, size: tuple[int, int]) -> np.ndarray:
    mask = np.asarray(Image.open(path).convert("L").resize(size, Image.Resampling.NEAREST)) > 127
    if not mask.any() or mask.all():
        raise ValueError(f"invalid mask for intervention: {path}")
    return mask


def shifted_control_mask(
    target: np.ndarray,
    rng: np.random.Generator,
    forbidden: np.ndarray | None = None,
) -> np.ndarray:
    ys, xs = np.where(target)
    y0, y1 = int(ys.min()), int(ys.max()) + 1
    x0, x1 = int(xs.min()), int(xs.max()) + 1
    crop = target[y0:y1, x0:x1]
    height, width = target.shape
    positions = [(y, x) for y in range(height - crop.shape[0] + 1) for x in range(width - crop.shape[1] + 1)]
    rng.shuffle(positions)
    for new_y, new_x in positions:
        candidate = np.zeros_like(target, dtype=bool)
        candidate[new_y : new_y + crop.shape[0], new_x : new_x + crop.shape[1]] = crop
        blocked = target if forbidden is None else forbidden
        if not np.logical_and(candidate, blocked).any():
            return candidate
    raise ValueError("could not place a non-overlapping equal-shape control")


def blur_region(image: Image.Image, mask: np.ndarray) -> Image.Image:
    radius = max(4, round(min(image.size) / 40))
    feather = max(1, round(min(image.size) / 150))
    blurred = image.filter(ImageFilter.GaussianBlur(radius=radius))
    blend = Image.fromarray((mask.astype(np.uint8) * 255), mode="L").filter(
        ImageFilter.GaussianBlur(radius=feather)
    )
    return Image.composite(blurred, image, blend)


def save_mask(mask: np.ndarray, path: Path) -> None:
    Image.fromarray(mask.astype(np.uint8) * 255, mode="L").save(path)


def build_family(
    image: Image.Image,
    sample_id: str,
    label: str,
    target: np.ndarray,
    output_dir: Path,
    rng: np.random.Generator,
    num_controls: int,
) -> dict[str, str]:
    image_dir = output_dir / "images"
    mask_dir = output_dir / "masks"
    image_dir.mkdir(parents=True, exist_ok=True)
    mask_dir.mkdir(parents=True, exist_ok=True)
    target_path = image_dir / f"{sample_id}__{label}_target_blur.png"
    target_mask_path = mask_dir / f"{sample_id}__{label}_target.png"
    blur_region(image, target).save(target_path)
    save_mask(target, target_mask_path)
    paths = {
        f"{label}_target_blur": str(target_path),
        f"{label}_target_mask": str(target_mask_path),
    }
    for control_index in range(1, num_controls + 1):
        # Controls are independent paired comparisons. They must avoid the
        # target, but do not need to avoid one another; requiring mutual
        # non-overlap can make large but otherwise valid masks impossible.
        control = shifted_control_mask(target, rng, forbidden=target)
        control_path = image_dir / f"{sample_id}__{label}_control_blur_{control_index}.png"
        control_mask_path = mask_dir / f"{sample_id}__{label}_control_{control_index}.png"
        blur_region(image, control).save(control_path)
        save_mask(control, control_mask_path)
        paths[f"{label}_control_blur_{control_index}"] = str(control_path)
        paths[f"{label}_control_mask_{control_index}"] = str(control_mask_path)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Create matched Stage-A target/control blur variants")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--seed", type=int, default=20260915)
    parser.add_argument("--num-controls", type=int, default=3)
    args = parser.parse_args()

    output_dir = Path(args.output_dir) / "interventions"
    records = []
    for index, row in enumerate(read_jsonl(args.manifest)):
        sample_id = str(row["sample_id"])
        image = Image.open(row["image_path"]).convert("RGB")
        claimed = load_mask(row["claimed_mask_path"], image.size)
        rng = np.random.default_rng(args.seed + index)
        paths: dict[str, str] = {}
        original_path = output_dir / "images" / f"{sample_id}__original.png"
        noop_path = output_dir / "images" / f"{sample_id}__noop.png"
        original_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(original_path)
        image.save(noop_path)
        paths["original"] = str(original_path)
        paths["noop"] = str(noop_path)
        paths.update(build_family(image, sample_id, "claimed", claimed, output_dir, rng, args.num_controls))
        gt_path = row.get("gt_mask_path")
        gt_control_feasible = None
        gt_control_error = None
        if gt_path:
            gt = load_mask(gt_path, image.size)
            try:
                paths.update(build_family(image, sample_id, "gt", gt, output_dir, rng, args.num_controls))
                gt_control_feasible = True
            except ValueError as exc:
                # A large GT region may have no room for a matched control.
                # Keep the claimed analysis, exclude only the GT comparison,
                # and retain the explicit reason in the manifest.
                gt_control_feasible = False
                gt_control_error = str(exc)
        enriched = dict(row)
        enriched["variant_paths"] = paths
        enriched["intervention_operator"] = "gaussian_blur"
        enriched["intervention_seed"] = args.seed + index
        enriched["num_controls"] = args.num_controls
        enriched["claimed_area_ratio"] = float(claimed.mean())
        enriched["gt_area_ratio"] = float(load_mask(gt_path, image.size).mean()) if gt_path else None
        enriched["gt_control_feasible"] = gt_control_feasible
        enriched["gt_control_error"] = gt_control_error
        records.append(enriched)
        print(json.dumps({"done": index + 1, "sample_id": sample_id}), flush=True)
    write_jsonl(Path(args.output_dir) / "metadata" / "intervention_manifest.jsonl", records)
    print(json.dumps({"n": len(records), "output": str(Path(args.output_dir) / "metadata" / "intervention_manifest.jsonl")}))


if __name__ == "__main__":
    main()
