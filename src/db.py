from __future__ import annotations

import os
import sqlite3
from datetime import date, datetime
from pathlib import Path

from src.models import Employee, LeaveRequest, ToolResponse, utc_now_iso

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = ROOT / "data" / "employees.db"

LEAVE_POLICY = {
    "notice_days": 2,
    "max_consecutive_days": 14,
    "types": ["annual", "sick"],
    "rules": [
        "Submit leave at least 2 calendar days in advance for annual leave when possible.",
        "Sick leave can be same-day; provide a brief reason.",
        "Pending requests do not reduce balance until approved.",
        "Maximum 14 consecutive calendar days per request.",
    ],
}


def get_db_path() -> Path:
    raw = os.environ.get("DATABASE_PATH", str(DEFAULT_DB))
    path = Path(raw)
    return path if path.is_absolute() else ROOT / path


def connect() -> sqlite3.Connection:
    path = get_db_path()
    if not path.exists():
        raise FileNotFoundError(
            f"Database not found at {path}. Run: python scripts/init_db.py"
        )
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def resolve_slug(employee: str) -> str | None:
    if not employee or not str(employee).strip():
        return None
    key = str(employee).strip().lower()
    aliases = {
        "devin": "devin",
        "nisha": "nisha",
        "gautam": "gautam",
    }
    if key in aliases:
        return aliases[key]
    for slug, display in [("devin", "devin"), ("nisha", "nisha"), ("gautam", "gautam")]:
        if key == display or key == slug:
            return slug
    with connect() as conn:
        row = conn.execute(
            """
            SELECT slug FROM employees
            WHERE lower(slug) = ? OR lower(display_name) = ?
            """,
            (key, key),
        ).fetchone()
    return row["slug"] if row else None


def parse_iso_date(value: str) -> date | None:
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except ValueError:
        return None


def calendar_days_inclusive(start: date, end: date) -> float:
    return float((end - start).days + 1)


def row_to_employee(row: sqlite3.Row) -> Employee:
    return Employee(
        id=row["id"],
        slug=row["slug"],
        display_name=row["display_name"],
        department=row["department"],
        email=row["email"],
        annual_remaining=float(row["annual_remaining"]),
        sick_remaining=float(row["sick_remaining"]),
    )


