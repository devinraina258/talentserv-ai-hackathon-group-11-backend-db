#!/usr/bin/env bash
# Clear read cache after context compaction (cache-cow)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

INPUT=$(cat 2>/dev/null || echo "{}")
CONV_ID=$(conversation_id_from "$INPUT")

if [[ -n "$CONV_ID" && -d "$CACHE_BASE/$CONV_ID" ]]; then
  CACHED_COUNT=$(find "$CACHE_BASE/$CONV_ID" -type f 2>/dev/null | wc -l | tr -d ' ')
  rm -rf "$CACHE_BASE/$CONV_ID"
  if [[ "$CACHED_COUNT" -gt 0 ]]; then
    log_hook "pre-compact: read cache cleared (${CACHED_COUNT} entries)"
    echo '{"user_message":"cache-cow: read cache cleared after compaction — re-read files only when needed."}'
    exit 0
  fi
fi

exit 0
