#!/usr/bin/env bash
# Filter verbose test output and tail log dumps (cache-cow)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

INPUT=$(cat)
COMMAND=$(shell_command_from "$INPUT")
[[ -z "$COMMAND" ]] && emit_allow

if echo "$COMMAND" | grep -qE '(pytest|python -m pytest|manage\.py test|npm test|npx jest|yarn test|vitest)'; then
  echo "$COMMAND" | grep -q "pre-shell.helper.filter" && emit_allow
  FILTER="$SCRIPT_DIR/pre-shell.helper.filter.sh"
  LIMITED="$COMMAND 2>&1 | bash \"$FILTER\""
  log_hook "pre-shell: test output filter applied"
  emit_allow_updated_shell "$LIMITED" "Test output filtered (start, failures, summary only)."
fi

if echo "$COMMAND" | grep -qE '(cat.*\.(log|out|err)|journalctl|docker logs)' && \
  ! echo "$COMMAND" | grep -qE '(head|tail|wc|-n |grep)'; then
  LIMITED="$COMMAND | tail -100"
  log_hook "pre-shell: log output limited to tail -100"
  emit_allow_updated_shell "$LIMITED" "Output limited to last 100 lines to save tokens."
fi

emit_allow
