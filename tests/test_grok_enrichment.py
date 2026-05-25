from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.init_db import init_db
from src import db
from src.grok_client import (
    _effective_model,
    generate_fallback_output_recommendations,
    generate_output_recommendations,
    grok_enrich_enabled,
)
from src.mcp_enrichment import (
    ENRICHED_TOOL_NAMES,
    GROK_FOOTER_LINE,
    GROK_HEADER_LINE,
    ensure_enriched_text,
    parse_enriched_mcp_response,
)
from src.server import _json_response_enriched, _resource_response_enriched


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_PATH", str(db_path))
    monkeypatch.setenv("GROK_ENRICH_OUTPUTS", "1")
    init_db(db_path)
    yield db_path


def test_grok_enrich_always_enabled(monkeypatch):
    monkeypatch.setenv("GROK_ENRICH_OUTPUTS", "0")
    assert grok_enrich_enabled() is True


def test_fallback_unknown_employee():
    payload = {
        "success": False,
        "error": "Unknown employee. Supported: devin, nisha, gautam",
    }
    grok = generate_fallback_output_recommendations(
        "get_employee", {"employee": "atlantis"}, payload, None
    )
    assert grok.used_grok is False
    assert "devin" in grok.recommendation
    assert any("slug" in s.lower() for s in grok.suggestions)


def test_enriched_apply_leave_fallback(temp_db, monkeypatch):
    monkeypatch.setenv("GROK_API_KEY", "")
    monkeypatch.setenv("PUTER_AUTH_TOKEN", "")

    async def run() -> dict:
        result = db.apply_leave(
            "devin", "annual", "2026-09-01", "2026-09-02", "Conference"
        )
        raw = await _json_response_enriched(
            result,
            source="apply_leave",
            args={
                "employee": "devin",
                "leave_type": "annual",
                "start_date": "2026-09-01",
                "end_date": "2026-09-02",
                "reason": "Conference",
            },
        )
        return raw, parse_enriched_mcp_response(raw)

    raw, parsed = asyncio.run(run())
    assert GROK_HEADER_LINE in raw
    assert GROK_FOOTER_LINE in raw
    assert parsed["success"] is True
    assert list(parsed.keys())[0] == "grok"
    assert list(parsed.keys())[-1] == "grok_footer"
    assert parsed["grok"] == parsed["grok_footer"]
    assert parsed["grok"]["used_grok"] is False
    assert parsed["grok"]["source"] == "fallback-rules"
    assert parsed["grok"]["recommendation"]


def test_puter_model_prefix(monkeypatch):
    monkeypatch.setenv("GROK_PROVIDER", "puter")
    monkeypatch.setenv("GROK_MODEL", "grok-4.3")
    assert _effective_model() == "x-ai/grok-4.3"
    monkeypatch.setenv("GROK_MODEL", "x-ai/grok-4-1-fast")
    assert _effective_model() == "x-ai/grok-4-1-fast"


def test_enriched_apply_leave_with_mock_grok(temp_db, monkeypatch):
    monkeypatch.setenv("GROK_PROVIDER", "xai")
    monkeypatch.setenv("GROK_API_KEY", "test-key")
    grok_json = json.dumps(
        {
            "recommendation": "Request submitted; track approval.",
            "suggestions": ["Check status tomorrow", "Notify manager"],
            "explanation": "Pending leave does not deduct balance yet.",
            "confidence": "high",
            "next_steps": ["check_leave_status"],
        }
    )

    async def run():
        with patch("src.grok_client._call_grok", new_callable=AsyncMock) as mock_call:
            mock_call.return_value = grok_json
            result = db.apply_leave(
                "nisha", "annual", "2026-10-01", "2026-10-01", "Personal"
            )
            suggestions = await generate_output_recommendations(
                "apply_leave",
                {"employee": "nisha"},
                result.to_dict(),
                None,
            )
            return suggestions, mock_call

    suggestions, mock_call = asyncio.run(run())
    assert suggestions.used_grok is True
    assert suggestions.source == "grok-api"
    assert "approval" in suggestions.recommendation.lower()
    mock_call.assert_awaited_once()


def test_resource_wrapper_includes_grok(temp_db, monkeypatch):
    monkeypatch.setenv("GROK_API_KEY", "")
    monkeypatch.setenv("PUTER_AUTH_TOKEN", "")
    from src import db as db_mod

    async def run() -> dict:
        raw = await _resource_response_enriched(
            "leave://employees",
            db_mod.get_employees_resource(),
        )
        return raw, parse_enriched_mcp_response(raw)

    raw, parsed = asyncio.run(run())
    assert GROK_HEADER_LINE in raw
    assert parsed["resource"] == "leave://employees"
    assert "employees" in parsed["content"]
    assert "grok_footer" in parsed
    assert parsed["grok"]["recommendation"]


