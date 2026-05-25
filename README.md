# Office Leave MCP

TalentServ hackathon — FastMCP server for office leave (apply, status, balances) with a local SQLite database, Grok-powered advice, and an optional **graphify** code graph for Cursor.

**One curl per MCP** — run from **any folder** (no `git clone` first). Writes `.cursor/mcp.json` + launchers only for that directory (like Jira/Figma MCP):

**office-leave**

```bash
curl -fsSL https://raw.githubusercontent.com/devinraina258/talentserv-ai-hackathon-group-11-backend-db/main/scripts/install-office-leave-mcp.sh | bash
```

**graphify**

```bash
curl -fsSL https://raw.githubusercontent.com/devinraina258/talentserv-ai-hackathon-group-11-backend-db/main/scripts/install-graphify-mcp.sh | bash
```

Windows: `irm .../install-office-leave-mcp.ps1 | iex` and `irm .../install-graphify-mcp.ps1 | iex` — [docs/MCP_SETUP.md](docs/MCP_SETUP.md).

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
office-leave-init-db
# or: python -m src.init_db
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

## Add to Cursor

See the curl commands at the top of this README, or [docs/MCP_SETUP.md](docs/MCP_SETUP.md).

- Installs via **uvx** → **pipx** → `.cursor/mcp-venv` (auto-detect)
- **Merges** into `.cursor/mcp.json` (keeps your other MCP servers)
- Reload Cursor after install

**Developers** with a full git checkout: `python scripts/bootstrap_mcp.py --all` or `pip install -e ".[dev,graphify]"`.

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
