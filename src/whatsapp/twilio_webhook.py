from __future__ import annotations

import os
from xml.sax.saxutils import escape

from fastapi import FastAPI, Request, Response
from fastapi.responses import PlainTextResponse
from twilio.request_validator import RequestValidator

from src.env import load_workspace_env
from src.whatsapp.handlers import handle_incoming

load_workspace_env()

app = FastAPI(title="Office Leave WhatsApp", version="1.0.0")


def _twilio_auth_token() -> str:
    return os.environ.get("TWILIO_AUTH_TOKEN", "").strip()


def _validate_twilio_request(request: Request, form: dict[str, str]) -> bool:
    token = _twilio_auth_token()
    if not token:
        # Allow local dev without token if explicitly disabled
        if os.environ.get("TWILIO_SKIP_SIGNATURE", "").strip() in ("1", "true", "yes"):
            return True
        return False
    signature = request.headers.get("X-Twilio-Signature", "")
    url = str(request.url)
    validator = RequestValidator(token)
    return validator.validate(url, form, signature)


def _twiml_message(text: str) -> Response:
    body = escape(text[:4000])
    xml = f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{body}</Message></Response>'
    return Response(content=xml, media_type="application/xml")


@app.get("/whatsapp/webhook")
async def webhook_health() -> dict[str, str]:
    return {"status": "ok", "service": "office-leave-whatsapp"}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/whatsapp/webhook")
async def whatsapp_webhook(request: Request) -> Response:
    form = dict(await request.form())
    params = {k: str(v) for k, v in form.items()}

    if not _validate_twilio_request(request, params):
        return PlainTextResponse("Invalid Twilio signature", status_code=403)

    from_phone = params.get("From", "")
    body = params.get("Body", "")
    reply = await handle_incoming(from_phone, body)
    return _twiml_message(reply)


def main() -> None:
    import uvicorn

    host = os.environ.get("WHATSAPP_HOST", "0.0.0.0")
    port = int(os.environ.get("WHATSAPP_PORT", "8000"))
    uvicorn.run(
        "src.whatsapp.twilio_webhook:app",
        host=host,
        port=port,
        reload=os.environ.get("WHATSAPP_RELOAD", "").strip() in ("1", "true"),
    )


if __name__ == "__main__":
    main()
