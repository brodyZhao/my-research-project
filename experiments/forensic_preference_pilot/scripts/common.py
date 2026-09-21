from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_number} is not a JSON object")
            rows.append(value)
    return rows


def write_jsonl(path: str | Path, rows: Iterable[dict[str, Any]]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def append_jsonl(path: str | Path, row: dict[str, Any]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        handle.flush()


def resolve_path(root: str | Path, value: str | Path) -> Path:
    candidate = Path(value)
    return candidate if candidate.is_absolute() else Path(root) / candidate


def first_existing(row: dict[str, Any], keys: tuple[str, ...]) -> str | None:
    for key in keys:
        value = row.get(key)
        if isinstance(value, str) and value:
            return value
    nested = row.get("qwen_output")
    if isinstance(nested, dict):
        for key in keys:
            value = nested.get(key)
            if isinstance(value, str) and value:
                return value
    return None


def normalize_manifest_row(row: dict[str, Any], source_root: str | Path) -> dict[str, Any]:
    if not row.get("sample_id"):
        raise ValueError("manifest row is missing sample_id")
    image_value = first_existing(row, ("forged_path", "image_path"))
    target_value = first_existing(row, ("claimed_mask_path", "evidence_mask_path"))
    gt_value = first_existing(
        row,
        ("gt_mask_path", "human_evidence_mask_path", "human_mask_path"),
    )
    if not image_value or not target_value:
        raise ValueError(f"{row['sample_id']} is missing image_path or evidence_mask_path")
    normalized = dict(row)
    normalized["sample_id"] = str(row["sample_id"])
    normalized["image_path"] = str(resolve_path(source_root, image_value))
    normalized["claimed_mask_path"] = str(resolve_path(source_root, target_value))
    normalized["gt_mask_path"] = (
        str(resolve_path(source_root, gt_value)) if gt_value else None
    )
    normalized["baseline_source"] = "locked_remote_manifest"
    return normalized


def require_file(path: str | Path, description: str) -> None:
    candidate = Path(path)
    if not candidate.is_file():
        raise FileNotFoundError(f"{description} does not exist: {candidate}")

