# Demo quickstart (5 min)

## One command (recommended)

From repo root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\demo.ps1
```

Checks venv, deps, `.env`, database, cloudflared; starts webhook + tunnel. Copy the `trycloudflare.com` URL into Twilio. Prerequisites only: `.\scripts\demo.ps1 -CheckOnly`

---

## Manual (3 terminals)

Use **PowerShell**. Run from repo root:

```powershell
cd C:\Users\Admin\Documents\talentserv-ai-hackathon-group-11-backend-db
$py = ".\.cursor\mcp-venv\Scripts\python.exe"
$cf = "C:\Program Files (x86)\cloudflared\cloudflared.exe"
```

If `cloudflared` is missing, install once: `winget install Cloudflare.cloudflared -e`

If `$py` is missing: `python -m venv .cursor\mcp-venv` then `& $py -m pip install -e ".[whatsapp]"`

---

## Before demo (once)

```powershell
& $py -m pip install -e ".[whatsapp]"
copy .env.example .env          # Twilio + WHATSAPP_PHONE_MAP
& $py -m src.init_db
```

On phone: join Twilio sandbox (`join <code>` → sandbox number).

---

## Every demo — 3 terminals (copy-paste)

**Terminal 1 — webhook**

```powershell
cd C:\Users\Admin\Documents\talentserv-ai-hackathon-group-11-backend-db
.\.cursor\mcp-venv\Scripts\python.exe -m uvicorn src.whatsapp.twilio_webhook:app --host 0.0.0.0 --port 8000
```

**Terminal 2 — HTTPS tunnel**

```powershell
& "C:\Program Files (x86)\cloudflared\cloudflared.exe" tunnel --url http://127.0.0.1:8000
```

Copy the `https://….trycloudflare.com` line from the output.

**Terminal 3 — MCP (optional, Cursor demo)**

```powershell
cd C:\Users\Admin\Documents\talentserv-ai-hackathon-group-11-backend-db
.\.cursor\mcp-venv\Scripts\python.exe -m src.server
```

Reload Cursor MCP after `.env` changes.

---

## Twilio

[WhatsApp Sandbox](https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn) → **When a message comes in** (POST):

```text
https://YOUR-NEW-URL.trycloudflare.com/whatsapp/webhook
```

Browser check: open that URL → `{"status":"ok",...}`

---

## WhatsApp

`help` → `balance` → `status` → `apply annual 2026-06-10 2026-06-11 demo reason`

---

## Microsoft Teams (optional)

Requires `TEAMS_WEBHOOK_URL` in `.env` (Incoming Webhook from your Teams channel). See [TEAMS_INTEGRATION.md](TEAMS_INTEGRATION.md).

**Smoke test** (repo root, venv python):

```powershell
& $py -c "from src.services.teams_service import send_teams_connection_test; send_teams_connection_test()"
```

**Cursor MCP demo** (Terminal 3 or chat): apply leave → watch Teams channel → `approve leave request <id>`.

Example prompts: *apply sick leave for devin 2026-06-03 to 2026-06-03 reason demo* → *approve leave request 5*.

---

## Update Twilio every time?

| Tunnel | Update Twilio? |
|--------|----------------|
| cloudflared quick (`trycloudflare.com`) | **Yes** — new URL each time you start Terminal 2 |
| Render / fixed host | **No** — set webhook once |

---

## “command not recognized” fix

| Error | Use this instead |
|--------|------------------|
| `cloudflared` | `& "C:\Program Files (x86)\cloudflared\cloudflared.exe" tunnel ...` |
| `office-leave-whatsapp` | `.\.cursor\mcp-venv\Scripts\python.exe -m uvicorn src.whatsapp.twilio_webhook:app --host 0.0.0.0 --port 8000` |
| `office-leave-init-db` | `.\.cursor\mcp-venv\Scripts\python.exe -m src.init_db` |
| `python` wrong version | Always use `.\.cursor\mcp-venv\Scripts\python.exe` |

Or refresh PATH in the current window, then retry short names:

```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```
