#!/usr/bin/env python3
"""sessionStart — clear read cache (cache-cow)."""
from __future__ import annotations

import json
import shutil
import time

from cache_cow_lib import CACHE_BASE, conversation_id, load_input, log_hook


def main() -> None:
    data = load_input()
    conv = conversation_id(data)
    CACHE_BASE.mkdir(parents=True, exist_ok=True)
    if conv:
        cache_dir = CACHE_BASE / conv
        if cache_dir.is_dir():
            count = sum(1 for _ in cache_dir.rglob("*") if _.is_file())
            shutil.rmtree(cache_dir, ignore_errors=True)
            log_hook(f"session-start: read cache cleared ({count} entries)")
    else:
        log_hook("session-start: no conversation id")
    cutoff = time.time() - 7 * 86400
    for child in CACHE_BASE.iterdir():
        if child.is_dir() and child.stat().st_mtime < cutoff:
            shutil.rmtree(child, ignore_errors=True)
    print(json.dumps({
        "additional_context": (
            "cache-cow: read cache initialized. "
            "Do not re-read unchanged files; use offset/limit for files over 1000 lines."
        ),
    }))


if __name__ == "__main__":
    main()
