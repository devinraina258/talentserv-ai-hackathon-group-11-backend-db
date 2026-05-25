#!/usr/bin/env python3
"""Run MCP modules with the repo .venv Python (cross-platform).

Cursor can use:
  "command": "python",
  "args": ["${workspaceFolder}${/}scripts${/}mcp_launcher.py", "-m", "src.server"]
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def venv_python() -> Path | None:
    if sys.platform == "win32":
        candidate = ROOT / ".venv" / "Scripts" / "python.exe"
    else:
        candidate = ROOT / ".venv" / "bin" / "python"
    return candidate if candidate.is_file() else None


def main() -> int:
    py = venv_python()
    if py is None:
        print(
            "MCP bootstrap required: .venv is missing.\n"
            f"  Repo: {ROOT}\n"
            "  Run from repo root:\n"
            "    curl -fsSL https://raw.githubusercontent.com/devinraina258/"
            "talentserv-ai-hackathon-group-11-backend-db/main/scripts/bootstrap-mcp.sh | bash\n"
            "  Or (Windows PowerShell):\n"
            "    irm .../bootstrap-mcp.ps1 | iex\n"
            "  Or: python scripts/bootstrap_mcp.py",
            file=sys.stderr,
        )
        return 1
    if len(sys.argv) < 2:
        print("usage: mcp_launcher.py -m <module> [module args...]", file=sys.stderr)
        return 2
    return subprocess.call([str(py), *sys.argv[1:]], cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
