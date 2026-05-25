#!/usr/bin/env bash
# Block redundant reads, large full reads, and duplicate partial ranges (cache-cow)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

INPUT=$(cat)
CONV_ID=$(conversation_id_from "$INPUT")
FILE_PATH=$(file_path_from "$INPUT")
OFFSET=$(offset_from "$INPUT")
LIMIT=$(limit_from "$INPUT")

[[ -z "$FILE_PATH" ]] && emit_allow
[[ ! -f "$FILE_PATH" ]] && emit_allow
[[ -z "$CONV_ID" ]] && emit_allow
should_skip_file "$FILE_PATH" && emit_allow

IS_PARTIAL=false
[[ -n "$OFFSET" && "$OFFSET" != "null" ]] && IS_PARTIAL=true
[[ -n "$LIMIT" && "$LIMIT" != "null" ]] && IS_PARTIAL=true

FNAME=$(basename "$FILE_PATH")
CACHE_DIR="$CACHE_BASE/$CONV_ID"
mkdir -p "$CACHE_DIR"
CACHE_KEY=$(cache_key_for "$FILE_PATH")
CACHE_FILE="$CACHE_DIR/$CACHE_KEY"

if [[ "$IS_PARTIAL" == "false" ]]; then
  LINE_COUNT=$(wc -l < "$FILE_PATH" 2>/dev/null || echo "0")
  LINE_COUNT=$(echo "$LINE_COUNT" | tr -d ' ')
  if [[ "$LINE_COUNT" -gt 1000 ]]; then
    MSG="This file has ${LINE_COUNT} lines. Use offset/limit to read only the section you need."
    log_hook "pre-read: blocked large file ${FNAME} (${LINE_COUNT} lines)"
    emit_deny "$MSG"
  fi
fi

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

  SNAPSHOT_FILE="$CACHE_DIR/${CACHE_KEY}.snapshot"
  RANGES_FILE="$CACHE_DIR/${CACHE_KEY}.ranges"

  if [[ -f "$SNAPSHOT_FILE" && -f "$RANGES_FILE" ]]; then
    if diff -q "$SNAPSHOT_FILE" "$FILE_PATH" > /dev/null 2>&1; then
      while read -r rs re; do
        [[ -z "$rs" || -z "$re" ]] && continue
        if [[ "$rs" -le "$START" && "$re" -ge "$END" ]]; then
          MSG="Range already read (lines ${START}-${END}): $FILE_PATH. No changes since last read — use Edit/Write instead of re-reading."
          log_hook "pre-read: partial range cache hit (${FNAME} ${START}-${END})"
          emit_deny "$MSG"
        fi
      done < "$RANGES_FILE"
    else
      DIFF=$(diff --unified=3 "$SNAPSHOT_FILE" "$FILE_PATH" 2>/dev/null || true)
      rm -f "$RANGES_FILE"
      log_hook "pre-read: partial read change detected (${FNAME})"
      emit_allow_note "Showing changes since last read: $FILE_PATH
---
$DIFF
---
Above diff shows changes since your last read."
    fi
  elif [[ -f "$CACHE_FILE" && -f "$RANGES_FILE" ]]; then
    if diff -q "$CACHE_FILE" "$FILE_PATH" > /dev/null 2>&1; then
      while read -r rs re; do
        [[ -z "$rs" || -z "$re" ]] && continue
        if [[ "$rs" -le "$START" && "$re" -ge "$END" ]]; then
          MSG="Range already read (lines ${START}-${END}): $FILE_PATH. No changes since last read."
          log_hook "pre-read: post-full-read partial range hit (${FNAME} ${START}-${END})"
          emit_deny "$MSG"
        fi
      done < "$RANGES_FILE"
    else
      DIFF=$(diff --unified=3 "$CACHE_FILE" "$FILE_PATH" 2>/dev/null || true)
      cp "$FILE_PATH" "$CACHE_FILE"
      rm -f "$RANGES_FILE"
      log_hook "pre-read: post-full-read partial change (${FNAME})"
      emit_allow_note "Showing changes since last read: $FILE_PATH
---
$DIFF
---"
    fi
  fi
  emit_allow
fi

[[ ! -f "$CACHE_FILE" ]] && emit_allow

if diff -q "$CACHE_FILE" "$FILE_PATH" > /dev/null 2>&1; then
  MSG="File unchanged (re-read unnecessary): $FILE_PATH. Use Edit/Write to modify."
  log_hook "pre-read: cache hit, blocked re-read (${FNAME})"
  emit_deny "$MSG"
fi

DIFF=$(diff --unified=3 "$CACHE_FILE" "$FILE_PATH" 2>/dev/null || true)
cp "$FILE_PATH" "$CACHE_FILE"
log_hook "pre-read: full read change detected (${FNAME})"
emit_allow_note "Showing changes since last read: $FILE_PATH
---
$DIFF
---
Above diff shows changes since your last read."
