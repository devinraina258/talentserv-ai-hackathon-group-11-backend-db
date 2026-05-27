# Microsoft Teams integration (Incoming Webhook)

Post leave lifecycle updates to a **Teams channel** when MCP tools mutate leave data. Uses Microsoft **Incoming Webhooks** (pre-authorized URL, no OAuth flow in this demo). Same SQLite DB as Cursor MCP and WhatsApp.

## What gets notified

| MCP tool | Teams message |
|----------|----------------|
| `apply_leave` | New request (channel + optional manager webhook) |
| `approve_leave` | Approved |
| `reject_leave` | Rejected |
| `announce_holiday` | Company holiday announcement |

Notifications are **best-effort**: webhook failures are logged; MCP tool responses still succeed. If `TEAMS_WEBHOOK_URL` is unset, notifications are skipped with a warning in logs.

## Architecture

```text
Cursor MCP (stdio)
    → src/server.py (FastMCP tools)
    → src/tools/leave_tools.py (DB + format message)
    → src/services/teams_service.py (POST JSON to webhook)
    → Microsoft Teams channel
```

Implementation: [`src/services/teams_service.py`](../src/services/teams_service.py), [`src/tools/leave_tools.py`](../src/tools/leave_tools.py).

## Prerequisites

- Python 3.10+ with project installed (`pip install -e ".[dev]"` — `requests` is a core dependency)
- A Teams team/channel where you can add an **Incoming Webhook** connector
- `.env` with `TEAMS_WEBHOOK_URL` (see below)

## 1. Create a Teams Incoming Webhook

1. In Microsoft Teams, open the target **channel**.
2. Channel menu → **Connectors** / **Workflows** (UI varies by tenant) → **Incoming Webhook**.
3. Name it (e.g. `Office Leave`) and create the webhook.
4. Copy the HTTPS URL (looks like `https://….webhook.office.com/webhookb2/…`).

Microsoft docs: [Create an Incoming Webhook](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook).

## 2. Configure environment

```bash
copy .env.example .env
```

Edit `.env`:

```env
TEAMS_WEBHOOK_URL=https://your-tenant.webhook.office.com/webhookb2/...
TEAMS_WEBHOOK_TIMEOUT_SECONDS=5
# Optional: Adaptive Cards instead of plain text
TEAMS_USE_ADAPTIVE_CARD=0

# Optional: separate manager channel
TEAMS_MANAGER_WEBHOOK_URL=
# Or per department (JSON object):
# TEAMS_MANAGER_WEBHOOK_URL_BY_DEPARTMENT={"Engineering":"https://...","Product":"https://..."}
```

Reload Cursor after changing `.env` so the MCP server picks up values (`OFFICE_LEAVE_WORKSPACE` / workspace `.env`).

**Security:** Treat webhook URLs like secrets. Do not commit real URLs to git; use `.env` only.

## 3. Smoke test (connection)

From repo root with venv active and `.env` loaded:

```bash
python -c "from src.services.teams_service import send_teams_connection_test; send_teams_connection_test()"
```

You should see **Office Leave — Teams connected** in the channel, listing what events will be posted.

## 4. Demo flow in Cursor

With **office-leave** MCP enabled and `TEAMS_WEBHOOK_URL` set:

1. **Apply leave** — e.g. `apply sick leave for devin 2026-06-03 to 2026-06-03, reason: fever`  
   → Channel: *Office Leave — New leave request* (pending).  
   → Manager webhook (if configured): *Manager action needed*.

2. **Approve or reject** — e.g. `approve leave request 5`  
   → Channel: *Leave approved* (balance updated on approve).

3. **Holiday** — e.g. `announce holiday 2026-12-25 Office closed`  
   → Channel: *Company holiday announced*.

Use `list_leave_requests` / `check_leave_status` to find `request_id` values.

## Message format

Plain text by default. Optional Adaptive Card wrapper when `TEAMS_USE_ADAPTIVE_CARD=1`.

Leave messages include employee name, department (from DB), leave type, dates, days, reason, and status line. Manager copies use audience-specific titles (*Manager action needed* vs *New leave request*).

## Manager notifications

The database does not model individual managers. Optional manager routing:

1. **`TEAMS_MANAGER_WEBHOOK_URL`** — single extra webhook for all manager-style messages.
2. **`TEAMS_MANAGER_WEBHOOK_URL_BY_DEPARTMENT`** — JSON map `{"Engineering":"https://...","Product":"https://..."}` keyed by employee department from seed data.

On `apply_leave`, the channel webhook receives the employee-facing text; the manager webhook receives the approval-oriented copy.

## MCP tools reference

| Tool | Description |
|------|-------------|
| `apply_leave` | Submit pending leave; notifies Teams |
| `approve_leave` | Approve by `request_id`; notifies Teams |
| `reject_leave` | Reject by `request_id`; notifies Teams |
| `announce_holiday` | Persist holiday + notify Teams |

Other tools (`get_leave_balance`, `advise_on_leave`, etc.) do not post to Teams.

## Troubleshooting

| Symptom | Check |
|---------|--------|
| No messages in Teams | `TEAMS_WEBHOOK_URL` set in workspace `.env`; reload Cursor |
| HTTP 4xx in logs | Webhook URL expired or revoked — recreate connector |
| `requests` import error | `pip install -e .` (core dep includes `requests`) |
| Manager copy missing | `TEAMS_MANAGER_WEBHOOK_URL` or department map set and valid JSON |

## Related docs

- [README.md](../README.md) — project overview
- [WHATSAPP_DEMO.md](WHATSAPP_DEMO.md) — employee messaging channel
- [DEMO_QUICKSTART.md](DEMO_QUICKSTART.md) — combined demo script
- [HACKATHON_SUBMISSION.md](HACKATHON_SUBMISSION.md) — submission architecture
