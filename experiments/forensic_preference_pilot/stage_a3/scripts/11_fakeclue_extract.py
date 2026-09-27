#!/usr/bin/env python3
"""从下载好的 FakeClue 字节区间 blob 中，按中央目录的偏移精确抽取 ff++ 图片。

不依赖成员连续性：每个成员由 header_offset 定位，从 blob 里读出该成员 local header
的真实 extra 长度后切片，再按压缩方式解压（store / deflate）。

用 mmap 读取 blob，避免把 1.8 GB 读进内存。

输出 <out-dir>/<member name>，例如 out/ff++/train/ff++/real/youtube/c23/frames/778/116.png
维护的目录结构可直接用于后续 real/fake 配对。
"""

from __future__ import annotations

import argparse
import json
import mmap
import struct
import zlib
from pathlib import Path

LOCAL_HEADER_SIGNATURE = b"PK\x03\x04"
LOCAL_HEADER_FIXED_SIZE = 30
NAME_LENGTH_FIELD = 26  # 固定头内 name_len / extra_len 的位置


def extract_member(blob: mmap.mmap, member: dict, first_offset: int) -> bytes:
    offset = member["offset"] - first_offset
    if blob[offset : offset + 4] != LOCAL_HEADER_SIGNATURE:
        raise ValueError(f"{member['name']} 偏移处不是 local header 签名")
    name_length, extra_length = struct.unpack_from("<HH", blob, offset + NAME_LENGTH_FIELD)
    data_offset = offset + LOCAL_HEADER_FIXED_SIZE + name_length + extra_length
    raw = blob[data_offset : data_offset + member["compress_size"]]
    if len(raw) != member["compress_size"]:
        raise ValueError(
            f"{member['name']} 数据越界：期望 {member['compress_size']} 实得 {len(raw)}"
        )
    method = member["method"]
    if method == 0:
        data = raw
    elif method == 8:
        data = zlib.decompress(raw, -zlib.MAX_WBITS)
    else:
        raise ValueError(f"{member['name']} 未知压缩方式 {method}")
    if len(data) != member["file_size"]:
        raise ValueError(
            f"{member['name']} 解压后大小不符：期望 {member['file_size']} 实得 {len(data)}"
        )
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract ff++ members from a downloaded byte-range blob")
    parser.add_argument("--meta", required=True, help="10_fakeclue_meta.py 生成的 ffpp_meta.json")
    parser.add_argument("--split", required=True)
    parser.add_argument("--blob", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    meta = json.loads(Path(args.meta).read_text(encoding="utf-8"))
    if args.split not in meta:
        raise KeyError(f"{args.meta} 中没有 split {args.split}")
    entry = meta[args.split]
    members = entry["members"]
    if args.limit is not None:
        members = members[: args.limit]

    out_dir = Path(args.out_dir)
    blob_path = Path(args.blob)
    expected = entry["last_end"] - entry["first_offset"]
    actual = blob_path.stat().st_size
    if actual < expected:
        raise ValueError(f"{blob_path} 不完整：期望 {expected} 字节，实得 {actual}")

    failures = []
    written = 0
    with blob_path.open("rb") as handle:
        with mmap.mmap(handle.fileno(), 0, access=mmap.ACCESS_READ) as blob:
            for index, member in enumerate(members, 1):
                destination = out_dir / member["name"]
                if destination.exists() and destination.stat().st_size == member["file_size"]:
                    written += 1
                    continue
                try:
                    data = extract_member(blob, member, entry["first_offset"])
                except Exception as exc:  # 记录并继续，单个坏成员不该中断整批
                    failures.append({"name": member["name"], "error": f"{type(exc).__name__}: {exc}"})
                    continue
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(data)
                written += 1
                if index % 2000 == 0:
                    print(json.dumps({"split": args.split, "done": index, "written": written}), flush=True)

    print(
        json.dumps(
            {
                "split": args.split,
                "requested": len(members),
                "written": written,
                "failed": len(failures),
                "failures_sample": failures[:5],
            },
            ensure_ascii=False,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
