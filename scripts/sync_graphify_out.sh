#!/usr/bin/env sh
# Regenerate graphify-out and stage tracked artifacts for the current commit.
set -eu

ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

run_graphify() {
  if command -v graphify >/dev/null 2>&1; then
    graphify "$@"
  elif [ -f ".venv/Scripts/python.exe" ] && .venv/Scripts/python.exe -c "import graphify" 2>/dev/null; then
    .venv/Scripts/python.exe -m graphify "$@"
  elif [ -f ".venv/bin/python" ] && .venv/bin/python -c "import graphify" 2>/dev/null; then
    .venv/bin/python -m graphify "$@"
  elif python -c "import graphify" 2>/dev/null; then
    python -m graphify "$@"
  else
    echo "graphify: not installed. Run: pip install graphifyy or pip install -e '.[graphify]'" >&2
    exit 1
  fi
}

if [ -f ".venv/Scripts/python.exe" ]; then
  PYTHON=".venv/Scripts/python.exe"
elif [ -f ".venv/bin/python" ]; then
  PYTHON=".venv/bin/python"
else
  PYTHON="python"
fi

echo "[graphify] updating graph (AST, no API key)..."
run_graphify update .

echo "[graphify] refreshing GRAPH_TREE.html..."
run_graphify tree --graph graphify-out/graph.json --output graphify-out/GRAPH_TREE.html

echo "[graphify] exporting graph_tree.jsonl..."
"$PYTHON" scripts/export_graph_tree_jsonl.py

echo "[graphify] staging graphify-out/ (cache and manifest are gitignored)..."
git add graphify-out/

echo "[graphify] sync complete."
