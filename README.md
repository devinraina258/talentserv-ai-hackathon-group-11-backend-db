# Office Leave MCP

TalentServ hackathon — FastMCP server for office leave (apply, status, balances) with a local SQLite database and Grok-powered advice.

## Prerequisites

- Python 3.10+
- [Grok API key](https://console.x.ai) (optional; fallback rules work without it)
- [Cursor](https://cursor.com) or another MCP host

## Quick start

```bash
git clone https://github.com/devinraina258/talentserv-ai-hackathon-group-11-backend-db.git
cd talentserv-ai-hackathon-group-11-backend-db
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev,graphify]"
```

### 1. Create the database

```bash
python scripts/init_db.py
```

Creates `data/employees.db` with three employees: **devin**, **nisha**, **gautam**.

### 2. Environment

```bash
copy .env.example .env
```

Edit `.env` and set `GROK_API_KEY` for live AI advice on `advise_on_leave`.

### 3. Run tests

```bash
pytest
```

### 4. Run the MCP server (stdio)

```bash
python -m src.server
```

Or:

```bash
fastmcp run src/server.py
```

## Knowledge graph ([graphify](https://github.com/safishamsi/graphify))

This repo includes a pre-built code graph so Cursor can query structure instead of grepping files (fewer tokens, faster answers).

| Artifact | Purpose |
|----------|---------|
| `graphify-out/graph.json` | Full graph (nodes, edges, communities) |
| `graphify-out/GRAPH_REPORT.md` | God nodes, surprising links, suggested questions |
| `graphify-out/graph_tree.jsonl` | Compact directory/symbol tree (one JSON object per line) |
| `graphify-out/graph.html` | Interactive graph in a browser |
| `graphify-out/GRAPH_TREE.html` | Collapsible module tree |

**Install graphify + Husky (once per machine):**

```bash
pip install "graphifyy[mcp]>=0.8.14"
# or: uv tool install graphifyy
graphify cursor install   # writes .cursor/rules/graphify.mdc (query-first for agents)
npm install               # installs Husky; prepare script wires git pre-commit
```

Optional: `graphify hook uninstall` if you previously ran `graphify hook install` — Husky pre-commit replaces the post-commit rebuild and keeps `graphify-out/` in the **same** commit as your code.

**Automatic updates (no manual refresh):**

| When | What runs |
|------|-----------|
| Every `git commit` | Husky **pre-commit** → `scripts/sync_graphify_out.sh` → stages `graphify-out/` |
| Every **PR** (and pushes to `main`/`master`) | GitHub Action [`.github/workflows/graphify.yml`](.github/workflows/graphify.yml) rebuilds and pushes `graphify-out` to the branch |

Manual sync only if hooks are skipped (`git commit --no-verify`):

```bash
npm run graphify:sync
```

**Query from the terminal (scoped subgraph, not full-repo grep):**

```bash
graphify query "how does apply_leave connect to the database?"
graphify path "apply_leave" "connect"
graphify explain "advise_on_leave"
```

**MCP:** Copy [.cursor/mcp.json.example](.cursor/mcp.json.example) to `.cursor/mcp.json` — it includes an optional `graphify` server (`query_graph`, `get_neighbors`, `shortest_path`, etc.) alongside `office-leave`.

## Add to Cursor

Copy the example config and adjust paths:

```bash
copy .cursor\mcp.json.example .cursor\mcp.json
```

Or paste into Cursor MCP settings — use your venv Python and repo `cwd` (see [.cursor/mcp.json.example](.cursor/mcp.json.example)). Restart Cursor after saving.

On Windows, if `python` is not on PATH, use `.venv\Scripts\python.exe` as the command.

## MCP tools

| Tool | Description |
|------|-------------|
| `list_employees` | All employees with balances |
| `get_employee` | Profile + balances |
| `get_leave_balance` | Annual/sick remaining |
| `apply_leave` | Submit pending leave (ISO dates `YYYY-MM-DD`) |
| `check_leave_status` | By `request_id` or latest for `employee` |
| `list_leave_requests` | History with optional filters |
| `advise_on_leave` | Grok guidance from DB context |

## MCP resources

- `leave://employees` — employee directory
- `leave://policy` — leave rules

## Example prompts in Cursor

- "What is Nisha's leave balance?"
- "Apply 2 days annual leave for Gautam from 2026-06-10 to 2026-06-11, reason: family event"
- "Check the latest leave status for Devin"
- "Should Devin take leave next week given his balance?"

## Employees (seed data)

| Slug | Name | Department | Annual | Sick |
|------|------|------------|--------|------|
| devin | Devin | Engineering | 12 | 5 |
| nisha | Nisha | Product | 10 | 4 |
| gautam | Gautam | Operations | 14 | 6 |

Pending requests do not reduce balance until approved (demo/local only; no auth on employee slug).

## Publish to GitHub

```bash
gh auth login
gh repo create talentserv-ai-hackathon-group-11-backend-db --public --source=. --remote=origin --push
```

## License

MIT
