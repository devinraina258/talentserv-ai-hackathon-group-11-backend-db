#!/usr/bin/env python3
"""postToolUse Read/Write/StrReplace — cache reads, invalidate on write (cache-cow)."""
from __future__ import annotations

import shutil
from pathlib import Path

from cache_cow_lib import (
    CACHE_BASE,
    allow,
    cache_key,
    conversation_id,
    file_path,
    is_write,
    load_input,
    log_hook,
    merge_ranges,
    offset_limit,
    should_skip,
)


def main() -> None:
    data = load_input()
    conv = conversation_id(data)
    path_str = file_path(data)
    if not path_str or not conv:
        allow()
    fp = Path(path_str)
    if not fp.is_file() or should_skip(path_str):
        allow()

    cache_dir = CACHE_BASE / conv
    cache_dir.mkdir(parents=True, exist_ok=True)
    key = cache_key(path_str)
    cache_file = cache_dir / key
    fname = fp.name

    if is_write(data):
        if cache_file.is_file():
            cache_file.write_bytes(fp.read_bytes())
        for extra in (cache_dir / f"{key}.snapshot", cache_dir / f"{key}.ranges"):
            extra.unlink(missing_ok=True)
        log_hook(f"post-file-cache: invalidated ({fname})")
        allow()

    offset, limit = offset_limit(data)
    is_partial = offset is not None or limit is not None
    ranges_file = cache_dir / f"{key}.ranges"
    snapshot = cache_dir / f"{key}.snapshot"

    if is_partial:
        offset_num = offset or 0
        if limit is not None:
            limit_num = limit
        else:
            limit_num = sum(1 for _ in fp.open(encoding="utf-8", errors="replace"))
        if limit_num <= 0:
            allow()
        start = offset_num + 1
        end = offset_num + limit_num
        shutil.copy2(fp, snapshot)
        with ranges_file.open("a", encoding="utf-8") as f:
            f.write(f"{start} {end}\n")
        merge_ranges(ranges_file)
        log_hook(f"post-file-cache: partial range ({fname} {start}-{end})")
    else:
        total = sum(1 for _ in fp.open(encoding="utf-8", errors="replace"))
        cache_file.write_bytes(fp.read_bytes())
        ranges_file.write_text(f"1 {total}\n", encoding="utf-8")
        snapshot.unlink(missing_ok=True)
        log_hook(f"post-file-cache: full read cached ({fname})")
    allow()


if __name__ == "__main__":
    main()
