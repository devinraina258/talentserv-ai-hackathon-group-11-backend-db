from __future__ import annotations

import os
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.init_db import init_db
from src import db


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_PATH", str(db_path))
    init_db(db_path)
    yield db_path


def test_list_employees(temp_db):
    result = db.list_employees()
    assert result.success
    assert len(result.data) == 3
    slugs = {e["slug"] for e in result.data}
    assert slugs == {"devin", "nisha", "gautam"}


def test_get_leave_balance(temp_db):
    result = db.get_leave_balance("nisha")
    assert result.success
    assert result.data["annual_remaining"] == 10.0
    assert result.data["sick_remaining"] == 4.0


def test_apply_leave_pending(temp_db):
    result = db.apply_leave(
        "devin",
        "annual",
        "2026-06-01",
        "2026-06-02",
        "Hackathon prep",
    )
    assert result.success
    assert result.data["request"]["status"] == "pending"
    assert result.data["request"]["days"] == 2.0

    balance = db.get_leave_balance("devin")
    assert balance.data["annual_remaining"] == 12.0


def test_apply_leave_insufficient_balance(temp_db):
    result = db.apply_leave(
        "nisha",
        "sick",
        "2026-07-01",
        "2026-07-10",
        "Extended recovery",
    )
    assert not result.success
    assert "Insufficient" in (result.error or "")


def test_check_leave_status_by_employee(temp_db):
    result = db.check_leave_status(employee="gautam")
    assert result.success
    assert result.data["employee_slug"] == "gautam"


def test_check_leave_status_by_id(temp_db):
    with db.connect() as conn:
        row = conn.execute(
            "SELECT id FROM leave_requests ORDER BY id LIMIT 1"
        ).fetchone()
    result = db.check_leave_status(request_id=row["id"])
    assert result.success
    assert result.data["id"] == row["id"]


def test_unknown_employee(temp_db):
    result = db.get_employee("atlantis")
    assert not result.success


def test_list_leave_requests_filter(temp_db):
    db.apply_leave("devin", "annual", "2026-08-01", "2026-08-01", "Test")
    result = db.list_leave_requests(employee="devin", status="pending")
    assert result.success
    assert all(r["status"] == "pending" for r in result.data)
