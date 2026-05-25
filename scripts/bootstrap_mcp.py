#!/usr/bin/env python3
"""Bootstrap one or both MCP servers into .cursor/mcp.json (portable paths)."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MCP_JSON = ROOT / ".cursor" / "mcp.json"
ENV_EXAMPLE = ROOT / ".env.example"
ENV_FILE = ROOT / ".env"
GRAPH_JSON = ROOT / "graphify-out" / "graph.json"

RAW = (
    "https://raw.githubusercontent.com/devinraina258/"
    "talentserv-ai-hackathon-group-11-backend-db/master/scripts"
)

RAW_INSTALL = (
    "https://raw.githubusercontent.com/devinraina258/"
    "talentserv-ai-hackathon-group-11-backend-db/master/scripts"
)


def run(cmd: list[str], **kwargs) -> None:
    print("+", " ".join(str(c) for c in cmd))
    subprocess.run(cmd, cwd=ROOT, check=True, **kwargs)


def venv_python() -> Path:
    if sys.platform == "win32":
        py = ROOT / ".venv" / "Scripts" / "python.exe"
    else:
        py = ROOT / ".venv" / "bin" / "python"
    if not py.is_file():
        raise SystemExit(f"venv python not found: {py}")
    return py


def ensure_venv() -> Path:
    marker = ROOT / ".venv" / (
        "Scripts/python.exe" if sys.platform == "win32" else "bin/python"
    )
    if not marker.is_file():
        print("[bootstrap] creating .venv ...")
        run([sys.executable, "-m", "venv", str(ROOT / ".venv")])
    return venv_python()


def merge_mcp_server(name: str, entry: dict) -> None:
    if MCP_JSON.is_file():
        config = json.loads(MCP_JSON.read_text(encoding="utf-8"))
    else:
        config = {}
    servers = config.setdefault("mcpServers", {})
    servers[name] = entry
    MCP_JSON.parent.mkdir(parents=True, exist_ok=True)
    MCP_JSON.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    print(f"[bootstrap] merged MCP server '{name}' -> {MCP_JSON}")


def sync_graphify(py: Path) -> None:
    if shutil.which("graphify"):
        run(["graphify", "update", "."])
        run(
            [
                "graphify",
                "tree",
                "--graph",
                "graphify-out/graph.json",
                "--output",
                "graphify-out/GRAPH_TREE.html",
            ]
        )
    else:
        run([str(py), "-m", "graphify", "update", "."])
        run(
            [
                str(py),
                "-m",
                "graphify",
                "tree",
                "--graph",
                "graphify-out/graph.json",
                "--output",
                "graphify-out/GRAPH_TREE.html",
            ]
        )
    export_script = ROOT / "scripts" / "export_graph_tree_jsonl.py"
    if export_script.is_file():
        run([str(py), str(export_script)])
    else:
        print("[bootstrap] skip JSONL export (export_graph_tree_jsonl.py not found)")


def setup_office_leave(py: Path) -> None:
    from scripts.mcp_install_lib import install_office_leave

    print("[bootstrap:office-leave] installing package + dev deps ...")
    run([str(py), "-m", "pip", "install", "--upgrade", "pip"])
    run([str(py), "-m", "pip", "install", "-e", ".[dev]"])
    install_office_leave(ROOT)
    run([str(py), "-c", "import src.server; print('office-leave ok')"])


def setup_graphify(py: Path, *, force_graph: bool) -> None:
    from scripts.mcp_install_lib import install_graphify

    print("[bootstrap:graphify] installing graphifyy[mcp] ...")
    run([str(py), "-m", "pip", "install", "--upgrade", "pip"])
    run([str(py), "-m", "pip", "install", "-e", ".[graphify]"])

    if force_graph or not GRAPH_JSON.is_file():
        print("[bootstrap:graphify] building graphify-out ...")
        sync_graphify(py)
    install_graphify(ROOT)
    run([str(py), "-c", "import graphify.serve; print('graphify ok')"])


def print_done(servers: list[str]) -> None:
    names = ", ".join(servers)
    print(
        f"\n[bootstrap] Done ({names}).\n"
        "  1. Reload Cursor (Developer: Reload Window)\n"
        f"  2. Settings -> MCP -> enable: {names}\n"
        f"  3. Config: {MCP_JSON}\n"
        "\nClone-free install (any folder, no git clone):\n"
        f"  office-leave: curl -fsSL {RAW_INSTALL}/install-office-leave-mcp.sh | bash\n"
        f"  graphify:     curl -fsSL {RAW_INSTALL}/install-graphify-mcp.sh | bash\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap MCP servers for Cursor")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--office-leave",
        action="store_true",
        help="Set up office-leave MCP only",
    )
    group.add_argument(
        "--graphify",
        action="store_true",
        help="Set up graphify MCP only",
    )
    group.add_argument(
        "--all",
        action="store_true",
        help="Set up both MCP servers (default)",
    )
    parser.add_argument(
        "--force-graph",
        action="store_true",
        help="Rebuild graphify-out even if graph.json exists",
    )
    args = parser.parse_args()

    if not (args.office_leave or args.graphify or args.all):
        args.all = True

    os.chdir(ROOT)
    print(f"[bootstrap] repo: {ROOT}")

    py = ensure_venv()
    done: list[str] = []

    if args.all or args.office_leave:
        setup_office_leave(py)
        done.append("office-leave")

    if args.all or args.graphify:
        setup_graphify(py, force_graph=args.force_graph)
        done.append("graphify")

    print_done(done)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
