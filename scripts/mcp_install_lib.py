#!/usr/bin/env python3
"""Clone-free MCP install: merge .cursor/mcp.json and write .cursor/bin launchers."""
from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
from pathlib import Path

RAW_BASE = (
    "https://raw.githubusercontent.com/devinraina258/"
    "talentserv-ai-hackathon-group-11-backend-db/master"
)
GIT_PKG = (
    "git+https://github.com/devinraina258/"
    "talentserv-ai-hackathon-group-11-backend-db@master"
)

# Runtime deps for `python -m src.server` from workspace (no wheel build; avoids file locks).
OFFICE_LEAVE_RUNTIME_DEPS = "fastmcp>=2.0.0 httpx>=0.27.0 python-dotenv>=1.0.0"

# Venv fallback: deps-only in a clone; full package from git otherwise.
_OFFICE_LEAVE_VENV_INSTALL_SH = r'''
if [ -f "$WS/pyproject.toml" ]; then
  "$PY" -m pip install -q -U pip ''' + OFFICE_LEAVE_RUNTIME_DEPS + r'''
else
  "$PY" -m pip install -q -U pip "$GIT_PKG"
fi
'''

_OFFICE_LEAVE_VENV_INSTALL_CMD = r'''
if exist "%WS%\pyproject.toml" (
  "%VENV%\Scripts\python.exe" -m pip install -q -U pip ''' + OFFICE_LEAVE_RUNTIME_DEPS + r'''
) else (
  "%VENV%\Scripts\python.exe" -m pip install -q -U pip "''' + GIT_PKG + r'''"
)
'''

OFFICE_LEAVE_MCP = {
    "command": "${workspaceFolder}${/}.cursor${/}bin${/}office-leave-mcp${/}run",
    "args": [],
    "cwd": "${workspaceFolder}",
    "env": {
        "DATABASE_PATH": "data/employees.db",
        "OFFICE_LEAVE_WORKSPACE": "${workspaceFolder}",
    },
}

GRAPHIFY_MCP = {
    "command": "${workspaceFolder}${/}.cursor${/}bin${/}graphify-mcp${/}run",
    "args": [],
    "cwd": "${workspaceFolder}",
}


def merge_mcp_json(workspace: Path, server_name: str, entry: dict) -> Path:
    mcp_path = workspace / ".cursor" / "mcp.json"
    mcp_path.parent.mkdir(parents=True, exist_ok=True)
    if mcp_path.is_file():
        config = json.loads(mcp_path.read_text(encoding="utf-8"))
    else:
        config = {}
    config.setdefault("mcpServers", {})[server_name] = entry
    mcp_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return mcp_path


OFFICE_LEAVE_RUN_SH = r'''#!/usr/bin/env sh
set -eu
WS="$(cd "$(dirname "$0")/../../.." && pwd)"
export OFFICE_LEAVE_WORKSPACE="$WS"
export DATABASE_PATH="${DATABASE_PATH:-data/employees.db}"
GIT_PKG="''' + GIT_PKG + r'''"
if command -v uvx >/dev/null 2>&1; then
  exec uvx --from "$GIT_PKG" office-leave-mcp
fi
if command -v pipx >/dev/null 2>&1; then
  exec pipx run --spec "$GIT_PKG" office-leave-mcp
fi
VENV="$WS/.cursor/mcp-venv"
if [ ! -x "$VENV/bin/python" ] && [ ! -x "$VENV/Scripts/python.exe" ]; then
  python3 -m venv "$VENV" 2>/dev/null || python -m venv "$VENV"
fi
PY="$VENV/bin/python"; [ -x "$PY" ] || PY="$VENV/Scripts/python.exe"
if ! "$PY" -c "import src.server" 2>/dev/null; then
''' + _OFFICE_LEAVE_VENV_INSTALL_SH + r'''
fi
exec "$PY" -m src.server
'''

OFFICE_LEAVE_INIT_SH = r'''#!/usr/bin/env sh
set -eu
WS="$(cd "$(dirname "$0")/../../.." && pwd)"
export OFFICE_LEAVE_WORKSPACE="$WS"
export DATABASE_PATH="${DATABASE_PATH:-data/employees.db}"
GIT_PKG="''' + GIT_PKG + r'''"
if command -v uvx >/dev/null 2>&1; then
  exec uvx --from "$GIT_PKG" office-leave-init-db
fi
if command -v pipx >/dev/null 2>&1; then
  exec pipx run --spec "$GIT_PKG" office-leave-init-db
fi
VENV="$WS/.cursor/mcp-venv"
PY="$VENV/bin/python"; [ -x "$PY" ] || PY="$VENV/Scripts/python.exe"
if [ ! -x "$PY" ]; then
  python3 -m venv "$VENV" 2>/dev/null || python -m venv "$VENV"
  PY="$VENV/bin/python"; [ -x "$PY" ] || PY="$VENV/Scripts/python.exe"
  "$PY" -m pip install -q -U pip "$GIT_PKG"
fi
exec "$PY" -m src.init_db
'''

