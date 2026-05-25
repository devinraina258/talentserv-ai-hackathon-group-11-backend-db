#!/usr/bin/env sh
# Clone-free: configure office-leave MCP in the current directory only.
#   curl -fsSL https://raw.githubusercontent.com/devinraina258/talentserv-ai-hackathon-group-11-backend-db/main/scripts/install-office-leave-mcp.sh | bash
set -eu
if [ -f "scripts/mcp_install_lib.py" ]; then
  PY=python3
  command -v python3 >/dev/null 2>&1 || PY=python
  exec "$PY" scripts/mcp_install_lib.py office-leave "$(pwd)"
fi
TMP="${TMPDIR:-/tmp}/mcp-install-$$"
mkdir -p "$TMP"
trap 'rm -rf "$TMP"' EXIT
BASE="${MCP_INSTALL_RAW_BASE:-https://raw.githubusercontent.com/devinraina258/talentserv-ai-hackathon-group-11-backend-db/main}"
curl -fsSL "$BASE/scripts/mcp_install_lib.py" -o "$TMP/mcp_install_lib.py"
PY=python3
command -v python3 >/dev/null 2>&1 || PY=python
exec "$PY" "$TMP/mcp_install_lib.py" office-leave "$(pwd)"
