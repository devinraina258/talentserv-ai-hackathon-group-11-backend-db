#!/usr/bin/env python3
"""preToolUse Shell — filter tests and tail logs (cache-cow)."""
from __future__ import annotations

import re
from pathlib import Path

from cache_cow_lib import allow, allow_updated_shell, load_input, log_hook, shell_command

TEST_RE = re.compile(
    r"(pytest|python -m pytest|manage\.py test|npm test|npx jest|yarn test|vitest)"
)
LOG_RE = re.compile(r"(cat.*\.(log|out|err)|journalctl|docker logs)")
LOG_SKIP_RE = re.compile(r"(head|tail|wc|-n |grep)")


def main() -> None:
    data = load_input()
    command = shell_command(data)
    if not command:
        allow()

    hook_dir = Path(__file__).resolve().parent
    filter_sh = hook_dir / "pre-shell.helper.filter.sh"

    if TEST_RE.search(command) and "pre-shell.helper.filter" not in command:
        if filter_sh.is_file():
            limited = f'{command} 2>&1 | bash "{filter_sh}"'
        else:
            limited = command
        log_hook("pre-shell: test output filter applied")
        allow_updated_shell(limited, "Test output filtered (start, failures, summary only).")

    if LOG_RE.search(command) and not LOG_SKIP_RE.search(command):
        limited = f"{command} | tail -100"
        log_hook("pre-shell: log output limited to tail -100")
        allow_updated_shell(limited, "Output limited to last 100 lines to save tokens.")

    allow()


if __name__ == "__main__":
    main()
