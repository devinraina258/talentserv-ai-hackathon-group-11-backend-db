#!/usr/bin/env bash
# Cache reads and invalidate on writes (cache-cow)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

INPUT=$(cat)
CONV_ID=$(conversation_id_from "$INPUT")
FILE_PATH=$(file_path_from "$INPUT")
OFFSET=$(offset_from "$INPUT")
LIMIT=$(limit_from "$INPUT")
IS_WRITE=$(is_write_from "$INPUT")

[[ -z "$FILE_PATH" ]] && emit_allow
[[ ! -f "$FILE_PATH" ]] && emit_allow
[[ -z "$CONV_ID" ]] && emit_allow
should_skip_file "$FILE_PATH" && emit_allow

FNAME=$(basename "$FILE_PATH")
CACHE_DIR="$CACHE_BASE/$CONV_ID"
mkdir -p "$CACHE_DIR"
CACHE_KEY=$(cache_key_for "$FILE_PATH")
CACHE_FILE="$CACHE_DIR/$CACHE_KEY"

_merge_ranges() {
  local ranges_file="$1"
  local tmp="${ranges_file}.tmp"
  grep -v '^\s*$' "$ranges_file" | sort -n -k1,1 -k2,2 | awk '
    BEGIN { n=0 }
    {
      s=$1; e=$2
      if (n==0) { rs[0]=s; re[0]=e; n=1 }
      else if (s <= re[n-1]+1) { if (e > re[n-1]) re[n-1]=e }
      else { rs[n]=s; re[n]=e; n++ }
    }
    END { for(i=0;i<n;i++) print rs[i], re[i] }
  ' > "$tmp" || { rm -f "$tmp"; return 0; }
  [[ -s "$tmp" ]] && mv "$tmp" "$ranges_file" || rm -f "$tmp"
}

if [[ "$IS_WRITE" == "true" ]]; then
  if [[ -f "$CACHE_FILE" ]]; then
    cp "$FILE_PATH" "$CACHE_FILE"
  fi
  rm -f "$CACHE_DIR/${CACHE_KEY}.snapshot" "$CACHE_DIR/${CACHE_KEY}.ranges"
  log_hook "post-file-cache: cache updated + ranges invalidated (${FNAME})"
  emit_allow
fi

RANGES_FILE="$CACHE_DIR/${CACHE_KEY}.ranges"
SNAPSHOT_FILE="$CACHE_DIR/${CACHE_KEY}.snapshot"

IS_PARTIAL=false
[[ -n "$OFFSET" && "$OFFSET" != "null" ]] && IS_PARTIAL=true
[[ -n "$LIMIT" && "$LIMIT" != "null" ]] && IS_PARTIAL=true

if [[ "$IS_PARTIAL" == "true" ]]; then
  OFFSET_NUM=${OFFSET:-0}
  if [[ -n "$LIMIT" && "$LIMIT" != "null" ]]; then
    LIMIT_NUM=$LIMIT
  else
    LIMIT_NUM=$(wc -l < "$FILE_PATH" | tr -d ' ')
  fi
  [[ "$LIMIT_NUM" -le 0 ]] && emit_allow
  START=$((OFFSET_NUM + 1))
  END=$((OFFSET_NUM + LIMIT_NUM))
  cp "$FILE_PATH" "$SNAPSHOT_FILE"
  echo "$START $END" >> "$RANGES_FILE"
  _merge_ranges "$RANGES_FILE"
  log_hook "post-file-cache: partial range cached (${FNAME} ${START}-${END})"
else
  TOTAL=$(wc -l < "$FILE_PATH" | tr -d ' ')
  cp "$FILE_PATH" "$CACHE_FILE"
  echo "1 $TOTAL" > "$RANGES_FILE"
  rm -f "$SNAPSHOT_FILE"
  log_hook "post-file-cache: full read cached (${FNAME})"
fi

emit_allow
