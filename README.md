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
pip install -e ".[dev]"
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