def row_to_leave_request(row: sqlite3.Row) -> LeaveRequest:
    return LeaveRequest(
        id=row["id"],
        employee_slug=row["employee_slug"],
        employee_name=row["employee_name"],
        leave_type=row["leave_type"],
        start_date=row["start_date"],
        end_date=row["end_date"],
        days=float(row["days"]),
        reason=row["reason"],
        status=row["status"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


def list_employees() -> ToolResponse[list[dict]]:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT e.slug, e.display_name, e.department, e.email,
                   b.annual_remaining, b.sick_remaining
            FROM employees e
            JOIN leave_balances b ON b.employee_id = e.id
            ORDER BY e.display_name
            """
        ).fetchall()
    data = [dict(r) for r in rows]
    return ToolResponse(success=True, data=data, timestamp=utc_now_iso())


def get_employee(employee: str) -> ToolResponse[dict]:
    slug = resolve_slug(employee)
    if not slug:
        return ToolResponse(
            success=False,
            error="Unknown employee. Supported: devin, nisha, gautam",
            timestamp=utc_now_iso(),
        )
    with connect() as conn:
        row = conn.execute(
            """
            SELECT e.id, e.slug, e.display_name, e.department, e.email,
                   b.annual_remaining, b.sick_remaining
            FROM employees e
            JOIN leave_balances b ON b.employee_id = e.id
            WHERE e.slug = ?
            """,
            (slug,),
        ).fetchone()
    if not row:
        return ToolResponse(success=False, error="Employee not found", timestamp=utc_now_iso())
    emp = row_to_employee(row)
    return ToolResponse(
        success=True,
        data={
            "slug": emp.slug,
            "display_name": emp.display_name,
            "department": emp.department,
            "email": emp.email,
            "annual_remaining": emp.annual_remaining,
            "sick_remaining": emp.sick_remaining,
        },
        timestamp=utc_now_iso(),
    )


def get_leave_balance(employee: str) -> ToolResponse[dict]:
    result = get_employee(employee)
    if not result.success:
        return result
    data = result.data or {}
    return ToolResponse(
        success=True,
        data={
            "employee": data.get("slug"),
            "display_name": data.get("display_name"),
            "annual_remaining": data.get("annual_remaining"),
            "sick_remaining": data.get("sick_remaining"),
        },
        timestamp=utc_now_iso(),
    )


def _fetch_requests(
    conn: sqlite3.Connection,
    employee_slug: str | None = None,
    status: str | None = None,
    limit: int = 50,
) -> list[LeaveRequest]:
    query = """
        SELECT lr.id, e.slug AS employee_slug, e.display_name AS employee_name,
               lr.leave_type, lr.start_date, lr.end_date, lr.days, lr.reason,
               lr.status, lr.created_at, lr.updated_at
        FROM leave_requests lr
        JOIN employees e ON e.id = lr.employee_id
        WHERE 1=1
    """
    params: list[object] = []
    if employee_slug:
        query += " AND e.slug = ?"
        params.append(employee_slug)
    if status:
        query += " AND lr.status = ?"
        params.append(status)
    query += " ORDER BY lr.created_at DESC LIMIT ?"
    params.append(limit)
    rows = conn.execute(query, params).fetchall()
    return [row_to_leave_request(r) for r in rows]


def list_leave_requests(
    employee: str | None = None,
    status: str | None = None,
) -> ToolResponse[list[dict]]:
    slug = None
    if employee:
        slug = resolve_slug(employee)
        if not slug:
            return ToolResponse(
                success=False,
                error="Unknown employee. Supported: devin, nisha, gautam",
                timestamp=utc_now_iso(),
            )
    if status and status not in ("pending", "approved", "rejected"):
        return ToolResponse(
            success=False,
            error="Invalid status. Use: pending, approved, rejected",
            timestamp=utc_now_iso(),
        )
    with connect() as conn:
        requests = _fetch_requests(conn, slug, status)
    return ToolResponse(
        success=True,
        data=[vars(r) for r in requests],
        timestamp=utc_now_iso(),
    )


def apply_leave(
    employee: str,
    leave_type: str,
    start_date: str,
    end_date: str,
    reason: str,
) -> ToolResponse[dict]:
    slug = resolve_slug(employee)
    if not slug:
        return ToolResponse(
            success=False,
            error="Unknown employee. Supported: devin, nisha, gautam",
            timestamp=utc_now_iso(),
        )

    leave_type = (leave_type or "").strip().lower()
    if leave_type not in ("annual", "sick"):
        return ToolResponse(
            success=False,
            error="leave_type must be 'annual' or 'sick'",
            timestamp=utc_now_iso(),
        )

    start = parse_iso_date(start_date)
    end = parse_iso_date(end_date)
    if not start or not end:
        return ToolResponse(
            success=False,
            error="Dates must be ISO format YYYY-MM-DD",
            timestamp=utc_now_iso(),
        )
    if end < start:
        return ToolResponse(
            success=False,
            error="end_date must be on or after start_date",
            timestamp=utc_now_iso(),
        )

    days = calendar_days_inclusive(start, end)
    if days > LEAVE_POLICY["max_consecutive_days"]:
        return ToolResponse(
            success=False,
            error=f"Maximum {LEAVE_POLICY['max_consecutive_days']} consecutive days per request",
            timestamp=utc_now_iso(),
        )

    reason = (reason or "").strip()
    if not reason:
        return ToolResponse(success=False, error="reason is required", timestamp=utc_now_iso())

    with connect() as conn:
        emp = conn.execute(
            """
            SELECT e.id, e.slug, e.display_name, b.annual_remaining, b.sick_remaining
            FROM employees e
            JOIN leave_balances b ON b.employee_id = e.id
            WHERE e.slug = ?
            """,
            (slug,),
        ).fetchone()
        if not emp:
            return ToolResponse(success=False, error="Employee not found", timestamp=utc_now_iso())

        balance_key = "annual_remaining" if leave_type == "annual" else "sick_remaining"
        remaining = float(emp[balance_key])
        if days > remaining:
            return ToolResponse(
                success=False,
                error=f"Insufficient {leave_type} balance: {remaining} days remaining, requested {days}",
                timestamp=utc_now_iso(),
            )

        cur = conn.execute(
            """
            INSERT INTO leave_requests
              (employee_id, leave_type, start_date, end_date, days, reason, status)
            VALUES (?, ?, ?, ?, ?, ?, 'pending')
            """,
            (emp["id"], leave_type, start.isoformat(), end.isoformat(), days, reason),
        )
        request_id = cur.lastrowid
        conn.commit()

        row = conn.execute(
            """
            SELECT lr.id, e.slug AS employee_slug, e.display_name AS employee_name,
                   lr.leave_type, lr.start_date, lr.end_date, lr.days, lr.reason,
                   lr.status, lr.created_at, lr.updated_at
            FROM leave_requests lr
            JOIN employees e ON e.id = lr.employee_id
            WHERE lr.id = ?
            """,
            (request_id,),
        ).fetchone()

    req = row_to_leave_request(row)
    return ToolResponse(
        success=True,
        data={
            "message": "Leave request submitted (pending approval)",
            "request": vars(req),
        },
        timestamp=utc_now_iso(),
    )


def check_leave_status(
    request_id: int | None = None,
    employee: str | None = None,
) -> ToolResponse[dict]:
    if request_id is not None:
        with connect() as conn:
            row = conn.execute(
                """
                SELECT lr.id, e.slug AS employee_slug, e.display_name AS employee_name,
                       lr.leave_type, lr.start_date, lr.end_date, lr.days, lr.reason,
                       lr.status, lr.created_at, lr.updated_at
                FROM leave_requests lr
                JOIN employees e ON e.id = lr.employee_id
                WHERE lr.id = ?
                """,
                (request_id,),
            ).fetchone()
        if not row:
            return ToolResponse(
                success=False,
                error=f"No request with id {request_id}",
                timestamp=utc_now_iso(),
            )
        return ToolResponse(
            success=True,
            data=vars(row_to_leave_request(row)),
            timestamp=utc_now_iso(),
        )

    if not employee:
        return ToolResponse(
            success=False,
            error="Provide request_id or employee",
            timestamp=utc_now_iso(),
        )

    slug = resolve_slug(employee)
    if not slug:
        return ToolResponse(
            success=False,
            error="Unknown employee. Supported: devin, nisha, gautam",
            timestamp=utc_now_iso(),
        )

    with connect() as conn:
        requests = _fetch_requests(conn, slug, limit=1)

    if not requests:
        return ToolResponse(
            success=False,
            error=f"No leave requests found for {slug}",
            timestamp=utc_now_iso(),
        )

    return ToolResponse(
        success=True,
        data=vars(requests[0]),
        timestamp=utc_now_iso(),
    )


def get_employee_context_for_advice(employee: str) -> ToolResponse[dict]:
    slug = resolve_slug(employee)
    if not slug:
        return ToolResponse(
            success=False,
            error="Unknown employee. Supported: devin, nisha, gautam",
            timestamp=utc_now_iso(),
        )
    profile = get_employee(slug)
    if not profile.success:
        return profile

    with connect() as conn:
        recent = _fetch_requests(conn, slug, limit=5)
        pending = _fetch_requests(conn, slug, status="pending", limit=10)

    return ToolResponse(
        success=True,
        data={
            "profile": profile.data,
            "recent_requests": [vars(r) for r in recent],
            "pending_requests": [vars(r) for r in pending],
            "policy": LEAVE_POLICY,
        },
        timestamp=utc_now_iso(),
    )


def get_employees_resource() -> str:
    result = list_employees()
    import json

    return json.dumps({"employees": result.data}, indent=2)


def get_policy_resource() -> str:
    import json

    return json.dumps(LEAVE_POLICY, indent=2)
