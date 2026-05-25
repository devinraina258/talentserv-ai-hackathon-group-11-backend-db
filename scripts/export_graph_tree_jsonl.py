"""Export graphify-out/graph.json as a compact JSONL tree for LLM context."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _walk_tree(node: dict, path: list[str], depth: int, lines: list[str]) -> None:
    name = node.get("name", "")
    total = node.get("total_count", 0)
    children = node.get("children") or []
    is_leaf = not children or name.startswith("(+")
    record = {
        "path": path + [name] if name else path,
        "name": name,
        "depth": depth,
        "total_count": total,
        "kind": (
            "truncation"
            if name.startswith("(+")
            else ("symbol" if is_leaf and "." in name else "dir" if children else "leaf")
        ),
    }
    lines.append(json.dumps(record, ensure_ascii=False))
    for child in children:
        _walk_tree(child, record["path"], depth + 1, lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Export graphify tree to JSONL")
    parser.add_argument(
        "--graph",
        type=Path,
        default=REPO_ROOT / "graphify-out" / "graph.json",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=REPO_ROOT / "graphify-out" / "graph_tree.jsonl",
    )
    args = parser.parse_args()
    if not args.graph.is_file():
        print(f"Missing graph: {args.graph}. Run: graphify update .", file=sys.stderr)
        return 1

    from graphify.tree_html import build_tree

    graph = json.loads(args.graph.read_text(encoding="utf-8"))
    tree = build_tree(graph, project_label=REPO_ROOT.name)
    lines: list[str] = []
    _walk_tree(tree, [], 0, lines)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {args.output} ({len(lines)} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