GRAPHIFY_RUN_SH = r'''#!/usr/bin/env sh
set -eu
WS="$(cd "$(dirname "$0")/../../.." && pwd)"
GRAPH="$WS/graphify-out/graph.json"
if command -v uvx >/dev/null 2>&1; then
  exec uvx --from 'graphifyy[mcp]' python -m graphify.serve "$GRAPH"
fi
if command -v pipx >/dev/null 2>&1; then
  exec pipx run --spec 'graphifyy[mcp]' python -m graphify.serve "$GRAPH"
fi
VENV="$WS/.cursor/mcp-venv"
if [ ! -x "$VENV/bin/python" ] && [ ! -x "$VENV/Scripts/python.exe" ]; then
  python3 -m venv "$VENV" 2>/dev/null || python -m venv "$VENV"
fi
PY="$VENV/bin/python"; [ -x "$PY" ] || PY="$VENV/Scripts/python.exe"
"$PY" -c "import graphify" 2>/dev/null || "$PY" -m pip install -q -U 'graphifyy[mcp]'
exec "$PY" -m graphify.serve "$GRAPH"
'''

GRAPHIFY_BUILD_SH = r'''#!/usr/bin/env sh
set -eu
WS="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$WS"
mkdir -p graphify-out
if command -v uvx >/dev/null 2>&1; then
  uvx --from 'graphifyy[mcp]' python -m graphify update .
  uvx --from 'graphifyy[mcp]' python -m graphify tree --graph graphify-out/graph.json --output graphify-out/GRAPH_TREE.html
  exit 0
fi
if command -v graphify >/dev/null 2>&1; then
  graphify update .
  graphify tree --graph graphify-out/graph.json --output graphify-out/GRAPH_TREE.html
  exit 0
fi
VENV="$WS/.cursor/mcp-venv"
PY="$VENV/bin/python"; [ -x "$PY" ] || PY="$VENV/Scripts/python.exe"
if [ ! -x "$PY" ]; then
  python3 -m venv "$VENV" 2>/dev/null || python -m venv "$VENV"
  PY="$VENV/bin/python"; [ -x "$PY" ] || PY="$VENV/Scripts/python.exe"
  "$PY" -m pip install -q 'graphifyy[mcp]'
fi
"$PY" -m graphify update .
"$PY" -m graphify tree --graph graphify-out/graph.json --output graphify-out/GRAPH_TREE.html
'''

OFFICE_LEAVE_RUN_CMD = r'''@echo off
setlocal
set "WS=%~dp0..\..\.."
for %%I in ("%WS%") do set "WS=%%~fI"
set OFFICE_LEAVE_WORKSPACE=%WS%
if not defined DATABASE_PATH set DATABASE_PATH=data/employees.db
where uvx >nul 2>&1 && (uvx --from "''' + GIT_PKG + r'''" office-leave-mcp & exit /b %ERRORLEVEL%)
where pipx >nul 2>&1 && (pipx run --spec "''' + GIT_PKG + r'''" office-leave-mcp & exit /b %ERRORLEVEL%)
set "VENV=%WS%\.cursor\mcp-venv"
if not exist "%VENV%\Scripts\python.exe" (
  python -m venv "%VENV%"
)
"%VENV%\Scripts\python.exe" -c "import src.server" 2>nul || (
''' + _OFFICE_LEAVE_VENV_INSTALL_CMD + r'''
)
"%VENV%\Scripts\python.exe" -m src.server
'''

GRAPHIFY_RUN_CMD = r'''@echo off
setlocal
set "WS=%~dp0..\..\.."
for %%I in ("%WS%") do set "WS=%%~fI"
set "GRAPH=%WS%\graphify-out\graph.json"
where uvx >nul 2>&1 && (uvx --from graphifyy[mcp] python -m graphify.serve "%GRAPH%" & exit /b %ERRORLEVEL%)
where pipx >nul 2>&1 && (pipx run --spec graphifyy[mcp] python -m graphify.serve "%GRAPH%" & exit /b %ERRORLEVEL%)
set "VENV=%WS%\.cursor\mcp-venv"
if not exist "%VENV%\Scripts\python.exe" (
  python -m venv "%VENV%"
)
"%VENV%\Scripts\python.exe" -c "import graphify" 2>nul || "%VENV%\Scripts\python.exe" -m pip install -q -U "graphifyy[mcp]"
"%VENV%\Scripts\python.exe" -m graphify.serve "%GRAPH%"
'''


