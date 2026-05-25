# MCP setup — one curl per server

Each MCP has its **own** bootstrap command. Run from the **repository root** after `git clone`. Config uses `${workspaceFolder}` + `scripts/mcp_launcher.py` (no hardcoded `C:\` or `D:\` paths).

**Prerequisites:** Python 3.10+ on PATH, Cursor opened on this repo folder.

---

## office-leave MCP (leave tools + SQLite)

Sets up: `.venv`, `pip install -e ".[dev]"`, `.env`, `data/employees.db`, merges `office-leave` into `.cursor/mcp.json`.

### curl (macOS / Linux / Git Bash)

```bash
curl -fsSL https://raw.githubusercontent.com/devinraina258/talentserv-ai-hackathon-group-11-backend-db/main/scripts/bootstrap-office-leave-mcp.sh | bash
```

### PowerShell (Windows)

```powershell
irm https://raw.githubusercontent.com/devinraina258/talentserv-ai-hackathon-group-11-backend-db/main/scripts/bootstrap-office-leave-mcp.ps1 | iex
```

### Local (no curl)

```bash
python scripts/bootstrap_mcp.py --office-leave
```

---

## graphify MCP (code graph queries)

Sets up: `.venv`, `pip install -e ".[graphify]"`, `graphify-out/graph.json` (+ HTML/JSONL if scripts present), merges `graphify` into `.cursor/mcp.json`.

### curl (macOS / Linux / Git Bash)

```bash
curl -fsSL https://raw.githubusercontent.com/devinraina258/talentserv-ai-hackathon-group-11-backend-db/main/scripts/bootstrap-graphify-mcp.sh | bash
```

### PowerShell (Windows)

```powershell
irm https://raw.githubusercontent.com/devinraina258/talentserv-ai-hackathon-group-11-backend-db/main/scripts/bootstrap-graphify-mcp.ps1 | iex
```

### Local (no curl)

```bash
python scripts/bootstrap_mcp.py --graphify
```

Force rebuild the graph:

```bash
python scripts/bootstrap_mcp.py --graphify --force-graph
```

---

## Both MCPs at once

```bash
curl -fsSL https://raw.githubusercontent.com/devinraina258/talentserv-ai-hackathon-group-11-backend-db/main/scripts/bootstrap-mcp.sh | bash
```

```powershell
irm https://raw.githubusercontent.com/devinraina258/talentserv-ai-hackathon-group-11-backend-db/main/scripts/bootstrap-mcp.ps1 | iex
```

```bash
python scripts/bootstrap_mcp.py --all
```

Running **office-leave** then **graphify** (or the reverse) is safe — each command **merges** into `.cursor/mcp.json` without removing the other server.

---

## After any bootstrap

1. **Developer → Reload Window** in Cursor  
2. **Settings → MCP** → enable the server(s) you installed  
3. Confirm green status for **office-leave** and/or **graphify**

---

## What each bootstrap installs

| Step | office-leave | graphify |
|------|:------------:|:--------:|
| Create `.venv` | yes | yes |
| `init_db.py` → `data/employees.db` | yes | no |
| `.env` from `.env.example` | yes | no |
| `graphify update .` | no | yes |
| MCP entry in `.cursor/mcp.json` | `office-leave` | `graphify` |

Shared: `scripts/mcp_launcher.py` picks `.venv` Python on Windows and Unix.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `path not found` / Connection closed | Re-run the curl for that MCP from repo root |
| curl 404 | Push scripts to GitHub `main`, or use `python scripts/bootstrap_mcp.py --…` locally |
| office-leave tools empty | Re-run office-leave bootstrap (creates DB) |
| graphify empty graph | `python scripts/bootstrap_mcp.py --graphify --force-graph` |
| `npm.ps1` blocked (Husky only) | Use `npm.cmd install` — not required for MCP |

---

*Repo: [talentserv-ai-hackathon-group-11-backend-db](https://github.com/devinraina258/talentserv-ai-hackathon-group-11-backend-db)*
