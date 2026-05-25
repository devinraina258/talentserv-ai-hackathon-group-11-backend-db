#!/usr/bin/env bash
# Shared helpers — adapted from https://github.com/soonswan-study/cache-cow (MIT)
set -euo pipefail

CACHE_COW_LOG="${CURSOR_HOOK_LOG:-${TMPDIR:-${TEMP:-/tmp}}/cursor-hooks.log}"
CACHE_BASE="${CURSOR_READ_CACHE:-${TMPDIR:-${TEMP:-/tmp}}/cursor-read-cache}"

log_hook() {
  echo "[$(date +%H:%M:%S)] $*" >> "$CACHE_COW_LOG"
}

conversation_id_from() {
  local input="$1"
  if command -v jq &>/dev/null; then
    echo "$input" | jq -r '.conversation_id // .session_id // ""'
  else
    echo "$input" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('conversation_id') or d.get('session_id') or '')"
  fi
}

file_path_from() {
  local input="$1"
  if command -v jq &>/dev/null; then
    echo "$input" | jq -r '.tool_input.path // .tool_input.file_path // ""'
  else
    echo "$input" | python3 -c "
import sys,json
d=json.load(sys.stdin)
ti=d.get('tool_input') or {}
print(ti.get('path') or ti.get('file_path') or '')
"
  fi
}

offset_from() {
  local input="$1"
  if command -v jq &>/dev/null; then
    echo "$input" | jq -r '.tool_input.offset // ""'
  else
    echo "$input" | python3 -c "import sys,json; print((json.load(sys.stdin).get('tool_input') or {}).get('offset',''))"
  fi
}

limit_from() {
  local input="$1"
  if command -v jq &>/dev/null; then
    echo "$input" | jq -r '.tool_input.limit // ""'
  else
    echo "$input" | python3 -c "import sys,json; print((json.load(sys.stdin).get('tool_input') or {}).get('limit',''))"
  fi
}

is_write_from() {
  local input="$1"
  if command -v jq &>/dev/null; then
    echo "$input" | jq -r 'if (.tool_input.content != null) or (.tool_input.new_string != null) or (.tool_input.old_string != null) then "true" else "false" end'
  else
    echo "$input" | python3 -c "
import sys,json
ti=json.load(sys.stdin).get('tool_input') or {}
print('true' if any(ti.get(k) is not None for k in ('content','new_string','old_string')) else 'false')
"
  fi
}

shell_command_from() {
  local input="$1"
  if command -v jq &>/dev/null; then
    echo "$input" | jq -r '.tool_input.command // .command // ""'
  else
    echo "$input" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print((d.get('tool_input') or {}).get('command') or d.get('command') or '')
"
  fi
}

cache_key_for() {
  local file_path="$1"
  if command -v md5 &>/dev/null; then
    echo -n "$file_path" | md5 -q
  elif command -v md5sum &>/dev/null; then
    echo -n "$file_path" | md5sum | cut -d' ' -f1
  else
    echo -n "$file_path" | sed 's/[^a-zA-Z0-9]/_/g'
  fi
}

should_skip_file() {
  local file_path="$1"
  case "$file_path" in
    *.png|*.jpg|*.jpeg|*.gif|*.svg|*.ico|*.pdf|*.lock|*.min.js|*.min.css|*.map) return 0 ;;
    graphify-out/cache/*|graphify-out/*.html) return 0 ;;
  esac
  return 1
}

emit_allow() {
  exit 0
}

emit_deny() {
  local message="$1"
  if command -v jq &>/dev/null; then
    jq -n --arg m "$message" '{permission:"deny",agent_message:$m,user_message:$m}'
  else
    python3 -c "import json,sys; m=sys.argv[1]; print(json.dumps({'permission':'deny','agent_message':m,'user_message':m}))" "$message"
  fi
  exit 0
}

emit_allow_note() {
  local message="$1"
  if command -v jq &>/dev/null; then
    jq -n --arg m "$message" '{permission:"allow",agent_message:$m}'
  else
    python3 -c "import json,sys; m=sys.argv[1]; print(json.dumps({'permission':'allow','agent_message':m}))" "$message"
  fi
  exit 0
}

emit_allow_updated_shell() {
  local command="$1"
  local note="$2"
  if command -v jq &>/dev/null; then
    jq -n --arg cmd "$command" --arg note "$note" \
      '{permission:"allow",updated_input:{command:$cmd},agent_message:$note}'
  else
    python3 -c "import json,sys; print(json.dumps({'permission':'allow','updated_input':{'command':sys.argv[1]},'agent_message':sys.argv[2]}))" "$command" "$note"
  fi
  exit 0
}
