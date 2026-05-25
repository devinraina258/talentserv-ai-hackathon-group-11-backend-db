#!/usr/bin/env python3
"""preCompact — clear read cache after compaction (cache-cow)."""
from __future__ import annotations

import json
import shutil

from cache_cow_lib import CACHE_BASE, conversation_id, load_input, log_hook


def main() -> None:
    data = load_input()
    conv = conversation_id(data)
    if conv:
        cache_dir = CACHE_BASE / conv
        if cache_dir.is_dir():
            count = sum(1 for _ in cache_dir.rglob("*") if _.is_file())
            shutil.rmtree(cache_dir, ignore_errors=True)
            if count > 0:
                log_hook(f"pre-compact: read cache cleared ({count} entries)")
                print(json.dumps({
                    "user_message": (
                        "cache-cow: read cache cleared after compaction — "
                        "re-read files only when needed."
                    ),
                }))
                return


if __name__ == "__main__":
    main()
