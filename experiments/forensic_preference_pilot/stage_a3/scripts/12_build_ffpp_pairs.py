#!/usr/bin/env python3
"""从抽取出的 FakeClue ff++ 图片建立 real/fake 配对清单。

配对键：FF++ 的 original_sequences 用 frames/<video>/<frame>.png，
        而 manipulated_sequences 用 frames/<video>_<clip>/<frame>.png
        —— 同一视频同一帧。所以键 = (split, video, frame)，
        其中 fake 的 video 从 "<video>_<clip>" 里取下划线前半段。

⚠️ 已知限制：FakeClue 不提供 mask，所以本清单的 gt_mask_path 恒为 None。
   GT 掩码需后续从 (real, fake) 差分图派生（步骤 13），或另建人脸检测器生成。
   在没有 GT 掩码前，本数据集只能做：
     - Gate 0 准确率
     - 基于 claimed 区域的必要性检验（x_restore_claimed 只需 claimed 区域，
       不需要 GT 掩码）—— 这正是本课题的核心检验
   而不能做 IoU(claimed, GT) 与 x_restore_gt。

输出：
  <out-dir>/pairs_ffpp.jsonl            全部配对
  <out-dir>/gate0_sample.jsonl          分层抽样，供 Gate 0 使用（按篡改方法分层）
  <out-dir>/pairs_summary.json
"""

from __future__ import annotations

import argparse
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

REAL_PATTERN = re.compile(r"/ff\+\+/real/\w+/c23/frames/(?P<video>\d+)/(?P<frame>\d+)\.png$")
FAKE_PATTERN = re.compile(
    r"/ff\+\+/fake/(?P<method>[^/]+)/c23/frames/(?P<video>\d+)_\d+/(?P<frame>\d+)\.png$"
)


def split_of(path: Path, root: Path) -> str:
    relative = path.relative_to(root)
    return relative.parts[0] if relative.parts else "unknown"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build FakeClue ff++ real/fake pair manifest")
    parser.add_argument("--root", required=True, help="fetch_fakeclue_ffpp.sh 的 --out-dir")
    parser.add_argument("--source-root", required=True, help="manifest 相对路径的解析根")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--gate0-sample", type=int, default=400, help="Gate 0 分层抽样量")
    parser.add_argument("--seed", type=int, default=20260921)
    args = parser.parse_args()

    root = Path(args.root)
    source_root = Path(args.source_root)

    reals: dict[tuple[str, str, str], Path] = {}
    fakes: dict[tuple[str, str, str], list[tuple[Path, str]]] = defaultdict(list)
    for path in root.rglob("*.png"):
        text = str(path)
        fake_match = FAKE_PATTERN.search(text)
        if fake_match:
            key = (
                split_of(path, root),
                fake_match.group("video"),
                fake_match.group("frame"),
            )
            fakes[key].append((path, fake_match.group("method")))
            continue
        real_match = REAL_PATTERN.search(text)
        if real_match:
            key = (
                split_of(path, root),
                real_match.group("video"),
                real_match.group("frame"),
            )
            reals[key] = path

    def relative(path: Path) -> str:
        try:
            return str(path.relative_to(source_root))
        except ValueError:
            return str(path)

    records = []
    for key, real_path in sorted(reals.items()):
        split, video, frame = key
        for fake_path, method in sorted(fakes.get(key, []), key=lambda item: item[1]):
            sample_id = f"ffpp_{split}_{video}_{frame}_{method}"
            records.append(
                {
                    "sample_id": sample_id,
                    "dataset": "FakeClue-FF++",
                    "split": split,
                    "pristine_path": relative(real_path),
                    "forged_path": relative(fake_path),
                    "image_path": relative(fake_path),  # 兼容既有推理脚本
                    "gt_mask_path": None,  # FakeClue 不提供 mask，见文件头说明
                    "gt_mask_source": "not_provided",
                    "claimed_mask_path": None,
                    "label": 1,  # 1 = fake
                    "source_image_id": f"ffpp_{video}_{frame}",
                    "manipulation_type": f"face_swap:{method}",
                    "method": method,
                    "video": video,
                    "frame": frame,
                    "eligible": True,
                    "exclusion_reasons": [],
                }
            )

    if not records:
        raise ValueError("没有构造出任何配对，检查 REAL/FAKE 正则是否匹配实际路径")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    pairs_path = out_dir / "pairs_ffpp.jsonl"
    with pairs_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    # 按 (split, method) 分层抽样，保证各篡改方法均衡
    strata: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for record in records:
        strata[(record["split"], record["method"])].append(record)
    rng = random.Random(args.seed)
    per_stratum = max(1, args.gate0_sample // max(1, len(strata)))
    sample = []
    for key in sorted(strata):
        pool = sorted(strata[key], key=lambda item: item["sample_id"])
        rng.shuffle(pool)
        sample.extend(pool[:per_stratum])
    sample.sort(key=lambda item: item["sample_id"])
    sample_path = out_dir / "gate0_sample.jsonl"
    with sample_path.open("w", encoding="utf-8") as handle:
        for record in sample:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    summary = {
        "dataset": "FakeClue-FF++",
        "n_pairs": len(records),
        "n_unique_source_images": len(reals),
        "by_split": dict(Counter(r["split"] for r in records)),
        "by_method": dict(Counter(r["method"] for r in records)),
        "gate0_sample": {"n": len(sample), "strata": len(strata), "per_stratum": per_stratum},
        "gt_mask": "not_provided（需由差分图派生或人脸检测器生成）",
        "outputs": {"pairs": str(pairs_path), "gate0_sample": str(sample_path)},
    }
    (out_dir / "pairs_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
