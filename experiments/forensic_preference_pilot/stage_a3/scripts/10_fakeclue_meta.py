#!/usr/bin/env python3
"""读取 FakeClue zip 的中央目录，取出 ff++ 成员的精确字节偏移，供区间下载 + 按偏移抽取。

为什么这么做：FakeClue 的 train.zip 有 28.4 GB，但 ff++ 子集只占约 1.8 GB。
逐成员用 remotezip 抓需要 2.5 万次 HTTP 请求（数小时）；而 ff++ 成员在 zip 中
近乎连续，所以只取 [first_offset, last_end) 这一个区间即可，一次下载搞定。

抽取不依赖"完全连续"假设：按中央目录记录的 header_offset 定位每个成员的
local header，从 blob 里读出真正的 extra 长度再切片。区间内的间隙无害。

输出 <out-dir>/ffpp_meta.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from remotezip import RemoteZip

MEMBER_MARKER = "/ff++/"


def collect(url: str) -> dict:
    with RemoteZip(url, support_suffix_range=True) as archive:
        infos = [
            info
            for info in archive.infolist()
            if MEMBER_MARKER in info.filename and info.filename.endswith(".png")
        ]
        if not infos:
            raise ValueError(f"{url} 中没有 ff++ 成员")
        infos.sort(key=lambda info: info.header_offset)
        members = [
            {
                "name": info.filename,
                "offset": info.header_offset,
                "compress_size": info.compress_size,
                "file_size": info.file_size,
                "method": info.compress_type,
            }
            for info in infos
        ]
        last = infos[-1]
        last_end = (
            last.header_offset
            + 30
            + len(last.filename.encode("utf-8"))
            + len(last.extra)
            + last.compress_size
        )
        return {
            "url": url,
            "n_members": len(members),
            "first_offset": infos[0].header_offset,
            "last_end": last_end,
            "span_bytes": last_end - infos[0].header_offset,
            "uncompressed_bytes": sum(info.file_size for info in infos),
            "members": members,
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect ff++ member offsets from FakeClue zips")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument(
        "--splits",
        nargs="+",
        default=["train", "test"],
        help="FakeClue 的 zip 名（不含扩展名）",
    )
    parser.add_argument(
        "--base-url",
        default="https://hf-mirror.com/datasets/lingcco/FakeClue/resolve/main",
    )
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    meta = {}
    for split in args.splits:
        url = f"{args.base_url}/{split}.zip"
        entry = collect(url)
        meta[split] = entry
        print(
            json.dumps(
                {
                    "split": split,
                    "n_members": entry["n_members"],
                    "first_offset": entry["first_offset"],
                    "last_end": entry["last_end"],
                    "span_mb": round(entry["span_bytes"] / 1e6, 1),
                    "uncompressed_mb": round(entry["uncompressed_bytes"] / 1e6, 1),
                },
                ensure_ascii=False,
            ),
            flush=True,
        )

    (out_dir / "ffpp_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    total = sum(entry["span_bytes"] for entry in meta.values())
    print(f"合计需下载区间: {total / 1e6:.1f} MB", flush=True)


if __name__ == "__main__":
    main()
