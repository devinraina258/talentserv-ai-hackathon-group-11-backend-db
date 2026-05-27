from __future__ import annotations

import logging
import os
from typing import Any

from src.env import load_workspace_env
from src.services.api_client import post_json

logger = logging.getLogger(__name__)


def _is_truthy(value: str | None) -> bool:
    return str(value or "").strip().lower() in ("1", "true", "yes", "on")


def _teams_webhook_url(webhook_url_override: str | None = None) -> str:
    """
    Microsoft Teams Incoming Webhook URL.

    Teams Incoming Webhooks are "pre-authorized" URLs. Your server posts a small JSON
    payload to the webhook endpoint, and Teams delivers it into the configured channel.
    """

    if webhook_url_override:
        return webhook_url_override.strip()
    return os.environ.get("TEAMS_WEBHOOK_URL", "").strip()


def _teams_timeout_seconds() -> float:
    raw = os.environ.get("TEAMS_WEBHOOK_TIMEOUT_SECONDS", "5").strip()
    try:
        return float(raw)
    except ValueError:
        return 5.0


# Sample Adaptive Card payload you can copy into tests or docs.
# Teams expects Adaptive Cards as:
#   { "attachments": [ { "contentType": "...adaptive...", "content": { ...card } } ] }
SAMPLE_ADAPTIVE_CARD: dict[str, Any] = {
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "type": "AdaptiveCard",
    "version": "1.4",
    "body": [
        {"type": "TextBlock", "size": "medium", "weight": "bolder", "text": "Office Leave Notification"},
        {"type": "TextBlock", "wrap": True, "text": "${message}"},
    ],
}


def format_teams_connection_test_message() -> str:
    """Sample message for webhook smoke tests (not a real leave event)."""
    return "\n".join(
        [
            "Office Leave — Teams connected",
            "",
            "This channel will receive:",
            "• New leave requests (pending approval)",
            "• Approvals and rejections",
            "• Company holiday announcements",
            "",
            "No action required — this was a connection test.",
        ]
    )


def send_teams_connection_test(*, webhook_url: str | None = None) -> None:
    """Post a meaningful smoke-test message to verify the Incoming Webhook."""
    send_teams_message(format_teams_connection_test_message(), webhook_url=webhook_url)


def send_teams_message(message: str, *, webhook_url: str | None = None) -> None:
    """
    Send a notification to Microsoft Teams via Incoming Webhook.

    This is intentionally resilient: failures are logged but do not raise, so MCP tool
    responses are not blocked by Teams outages.
    """
    load_workspace_env()
    resolved_webhook_url = _teams_webhook_url(webhook_url)
    if not resolved_webhook_url:
        logger.warning("TEAMS_WEBHOOK_URL not set; skipping Teams notification.")
        return

    timeout_seconds = _teams_timeout_seconds()

    # Incoming Webhook supports simple "text" messages, and also Adaptive Cards.
    # Adaptive cards are useful for richer formatting and better readability.
    use_adaptive = _is_truthy(os.environ.get("TEAMS_USE_ADAPTIVE_CARD"))
    if use_adaptive:
        adaptive_card = {
            **SAMPLE_ADAPTIVE_CARD,
            "body": [
                SAMPLE_ADAPTIVE_CARD["body"][0],
                {"type": "TextBlock", "wrap": True, "text": message},
            ],
        }
        payload: dict[str, Any] = {
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "content": adaptive_card,
                }
            ]
        }
    else:
        payload = {"text": message}

    try:
        resp = post_json(resolved_webhook_url, payload, timeout_seconds=timeout_seconds)
    except Exception:
        logger.exception("Teams webhook request failed.")
        return

    if resp.status_code >= 400:
        text = (resp.text or "").strip()
        logger.error(
            "Teams webhook returned HTTP %s: %s",
            resp.status_code,
            text[:2000],
        )

