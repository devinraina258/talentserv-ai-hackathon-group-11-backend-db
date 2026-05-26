from __future__ import annotations

import json
import os
import re
from functools import lru_cache

_WHATSAPP_PREFIX = re.compile(r"^whatsapp:", re.IGNORECASE)


def normalize_phone(value: str) -> str:
    """Normalize Twilio From (e.g. whatsapp:+14155550100) to E.164."""
    raw = _WHATSAPP_PREFIX.sub("", (value or "").strip())
    digits = re.sub(r"[^\d+]", "", raw)
    if not digits:
        return ""
    if not digits.startswith("+"):
        digits = f"+{digits}"
    return digits


@lru_cache(maxsize=1)
def load_phone_map() -> dict[str, str]:
    raw = os.environ.get("WHATSAPP_PHONE_MAP", "{}").strip()
    if not raw:
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    if not isinstance(data, dict):
        return {}
    return {normalize_phone(str(phone)): str(slug).strip().lower() for phone, slug in data.items()}


def resolve_slug_from_phone(phone: str) -> str | None:
    slug = load_phone_map().get(normalize_phone(phone))
    return slug if slug else None
