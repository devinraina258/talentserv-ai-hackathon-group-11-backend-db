"""Export graphify-out/graph.json as a compact JSONL tree for LLM context.

Each line is one tree node (directory or symbol) with a stable path — cheaper
than grepping the repo or loading the full graph.json.

Usage:
    python scripts/export_graph_tree_jsonl.py
    python scripts/export_graph_tree_jsonl.py --graph graphify-out/graph.json -o graphify-out/graph_tree.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _walk_tree(
    node: dict,
    path: list[str],
    depth: int,
    out,
) -> None:
    name = node.get("name", "")
    total = node.get("total_count", 0)
    children = node.get("children") or []
    is_leaf = not children or name.startswith("(+")
    record = {
        "path": path + [name] if name else path,
        "name": name,
        "depth": depth,
        "total_count": total,
        "kind": "truncation" if name.startswith("(+") else ("symbol" if is_leaf and "/" not in name and "." in name else "dir" if children else "leaf"),
    }
    out.write(json.dumps(record, ensure_ascii=False) + "\n")
    for child in children:
        _walk_tree(child, record["path"], depth + 1, out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Export graphify tree to JSONL")
    parser.add_argument(
        "--graph",
        type=Path,
        default=REPO_ROOT / "graphify-out" / "graph.json",
        help="Path to graphify graph.json",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=REPO_ROOT / "graphify-out" / "graph_tree.jsonl",
        help="Output JSONL path",
    )
    args = parser.parse_args()
    if not args.graph.is_file():
        print(f"Missing graph: {args.graph}. Run: graphify update .", file=sys.stderr)
        return 1

    from graphify.tree_html import build_tree

    graph = json.loads(args.graph.read_text(encoding="utf-8"))
    tree = build_tree(graph, project_label=REPO_ROOT.name)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []

    class _Writer:
        def write(self, s: str) -> int:
            lines.append(s)
            return len(s)

    _walk_tree(tree, [], 0, _Writer())
    args.output.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {args.output} ({len(lines)} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
