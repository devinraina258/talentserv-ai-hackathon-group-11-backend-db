from __future__ import annotations

import json
import logging
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    import requests

logger = logging.getLogger(__name__)


def post_json(url: str, payload: dict[str, Any], *, timeout_seconds: float) -> Any:
    """
    Thin wrapper around `requests.post` so we can centralize:
    - timeouts
    - basic error logging
    - content-type expectations
    """

    try:
        import requests  # local import to avoid hard dependency for non-Teams runs
    except ModuleNotFoundError as e:
        logger.error("`requests` is required for Teams notifications: pip install -e \".[teams]\"")
        raise e

    headers = {"Content-Type": "application/json"}
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=timeout_seconds)
    except Exception:
        # Let callers decide how to handle exceptions; we only log context here.
        logger.exception("POST failed (url=%s) payload=%s", url, json.dumps(payload)[:2000])
        raise
    return resp

