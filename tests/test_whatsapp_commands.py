from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.init_db import init_db
from src import db
from src.whatsapp.auth import load_phone_map, normalize_phone, resolve_slug_from_phone
from src.whatsapp.commands import ParseError, parse_command
from src.whatsapp.handlers import UNREGISTERED_MSG, handle_command, handle_incoming


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_PATH", str(db_path))
    monkeypatch.setenv("GROK_API_KEY", "")
    monkeypatch.setenv("PUTER_AUTH_TOKEN", "")
    init_db(db_path)
    yield db_path


@pytest.fixture(autouse=True)
def whatsapp_test_env(monkeypatch):
    monkeypatch.setenv("WHATSAPP_DISABLE_RATE_LIMIT", "1")
    load_phone_map.cache_clear()
    yield
    load_phone_map.cache_clear()


def test_normalize_phone_whatsapp_prefix():
    assert normalize_phone("whatsapp:+14155550100") == "+14155550100"
    assert normalize_phone("+14155550100") == "+14155550100"


def test_resolve_slug_from_env(monkeypatch):
    monkeypatch.setenv(
        "WHATSAPP_PHONE_MAP",
        json.dumps({"+14155550100": "devin", "whatsapp:+19998887777": "nisha"}),
    )
    load_phone_map.cache_clear()
    assert resolve_slug_from_phone("whatsapp:+14155550100") == "devin"
    assert resolve_slug_from_phone("+19998887777") == "nisha"
    assert resolve_slug_from_phone("+10000000000") is None


def test_parse_help_and_balance():
    assert parse_command("help").action == "help"
    assert parse_command("balance").action == "balance"


def test_parse_balance_rejects_other_employee():
    err = parse_command("balance nisha")
    assert isinstance(err, ParseError)


def test_parse_apply_valid():
    cmd = parse_command("apply annual 2026-06-10 2026-06-11 family trip")
    assert cmd.action == "apply"
    assert cmd.leave_type == "annual"
    assert cmd.reason == "family trip"


def test_parse_apply_invalid_date():
    assert isinstance(parse_command("apply annual bad-date 2026-06-11 x"), ParseError)


def test_parse_advise():
    cmd = parse_command("advise Can I take leave next week?")
    assert cmd.action == "advise"
    assert "next week" in cmd.question


def test_unregistered_phone(monkeypatch):
    monkeypatch.setenv("WHATSAPP_PHONE_MAP", "{}")
    load_phone_map.cache_clear()
    reply = asyncio.run(handle_incoming("whatsapp:+10000000001", "help"))
    assert reply == UNREGISTERED_MSG


def test_handle_balance_for_mapped_user(temp_db, monkeypatch):
    monkeypatch.setenv("WHATSAPP_PHONE_MAP", json.dumps({"+14155550100": "nisha"}))
    load_phone_map.cache_clear()
    reply = asyncio.run(handle_incoming("whatsapp:+14155550100", "balance"))
    assert "10" in reply
    assert "annual" in reply.lower()


def test_handle_apply_for_mapped_user(temp_db, monkeypatch):
    monkeypatch.setenv("WHATSAPP_PHONE_MAP", json.dumps({"+14155550100": "devin"}))
    load_phone_map.cache_clear()
    reply = asyncio.run(
        handle_incoming(
            "whatsapp:+14155550100",
            "apply annual 2026-08-01 2026-08-01 conference",
        )
    )
    assert "Submitted" in reply or "request" in reply.lower()


def test_handle_list_no_registration_required_for_list(monkeypatch, temp_db):
    """list still requires registration per plan — verify registered user can list."""
    monkeypatch.setenv("WHATSAPP_PHONE_MAP", json.dumps({"+14155550100": "devin"}))
    load_phone_map.cache_clear()
    reply = asyncio.run(handle_incoming("whatsapp:+14155550100", "list"))
    assert "Devin" in reply or "devin" in reply.lower()


def test_handle_command_status(temp_db):
    reply = asyncio.run(handle_command("gautam", parse_command("status")))
    assert isinstance(reply, str)
