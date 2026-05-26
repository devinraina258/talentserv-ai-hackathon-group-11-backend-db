"""Shared cache-cow helpers for Cursor hooks (MIT, adapted from soonswan-study/cache-cow)."""
from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path

CACHE_BASE = Path(
    os.environ.get("CURSOR_READ_CACHE")
    or os.path.join(os.environ.get("TEMP", os.environ.get("TMPDIR", "/tmp")), "cursor-read-cache")
)
LOG_PATH = Path(
    os.environ.get("CURSOR_HOOK_LOG")
    or os.path.join(os.environ.get("TEMP", os.environ.get("TMPDIR", "/tmp")), "cursor-hooks.log")
)

SKIP_SUFFIXES = (
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".pdf", ".lock",
    ".min.js", ".min.css", ".map",
)


def log_hook(message: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%H:%M:%S")
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(f"[{stamp}] {message}\n")


def load_input() -> dict:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    return json.loads(raw)


def conversation_id(data: dict) -> str:
    return str(data.get("conversation_id") or data.get("session_id") or "")


def file_path(data: dict) -> str:
    ti = data.get("tool_input") or {}
    return str(ti.get("path") or ti.get("file_path") or "")


def offset_limit(data: dict) -> tuple[int | None, int | None]:
    ti = data.get("tool_input") or {}
    off = ti.get("offset")
    lim = ti.get("limit")
    o = None if off in (None, "", "null") else int(off)
    l = None if lim in (None, "", "null") else int(lim)
    return o, l


def shell_command(data: dict) -> str:
    ti = data.get("tool_input") or {}
    return str(ti.get("command") or data.get("command") or "")


def is_write(data: dict) -> bool:
    ti = data.get("tool_input") or {}
    return any(ti.get(k) is not None for k in ("content", "new_string", "old_string"))


def should_skip(path: str) -> bool:
    p = path.replace("\\", "/")
    if any(p.endswith(s) for s in SKIP_SUFFIXES):
        return True
    if "graphify-out/cache/" in p or p.endswith("graphify-out/graph.html"):
        return True
    return False


def cache_key(path: str) -> str:
    return hashlib.md5(path.encode("utf-8")).hexdigest()


def emit(obj: dict) -> None:
    print(json.dumps(obj))
    sys.exit(0)


def allow() -> None:
    sys.exit(0)


def deny(message: str) -> None:
    emit({"permission": "deny", "agent_message": message, "user_message": message})


def allow_note(message: str) -> None:
    emit({"permission": "allow", "agent_message": message})


def allow_updated_shell(command: str, note: str) -> None:
    emit({
        "permission": "allow",
        "updated_input": {"command": command},
        "agent_message": note,
    })


def merge_ranges(ranges_file: Path) -> None:
    if not ranges_file.exists():
        return
    lines = [ln.strip() for ln in ranges_file.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if not lines:
        return
    pairs = []
    for ln in lines:
        parts = ln.split()
        if len(parts) >= 2:
            pairs.append((int(parts[0]), int(parts[1])))
    pairs.sort()
    merged: list[tuple[int, int]] = []
    for s, e in pairs:
        if not merged or s > merged[-1][1] + 1:
            merged.append((s, e))
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
    ranges_file.write_text(
        "\n".join(f"{s} {e}" for s, e in merged) + ("\n" if merged else ""),
        encoding="utf-8",
    )


def read_ranges(ranges_file: Path) -> list[tuple[int, int]]:
    if not ranges_file.exists():
        return []
    out: list[tuple[int, int]] = []
    for ln in ranges_file.read_text(encoding="utf-8").splitlines():
        parts = ln.split()
        if len(parts) >= 2:
            out.append((int(parts[0]), int(parts[1])))
    return out


def range_covered(ranges: list[tuple[int, int]], start: int, end: int) -> bool:
    return any(rs <= start and re >= end for rs, re in ranges)


def files_equal(a: Path, b: Path) -> bool:
    try:
        return a.read_bytes() == b.read_bytes()
    except OSError:
        return False


def unified_diff(old: Path, new: Path) -> str:
    import difflib

    try:
        old_lines = old.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
        new_lines = new.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
    except OSError:
        return ""
    return "".join(
        difflib.unified_diff(old_lines, new_lines, fromfile=str(old), tofile=str(new), lineterm="")
    )
