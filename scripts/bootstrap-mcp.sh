#!/usr/bin/env sh
# Portable MCP bootstrap — safe to pipe from curl:
#   curl -fsSL https://raw.githubusercontent.com/devinraina258/talentserv-ai-hackathon-group-11-backend-db/main/scripts/bootstrap-mcp.sh | bash
#
# From an existing clone (repo root):
#   curl -fsSL .../bootstrap-mcp.sh | bash
#   ./scripts/bootstrap-mcp.sh
set -eu

REPO_URL="${REPO_URL:-https://github.com/devinraina258/talentserv-ai-hackathon-group-11-backend-db.git}"
BRANCH="${BRANCH:-main}"
CLONE_DIR="${CLONE_DIR:-}"

if [ -n "${1:-}" ] && [ "${1:-}" != "--here" ]; then
  case "$1" in
    --clone)
      CLONE_DIR="${2:-talentserv-ai-hackathon-group-11-backend-db}"
      ;;
    --help|-h)
      echo "Usage:"
      echo "  curl ... | bash              # bootstrap current directory (must be repo root)"
      echo "  curl ... | bash -s -- --here # same"
      echo "  curl ... | bash -s -- --clone [dir]  # git clone then bootstrap"
      exit 0
      ;;
  esac
fi

if [ "${1:-}" = "--clone" ] || [ -n "$CLONE_DIR" ]; then
  TARGET="${CLONE_DIR:-talentserv-ai-hackathon-group-11-backend-db}"
  if [ ! -d "$TARGET/.git" ]; then
    echo "[bootstrap] cloning $REPO_URL -> $TARGET"
    git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$TARGET" || git clone --depth 1 "$REPO_URL" "$TARGET"
  fi
  cd "$TARGET"
else
  # When piped from curl, cwd may not be the repo — detect via this script if present
  if [ -f "scripts/bootstrap_mcp.py" ]; then
    : # already in repo root
  elif [ -f "scripts/bootstrap-mcp.sh" ]; then
    :
  else
    echo "[bootstrap] Run from the repository root, or use: bash -s -- --clone" >&2
    exit 1
  fi
fi

if ! command -v python3 >/dev/null 2>&1 && ! command -v python >/dev/null 2>&1; then
  echo "[bootstrap] Python 3.10+ is required. Install from https://www.python.org/downloads/" >&2
  exit 1
fi

PY=python3
command -v python3 >/dev/null 2>&1 || PY=python

echo "[bootstrap] using $("$PY" --version)"
exec "$PY" scripts/bootstrap_mcp.py --all
