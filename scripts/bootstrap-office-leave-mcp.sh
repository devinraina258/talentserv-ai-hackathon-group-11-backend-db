#!/usr/bin/env sh
# office-leave MCP only:
#   curl -fsSL https://raw.githubusercontent.com/devinraina258/talentserv-ai-hackathon-group-11-backend-db/main/scripts/bootstrap-office-leave-mcp.sh | bash
set -eu

if [ ! -f "scripts/bootstrap_mcp.py" ]; then
  echo "[office-leave] Run from repository root (or clone the repo first)." >&2
  exit 1
fi

PY=python3
command -v python3 >/dev/null 2>&1 || PY=python
exec "$PY" scripts/bootstrap_mcp.py --office-leave
