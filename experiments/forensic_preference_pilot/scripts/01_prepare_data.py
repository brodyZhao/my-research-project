from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from PIL import Image

from common import normalize_manifest_row, read_jsonl, require_file, write_jsonl


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate and lock a Stage-A sample manifest")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--seed", type=int, default=20260915)
    args = parser.parse_args()

    rows = read_jsonl(args.manifest)
    if args.limit is not None:
        rows = rows[: args.limit]
    if not rows:
        raise ValueError("no rows selected")
    normalized = []
    for row in rows:
        item = normalize_manifest_row(row, args.source_root)
        require_file(item["image_path"], "image")
        require_file(item["claimed_mask_path"], "claimed mask")
        if item["gt_mask_path"]:
            require_file(item["gt_mask_path"], "GT mask")
        with Image.open(item["image_path"]) as image, Image.open(item["claimed_mask_path"]) as mask:
            if mask.size != image.size:
                raise ValueError(
                    f"{item['sample_id']} claimed mask size {mask.size} != image size {image.size}"
                )
        normalized.append(item)

    random.Random(args.seed).shuffle(normalized)
    destination = Path(args.output_dir)
    metadata_dir = destination / "metadata"
    metadata_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(metadata_dir / "validated_manifest.jsonl", normalized)
    summary = {
        "stage": "A",
        "seed": args.seed,
        "n": len(normalized),
        "has_gt_mask": sum(item["gt_mask_path"] is not None for item in normalized),
        "has_paired_original": sum(bool(item.get("original_path")) for item in normalized),
        "source_manifest": str(Path(args.manifest).resolve()),
        "source_root": str(Path(args.source_root).resolve()),
        "note": "No paired original was found in the locked manifest; this run uses perturbation diagnostics on forged images.",
    }
    (metadata_dir / "preparation.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()

