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
    generate_fallback_output_recommendations,
    generate_output_recommendations,
    grok_enrich_enabled,
)
from src.server import _json_response_enriched, _resource_response_enriched


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_PATH", str(db_path))
    monkeypatch.setenv("GROK_ENRICH_OUTPUTS", "1")
    init_db(db_path)
    yield db_path


def test_grok_enrich_enabled_default(monkeypatch):
    monkeypatch.delenv("GROK_ENRICH_OUTPUTS", raising=False)
    assert grok_enrich_enabled() is True
    monkeypatch.setenv("GROK_ENRICH_OUTPUTS", "0")
    assert grok_enrich_enabled() is False


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
        return json.loads(raw)

    parsed = asyncio.run(run())
    assert parsed["success"] is True
    assert "grok" in parsed
    assert parsed["grok"]["used_grok"] is False
    assert parsed["grok"]["source"] == "fallback-rules"
    assert parsed["grok"]["recommendation"]


def test_enriched_apply_leave_with_mock_grok(temp_db, monkeypatch):
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
    from src import db as db_mod

    async def run() -> dict:
        raw = await _resource_response_enriched(
            "leave://employees",
            db_mod.get_employees_resource(),
        )
        return json.loads(raw)

    parsed = asyncio.run(run())
    assert parsed["resource"] == "leave://employees"
    assert "employees" in parsed["content"]
    assert "grok" in parsed
    assert parsed["grok"]["recommendation"]


def test_advise_on_leave_single_grok_block(temp_db, monkeypatch):
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
            return json.loads(raw), mock_call

    parsed, mock_call = asyncio.run(run())
    assert mock_call.await_count == 1
    assert "grok" in parsed
    assert parsed["grok"]["used_grok"] is True
    assert parsed["data"]["advice"]["recommendation"]


def test_enrichment_disabled_skips_grok_block(temp_db, monkeypatch):
    monkeypatch.setenv("GROK_ENRICH_OUTPUTS", "0")

    async def run() -> dict:
        result = db.get_leave_balance("gautam")
        raw = await _json_response_enriched(
            result, source="get_leave_balance", args={"employee": "gautam"}
        )
        return json.loads(raw)

    parsed = asyncio.run(run())
    assert "grok" not in parsed
