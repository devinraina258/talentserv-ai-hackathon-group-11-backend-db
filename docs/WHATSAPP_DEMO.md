# WhatsApp demo (Twilio Sandbox, free tier)

Message the office-leave backend from WhatsApp using **Twilio WhatsApp Sandbox** + **ngrok** (local) or **Render** (optional public URL). Reuses the same SQLite DB and [`src/db.py`](../src/db.py) as the MCP server—short text replies, no MCP JSON.

For **manager channel alerts** on apply/approve/reject, see [TEAMS_INTEGRATION.md](TEAMS_INTEGRATION.md) (Microsoft Teams Incoming Webhook).

## Prerequisites

- Python 3.10+
- [Twilio account](https://www.twilio.com/try-twilio) (trial / free)
- [ngrok](https://ngrok.com/) (free) for local HTTPS webhook
- Database: `office-leave-init-db` or `python -m src.init_db`

## 1. Install

```bash
pip install -e ".[dev,whatsapp]"
copy .env.example .env
```

Edit `.env`:

- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` from [Twilio Console](https://console.twilio.com/)
- `TWILIO_WHATSAPP_FROM` — sandbox number, e.g. `whatsapp:+14155238886` (from Sandbox page)
- `WHATSAPP_PHONE_MAP` — JSON map of **your** E.164 number → slug:

```env
WHATSAPP_PHONE_MAP={"+1YOUR_MOBILE":"devin"}
```

Use the exact format Twilio sends (check webhook logs); include country code.

## 2. Twilio WhatsApp Sandbox

1. Console → **Messaging** → **Try it out** → **Send a WhatsApp message** → **Sandbox**.
2. On your phone, send `join <your-sandbox-code>` to the sandbox number shown.
3. Under **Sandbox settings**, set **When a message comes in** to your public webhook URL (step 3 below) + `/whatsapp/webhook`, method **POST**.

## 3. Run webhook locally + ngrok

Terminal 1:

```bash
office-leave-init-db
office-leave-whatsapp
# or: uvicorn src.whatsapp.twilio_webhook:app --host 0.0.0.0 --port 8000
```

Terminal 2:

```bash
ngrok http 8000
```

Copy the `https://….ngrok-free.app` URL into Twilio:

`https://YOUR_SUBDOMAIN.ngrok-free.app/whatsapp/webhook`

Health check: `GET https://…/whatsapp/webhook` → `{"status":"ok",…}`

### Local dev without signature (optional)

Only on your machine:

```env
TWILIO_SKIP_SIGNATURE=1
```

Never use in production or on a public URL.

## 4. Try commands on WhatsApp

| Message | Action |
|---------|--------|
| `help` | Command menu |
| `list` | All employees + balances |
| `balance` | Your balance (phone → slug) |
| `status` | Latest leave request |
| `requests` | Recent requests |
| `apply annual 2026-06-10 2026-06-11 family trip` | Submit leave (pending) |
| `advise Can I take 2 days next week?` | Short Grok/rules advice |

Unknown phones: *Not registered. Ask admin to add your number…*

## 5. Optional: Render (free tier)

1. New **Web Service** from this repo; build: `pip install -e ".[whatsapp]"`; start: `uvicorn src.whatsapp.twilio_webhook:app --host 0.0.0.0 --port $PORT`
2. Set env vars in Render (Twilio + `WHATSAPP_PHONE_MAP` + `DATABASE_PATH`).
3. On deploy, run init DB once (shell or release command): `python -m src.init_db`
4. Point Twilio webhook to `https://YOUR_APP.onrender.com/whatsapp/webhook`

**Note:** Free Render disks are ephemeral; re-seed DB after redeploy or commit a small seed DB for demos only.

## Security (demo limits)

- Only numbers that **joined the sandbox** can message.
- `WHATSAPP_PHONE_MAP` is demo auth—not enterprise SSO.
- `apply` and `balance` always use **your** mapped slug (no `balance nisha`).
- Twilio requests must pass `X-Twilio-Signature` validation (unless `TWILIO_SKIP_SIGNATURE=1` locally).

## Troubleshooting

| Issue | Fix |
|-------|-----|
| 403 Invalid signature | Webhook URL must match exactly what Twilio calls; use ngrok HTTPS URL; check `TWILIO_AUTH_TOKEN` |
| Not registered | Add your phone to `WHATSAPP_PHONE_MAP` in E.164 form |
| No reply | Confirm sandbox `join`; check ngrok/uvicorn logs |
| Insufficient balance | Expected for demo data; try another employee slug in the map |

## Manual test checklist

1. `help` → menu
2. `balance` → annual/sick numbers
3. `apply annual …` → pending request id
4. `status` → shows pending
5. `list` → three employees
