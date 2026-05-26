#!/usr/bin/env python3
"""preToolUse Read — block redundant/large reads (cache-cow)."""
from __future__ import annotations

from pathlib import Path

from cache_cow_lib import (
    CACHE_BASE,
    allow,
    allow_note,
    cache_key,
    conversation_id,
    deny,
    file_path,
    files_equal,
    load_input,
    log_hook,
    offset_limit,
    range_covered,
    read_ranges,
    should_skip,
    unified_diff,
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

    offset, limit = offset_limit(data)
    is_partial = offset is not None or limit is not None
    cache_dir = CACHE_BASE / conv
    cache_dir.mkdir(parents=True, exist_ok=True)
    key = cache_key(path_str)
    cache_file = cache_dir / key
    fname = fp.name

    if not is_partial:
        try:
            line_count = sum(1 for _ in fp.open(encoding="utf-8", errors="replace"))
        except OSError:
            line_count = 0
        if line_count > 1000:
            log_hook(f"pre-read: blocked large file {fname} ({line_count} lines)")
            deny(
                f"This file has {line_count} lines. Use offset/limit to read only the section you need."
            )

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
        snapshot = cache_dir / f"{key}.snapshot"
        ranges_file = cache_dir / f"{key}.ranges"

        if snapshot.is_file() and ranges_file.is_file():
            if files_equal(snapshot, fp):
                if range_covered(read_ranges(ranges_file), start, end):
                    log_hook(f"pre-read: partial range cache hit ({fname} {start}-{end})")
                    deny(
                        f"Range already read (lines {start}-{end}): {path_str}. "
                        "No changes since last read — use Write/StrReplace instead of re-reading."
                    )
            else:
                diff = unified_diff(snapshot, fp)
                ranges_file.unlink(missing_ok=True)
                log_hook(f"pre-read: partial read change ({fname})")
                allow_note(
                    f"Showing changes since last read: {path_str}\n---\n{diff}\n---"
                )
        elif cache_file.is_file() and ranges_file.is_file():
            if files_equal(cache_file, fp):
                if range_covered(read_ranges(ranges_file), start, end):
                    log_hook(f"pre-read: post-full-read partial hit ({fname} {start}-{end})")
                    deny(f"Range already read (lines {start}-{end}): {path_str}.")
            else:
                diff = unified_diff(cache_file, fp)
                cache_file.write_bytes(fp.read_bytes())
                ranges_file.unlink(missing_ok=True)
                log_hook(f"pre-read: post-full-read partial change ({fname})")
                allow_note(f"Showing changes since last read: {path_str}\n---\n{diff}\n---")
        allow()

    if not cache_file.is_file():
        allow()
    if files_equal(cache_file, fp):
        log_hook(f"pre-read: cache hit, blocked re-read ({fname})")
        deny(f"File unchanged (re-read unnecessary): {path_str}. Use Write/StrReplace to modify.")
    diff = unified_diff(cache_file, fp)
    cache_file.write_bytes(fp.read_bytes())
    log_hook(f"pre-read: full read change ({fname})")
    allow_note(
        f"Showing changes since last read: {path_str}\n---\n{diff}\n---\n"
        "Above diff shows changes since your last read."
    )


if __name__ == "__main__":
    main()
