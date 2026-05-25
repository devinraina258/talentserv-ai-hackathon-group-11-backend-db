# Office Leave MCP

TalentServ hackathon — FastMCP server for office leave (apply, status, balances) with a local SQLite database, Grok-powered advice, and an optional **graphify** code graph for Cursor.

**One curl per MCP** (run from repo root after clone; portable `.cursor/mcp.json`, no hardcoded paths):

**office-leave**

```bash
curl -fsSL https://raw.githubusercontent.com/devinraina258/talentserv-ai-hackathon-group-11-backend-db/main/scripts/bootstrap-office-leave-mcp.sh | bash
```

**graphify**

```bash
curl -fsSL https://raw.githubusercontent.com/devinraina258/talentserv-ai-hackathon-group-11-backend-db/main/scripts/bootstrap-graphify-mcp.sh | bash
```

Windows: `irm .../bootstrap-office-leave-mcp.ps1 | iex` and `irm .../bootstrap-graphify-mcp.ps1 | iex` — [docs/MCP_SETUP.md](docs/MCP_SETUP.md).

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

## Add to Cursor (one curl per MCP)

From the **repository root** (after `git clone`). Each command creates `.venv`, installs what that server needs, and **merges** into `.cursor/mcp.json` (portable paths, no `D:\...` hardcoding).

### office-leave only

```bash
curl -fsSL https://raw.githubusercontent.com/devinraina258/talentserv-ai-hackathon-group-11-backend-db/main/scripts/bootstrap-office-leave-mcp.sh | bash
```

```powershell
irm https://raw.githubusercontent.com/devinraina258/talentserv-ai-hackathon-group-11-backend-db/main/scripts/bootstrap-office-leave-mcp.ps1 | iex
```

### graphify only

```bash
curl -fsSL https://raw.githubusercontent.com/devinraina258/talentserv-ai-hackathon-group-11-backend-db/main/scripts/bootstrap-graphify-mcp.sh | bash
```

```powershell
irm https://raw.githubusercontent.com/devinraina258/talentserv-ai-hackathon-group-11-backend-db/main/scripts/bootstrap-graphify-mcp.ps1 | iex
```

### Both MCPs

```bash
curl -fsSL https://raw.githubusercontent.com/devinraina258/talentserv-ai-hackathon-group-11-backend-db/main/scripts/bootstrap-mcp.sh | bash
```

Then **Developer → Reload Window** and enable the server(s) you installed.

Details: [docs/MCP_SETUP.md](docs/MCP_SETUP.md) · Local: `python scripts/bootstrap_mcp.py --office-leave` / `--graphify` / `--all`

Copy [.cursor/mcp.json.example](.cursor/mcp.json.example) to `.cursor/mcp.json` if you prefer manual setup (both **office-leave** and **graphify** use `scripts/mcp_launcher.py`).

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
