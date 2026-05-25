#!/usr/bin/env bash
# Clear per-conversation read cache on session start (cache-cow)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

INPUT=$(cat)
CONV_ID=$(conversation_id_from "$INPUT")

mkdir -p "$CACHE_BASE"
if [[ -n "$CONV_ID" && -d "$CACHE_BASE/$CONV_ID" ]]; then
  CACHED_COUNT=$(find "$CACHE_BASE/$CONV_ID" -type f 2>/dev/null | wc -l | tr -d ' ')
  rm -rf "$CACHE_BASE/$CONV_ID"
  log_hook "session-start: read cache cleared (${CACHED_COUNT} entries)"
else
  log_hook "session-start: no cache to clear"
fi

# Remove stale caches (>7 days)
find "$CACHE_BASE" -mindepth 1 -maxdepth 1 -type d -mtime +7 -exec rm -rf {} + 2>/dev/null || true

echo '{"additional_context":"cache-cow: read cache initialized. Do not re-read unchanged files; use offset/limit for files over 1000 lines."}'
exit 0
