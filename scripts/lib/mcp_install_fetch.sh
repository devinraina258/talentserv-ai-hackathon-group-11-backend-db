#!/usr/bin/env sh
# Shared fetch helper for clone-free MCP installers (sourced, not executed alone).
MCP_INSTALL_RAW_BASE="${MCP_INSTALL_RAW_BASE:-https://raw.githubusercontent.com/devinraina258/talentserv-ai-hackathon-group-11-backend-db/main}"

mcp_install_run_python() {
  CMD="$1"
  WS="${2:-$(pwd)}"
  if [ -f "scripts/mcp_install_lib.py" ]; then
    PY=python3
    command -v python3 >/dev/null 2>&1 || PY=python
    exec "$PY" scripts/mcp_install_lib.py "$CMD" "$WS"
  fi
  TMP="${TMPDIR:-/tmp}/mcp-install-$$"
  mkdir -p "$TMP"
  trap 'rm -rf "$TMP"' EXIT
  curl -fsSL "$MCP_INSTALL_RAW_BASE/scripts/mcp_install_lib.py" -o "$TMP/mcp_install_lib.py"
  PY=python3
  command -v python3 >/dev/null 2>&1 || PY=python
  exec "$PY" "$TMP/mcp_install_lib.py" "$CMD" "$WS"
}
