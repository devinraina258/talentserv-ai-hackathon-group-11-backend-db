# cache-cow hooks (Cursor)

Token-saving hooks adapted from [soonswan-study/cache-cow](https://github.com/soonswan-study/cache-cow) for **Cursor** (not Claude Code). They live in this repo under `.cursor/hooks/` and activate when you open the project in Cursor.

**Runtime:** Python 3 hooks (`.cursor/hooks/*.py`) — no `jq` or Git Bash required on Windows. Bash scripts (`.sh`) are kept for reference / macOS/Linux parity with [upstream cache-cow](https://github.com/soonswan-study/cache-cow).

## What it does

| Hook | Cursor event | Behavior |
|------|----------------|----------|
| `session-start.sh` | `sessionStart` | Clears per-chat read cache; removes caches older than 7 days |
| `pre-read.sh` | `preToolUse` (Read) | Blocks re-reads of unchanged files; shows diff if changed; blocks full reads of files &gt;1000 lines; blocks duplicate partial ranges |
| `post-file-cache.sh` | `postToolUse` (Read/Write/StrReplace) | Caches reads and range metadata; invalidates on writes |
| `pre-shell.sh` | `preToolUse` (Shell) | Filters pytest/jest/vitest output; appends `tail -100` to raw log commands |
| `pre-compact.sh` | `preCompact` | Clears read cache after context compaction |

## Prerequisites

- **Cursor** with hooks enabled (Settings → Hooks)
- **Python 3.10+** on `PATH` as `python` (same as the rest of this repo)

Optional: **Git Bash** only if you switch `hooks.json` to the `.sh` variants; **jq** only for those bash hooks.

## Verify

1. Reload Cursor after pulling: **Developer → Reload Window**
2. Open **Settings → Hooks** and confirm entries from `.cursor/hooks.json`
3. Start a new Agent chat and watch the log:

```powershell
Get-Content $env:TEMP\cursor-hooks.log -Wait -Tail 20
```

On Git Bash: `tail -f "${TMPDIR:-/tmp}/cursor-hooks.log"`

Expected log lines include `session-start:`, `pre-read: cache hit`, `post-file-cache: full read cached`.

## Configuration

| Setting | Default | File |
|---------|---------|------|
| Large-file line threshold | 1000 | `.cursor/hooks/pre-read.sh` |
| Log tail limit | 100 | `.cursor/hooks/pre-shell.sh` |
| Cache directory | `%TEMP%\cursor-read-cache` (Windows) or `/tmp/cursor-read-cache` | env `CURSOR_READ_CACHE` |
| Log file | `%TEMP%\cursor-hooks.log` | env `CURSOR_HOOK_LOG` |

Skipped paths include common binaries and `graphify-out/cache/*`, `graphify-out/*.html`.

## Make scripts executable (Git on Windows)

If hooks do not run, mark scripts executable once:

```bash
git update-index --chmod=+x .cursor/hooks/*.sh
```

Or in Git Bash from the repo root:

```bash
chmod +x .cursor/hooks/*.sh
```

## Upstream

To pull hook logic updates from upstream cache-cow, compare `hooks/` in that repo with `.cursor/hooks/` here (Cursor uses `conversation_id`, `tool_input.path`, and JSON `permission` responses instead of Claude’s `session_id` / `file_path` / exit code 2).

License: MIT (same as upstream cache-cow).