def test_enriched_apply_leave_with_mock_puter(temp_db, monkeypatch):
    monkeypatch.setenv("GROK_PROVIDER", "puter")
    monkeypatch.setenv("PUTER_AUTH_TOKEN", "test-puter-token")
    grok_json = json.dumps(
        {
            "recommendation": "Puter-powered tip.",
            "suggestions": ["a"],
            "explanation": "via puter",
            "confidence": "high",
            "next_steps": ["apply_leave"],
        }
    )

    async def run():
        with patch("src.grok_client._call_grok", new_callable=AsyncMock) as mock_call:
            mock_call.return_value = grok_json
            result = db.get_leave_balance("devin")
            suggestions = await generate_output_recommendations(
                "get_leave_balance",
                {"employee": "devin"},
                result.to_dict(),
                None,
            )
            return suggestions

    suggestions = asyncio.run(run())
    assert suggestions.used_grok is True
    assert suggestions.source == "puter-api"


def test_advise_on_leave_single_grok_block(temp_db, monkeypatch):
    monkeypatch.setenv("GROK_PROVIDER", "xai")
    monkeypatch.setenv("GROK_API_KEY", "test-key")
    grok_json = json.dumps(
        {
            "recommendation": "You can take 2 days annual leave.",
            "explanation": "Balance is sufficient.",
            "confidence": "high",
            "next_steps": ["apply_leave"],
        }
    )

    async def run():
        with patch("src.grok_client._call_grok", new_callable=AsyncMock) as mock_call:
            mock_call.return_value = grok_json
            from src.server import advise_on_leave

            raw = await advise_on_leave("devin", "Can I take leave next week?")
            return parse_enriched_mcp_response(raw), mock_call

    parsed, mock_call = asyncio.run(run())
    assert mock_call.await_count == 1
    assert "grok_footer" in parsed
    assert parsed["grok"]["used_grok"] is True
    assert parsed["data"]["advice"]["recommendation"]


@pytest.mark.parametrize("source", ENRICHED_TOOL_NAMES)
def test_every_tool_response_has_grok_header_footer(source, temp_db, monkeypatch):
    monkeypatch.setenv("GROK_API_KEY", "")
    monkeypatch.setenv("PUTER_AUTH_TOKEN", "")

    async def run() -> tuple[str, dict]:
        if source == "list_employees":
            result = db.list_employees()
            args: dict = {}
        elif source == "get_employee":
            result = db.get_employee("devin")
            args = {"employee": "devin"}
        elif source == "get_leave_balance":
            result = db.get_leave_balance("devin")
            args = {"employee": "devin"}
        elif source == "apply_leave":
            result = db.apply_leave(
                "devin", "annual", "2026-11-01", "2026-11-01", "Test"
            )
            args = {
                "employee": "devin",
                "leave_type": "annual",
                "start_date": "2026-11-01",
                "end_date": "2026-11-01",
                "reason": "Test",
            }
        elif source == "check_leave_status":
            result = db.check_leave_status(None, "devin")
            args = {"employee": "devin"}
        elif source == "list_leave_requests":
            result = db.list_leave_requests(None, None)
            args = {}
        else:
            ctx = db.get_employee_context_for_advice("devin")
            result = ctx
            args = {"employee": "devin", "question": "Can I take leave?"}

        raw = await _json_response_enriched(result, source=source, args=args)
        return raw, parse_enriched_mcp_response(raw)

    raw, parsed = asyncio.run(run())
    assert GROK_HEADER_LINE in raw
    assert GROK_FOOTER_LINE in raw
    assert parsed["grok"]["recommendation"]
    assert parsed["grok_footer"] == parsed["grok"]


def test_middleware_enriches_plain_json(temp_db, monkeypatch):
    monkeypatch.setenv("GROK_API_KEY", "")
    monkeypatch.setenv("PUTER_AUTH_TOKEN", "")
    plain = json.dumps(db.get_leave_balance("nisha").to_dict())

    async def run() -> str:
        return await ensure_enriched_text(
            plain, source="get_leave_balance", args={"employee": "nisha"}
        )

    raw = asyncio.run(run())
    assert GROK_HEADER_LINE in raw
    assert "grok_footer" in parse_enriched_mcp_response(raw)


def test_enrichment_always_includes_grok_block(temp_db, monkeypatch):
    monkeypatch.setenv("GROK_ENRICH_OUTPUTS", "0")
    monkeypatch.setenv("GROK_API_KEY", "")
    monkeypatch.setenv("PUTER_AUTH_TOKEN", "")

    async def run() -> dict:
        result = db.get_leave_balance("gautam")
        raw = await _json_response_enriched(
            result, source="get_leave_balance", args={"employee": "gautam"}
        )
        return parse_enriched_mcp_response(raw)

    parsed = asyncio.run(run())
    assert parsed["grok"]["recommendation"]
    assert parsed["grok_footer"]["recommendation"]