def write_launcher(workspace: Path, name: str, run_sh: str, run_cmd: str, extra: dict[str, str] | None = None) -> None:
    bin_dir = workspace / ".cursor" / "bin" / name
    bin_dir.mkdir(parents=True, exist_ok=True)
    run_path = bin_dir / "run"
    run_path.write_text(run_sh.strip() + "\n", encoding="utf-8", newline="\n")
    if platform.system() != "Windows":
        run_path.chmod(0o755)
    (bin_dir / "run.cmd").write_text(run_cmd.strip() + "\r\n", encoding="utf-8")
    if extra:
        for fname, body in extra.items():
            p = bin_dir / fname
            p.write_text(body.strip() + "\n", encoding="utf-8", newline="\n")
            if fname.endswith(".sh") and platform.system() != "Windows":
                p.chmod(0o755)


def _venv_python(venv: Path) -> Path | None:
    for rel in ("Scripts/python.exe", "bin/python"):
        p = venv / rel
        if p.is_file():
            return p
    return None


def _install_office_leave_into_venv(py: Path, workspace: Path) -> None:
    subprocess.run([str(py), "-m", "pip", "install", "-q", "-U", "pip"], check=True)
    if (workspace / "pyproject.toml").is_file():
        subprocess.run(
            [str(py), "-m", "pip", "install", "-q", *OFFICE_LEAVE_RUNTIME_DEPS.split()],
            check=True,
        )
    else:
        subprocess.run([str(py), "-m", "pip", "install", "-q", GIT_PKG], check=True)


def _create_venv_python(workspace: Path, venv: Path) -> Path:
    venv.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
    py = _venv_python(venv)
    if not py:
        raise RuntimeError(f"Failed to create venv at {venv}")
    _install_office_leave_into_venv(py, workspace)
    return py


def install_office_leave(workspace: Path) -> None:
    print(f"[install] office-leave -> {workspace}")
    write_launcher(
        workspace,
        "office-leave-mcp",
        OFFICE_LEAVE_RUN_SH,
        OFFICE_LEAVE_RUN_CMD,
        {"init-db.sh": OFFICE_LEAVE_INIT_SH},
    )
    merge_mcp_json(workspace, "office-leave", OFFICE_LEAVE_MCP)
    env = {
        "OFFICE_LEAVE_WORKSPACE": str(workspace),
        "DATABASE_PATH": "data/employees.db",
    }
    db_path = workspace / "data" / "employees.db"
    if not db_path.is_file():
        print("[install] initializing database...")
        for args in (
            ["uvx", "--from", GIT_PKG, "office-leave-init-db"],
            ["pipx", "run", "--spec", GIT_PKG, "office-leave-init-db"],
        ):
            try:
                subprocess.run(args, cwd=workspace, check=True, env={**os.environ, **env})
                break
            except (FileNotFoundError, subprocess.CalledProcessError):
                continue
        else:
            py = _create_venv_python(workspace, workspace / ".cursor" / "mcp-venv")
            subprocess.run([str(py), "-m", "src.init_db"], cwd=workspace, check=True, env=env)
    env_example = workspace / ".env.example"
    env_file = workspace / ".env"
    if env_example.is_file() and not env_file.is_file():
        env_file.write_text(env_example.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"[install] created {env_file}")


def install_graphify(workspace: Path) -> None:
    print(f"[install] graphify -> {workspace}")
    write_launcher(
        workspace,
        "graphify-mcp",
        GRAPHIFY_RUN_SH,
        GRAPHIFY_RUN_CMD,
        {"build-graph.sh": GRAPHIFY_BUILD_SH},
    )
    merge_mcp_json(workspace, "graphify", GRAPHIFY_MCP)
    graph_json = workspace / "graphify-out" / "graph.json"
    if not graph_json.is_file():
        print("[install] building graphify-out (first time, AST only)...")
        for args in (
            ["uvx", "--from", "graphifyy[mcp]", "python", "-m", "graphify", "update", "."],
            ["graphify", "update", "."],
        ):
            try:
                subprocess.run(args, cwd=workspace, check=True)
                break
            except (FileNotFoundError, subprocess.CalledProcessError):
                continue
        else:
            py = _create_venv_python(workspace, workspace / ".cursor" / "mcp-venv", "graphifyy[mcp]")
            subprocess.run([str(py), "-m", "graphify", "update", "."], cwd=workspace, check=True)
    if graph_json.is_file():
        print(f"[install] graph ready: {graph_json}")
    else:
        print("[install] warning: graphify-out/graph.json missing — run build-graph.sh or open repo with graph committed")


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        print("Usage: mcp_install_lib.py office-leave|graphify|all [workspace]")
        return 0
    cmd = argv[0]
    workspace = Path(argv[1]).resolve() if len(argv) > 1 else Path.cwd().resolve()
    if cmd == "office-leave":
        install_office_leave(workspace)
    elif cmd == "graphify":
        install_graphify(workspace)
    elif cmd == "all":
        install_office_leave(workspace)
        install_graphify(workspace)
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        return 2
    print("\n[install] Done. Reload Cursor (Developer: Reload Window), then enable MCP servers.")
    print(f"  Config: {workspace / '.cursor' / 'mcp.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
