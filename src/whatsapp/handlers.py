from __future__ import annotations

import os
import time

from src import db
from src.grok_client import generate_leave_advice_with_grok
from src.whatsapp.auth import resolve_slug_from_phone
from src.whatsapp.commands import ParseError, ParsedCommand, parse_command
from src.whatsapp import formatters

_COOLDOWN_SECONDS = 1.0
_last_reply_at: dict[str, float] = {}

UNREGISTERED_MSG = "Not registered. Ask admin to add your number to WHATSAPP_PHONE_MAP."


def _rate_limited(phone: str) -> bool:
    if os.environ.get("WHATSAPP_DISABLE_RATE_LIMIT", "").strip() in (
        "1",
        "true",
        "yes",
    ):
        return False
    now = time.monotonic()
    last = _last_reply_at.get(phone, 0.0)
    if now - last < _COOLDOWN_SECONDS:
        return True
    _last_reply_at[phone] = now
    return False


async def handle_command(slug: str, parsed: ParsedCommand) -> str:
    if parsed.action == "help":
        return formatters.format_help()

    if parsed.action == "list":
        return formatters.format_employees(db.list_employees())

    if parsed.action == "balance":
        return formatters.format_balance(db.get_leave_balance(slug))

    if parsed.action == "status":
        return formatters.format_status(db.check_leave_status(None, slug))

    if parsed.action == "requests":
        return formatters.format_requests(db.list_leave_requests(slug, None))

    if parsed.action == "apply":
        return formatters.format_apply(
            db.apply_leave(
                slug,
                parsed.leave_type,
                parsed.start_date,
                parsed.end_date,
                parsed.reason,
            )
        )

    if parsed.action == "advise":
        ctx = db.get_employee_context_for_advice(slug)
        if not ctx.success:
            return ctx.error or "Could not load your profile."
        advice = await generate_leave_advice_with_grok(ctx.data or {}, parsed.question)
        return formatters.format_advice(advice)

    return (
        "Unknown command. Send help for:\n"
        "list, balance, status, requests, apply, advise"
    )


async def handle_incoming(from_phone: str, body: str) -> str:
    if _rate_limited(from_phone):
        return "Please wait a moment before sending another message."

    slug = resolve_slug_from_phone(from_phone)
    if not slug:
        return UNREGISTERED_MSG

    parsed = parse_command(body)
    if isinstance(parsed, ParseError):
        return formatters.format_error(parsed.message)

    return await handle_command(slug, parsed)
