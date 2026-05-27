from __future__ import annotations

import asyncio
import json
import logging
import os
from typing import Any, Literal

from src import db
from src.models import ToolResponse
from src.services.teams_service import send_teams_message

logger = logging.getLogger(__name__)

LeaveTeamsEvent = Literal["submitted", "approved", "rejected"]
TeamsAudience = Literal["channel", "manager"]


def _leave_type_label(leave_type: str | None) -> str:
    lt = (leave_type or "").strip().lower()
    if lt == "annual":
        return "Annual leave"
    if lt == "sick":
        return "Sick leave"
    return lt.title() if lt else "Leave"


def _days_label(days: Any) -> str:
    try:
        n = float(days)
    except (TypeError, ValueError):
        return ""
    if n == 1.0:
        return "1 day"
    if n == int(n):
        return f"{int(n)} days"
    return f"{n:g} days"


def _date_range_label(req: dict[str, Any]) -> str:
    start = req.get("start_date") or ""
    end = req.get("end_date") or ""
    if start and start == end:
        return str(start)
    if start and end:
        return f"{start} to {end}"
    return str(start or end or "—")


def _employee_department(employee_slug: str | None) -> str | None:
    if not employee_slug:
        return None
    emp = db.get_employee(employee_slug)
    if emp.success and isinstance(emp.data, dict):
        dept = emp.data.get("department")
        if isinstance(dept, str) and dept.strip():
            return dept.strip()
    return None


def _employee_header(req: dict[str, Any]) -> str:
    name = req.get("employee_name") or req.get("employee_slug") or "Employee"
    dept = _employee_department(req.get("employee_slug"))
    if dept:
        return f"{name} · {dept}"
    return str(name)


def format_leave_teams_message(
    event: LeaveTeamsEvent,
    req: dict[str, Any],
    *,
    audience: TeamsAudience = "channel",
) -> str:
    """Human-readable Teams text for leave lifecycle events."""
    request_id = req.get("id")
    id_part = f"Request #{request_id}" if request_id is not None else "Leave request"
    header = _employee_header(req)
    leave_parts = [_leave_type_label(req.get("leave_type"))]
    days_part = _days_label(req.get("days"))
    if days_part:
        leave_parts.append(days_part)
    date_part = _date_range_label(req)
    if date_part and date_part != "—":
        leave_parts.append(date_part)
    leave_line = " · ".join(leave_parts)
    reason = (req.get("reason") or "").strip()
    reason_line = f"Reason: {reason}" if reason else ""

    if event == "submitted":
        title = (
            "Office Leave — Manager action needed"
            if audience == "manager"
            else "Office Leave — New leave request"
        )
        status_line = (
            "Pending your approval — please approve or reject when ready."
            if audience == "manager"
            else "Status: Pending approval — awaiting manager review."
        )
    elif event == "approved":
        title = "Office Leave — Leave approved"
        status_line = "Status: Approved — leave balance has been updated."
    else:
        title = "Office Leave — Leave rejected"
        status_line = "Status: Rejected — leave balance unchanged."

    lines = [title, "", f"{id_part} · {header}", leave_line]
    if reason_line:
        lines.append(reason_line)
    lines.extend(["", status_line])
    return "\n".join(lines)


def format_holiday_teams_message(announcement: dict[str, Any]) -> str:
    holiday_date = announcement.get("holiday_date") or "—"
    description = (announcement.get("description") or "").strip() or "Holiday"
    return "\n".join(
        [
            "Office Leave — Company holiday announced",
            "",
            f"Date: {holiday_date}",
            f"Details: {description}",
            "",
            "All staff: please plan around this office closure.",
        ]
    )


async def _notify_teams(message: str) -> None:
    """
    Fire-and-forget style notification with safe error handling.

    We run `requests.post` in a thread because FastMCP tools are async and the
    Teams webhook call is synchronous.
    """
    try:
        await asyncio.to_thread(send_teams_message, message)
    except Exception:
        logger.exception("Unexpected error notifying Teams.")


def _manager_webhook_for_employee(employee_slug: str) -> str | None:
    """
    Optional "notify manager separately" using department-based webhook mapping.

    Database does not model managers directly, so we approximate "manager channels"
    by posting to a department-specific webhook.
    """

    # 1) Department-specific mapping (preferred)
    mapping_raw = (os.environ.get("TEAMS_MANAGER_WEBHOOK_URL_BY_DEPARTMENT", "")).strip()
    if mapping_raw:
        try:
            mapping = json.loads(mapping_raw)
            if isinstance(mapping, dict):
                emp = db.get_employee(employee_slug)
                if emp.success and isinstance(emp.data, dict):
                    dept = emp.data.get("department")
                    if dept:
                        url = mapping.get(dept)
                        if isinstance(url, str) and url.strip():
                            return url.strip()
        except json.JSONDecodeError:
            logger.warning(
                "Invalid TEAMS_MANAGER_WEBHOOK_URL_BY_DEPARTMENT JSON; expected object mapping department->webhook."
            )

    # 2) Single manager webhook fallback
    url = os.environ.get("TEAMS_MANAGER_WEBHOOK_URL", "").strip()
    return url or None


async def _notify_manager_if_configured(message: str, employee_slug: str | None) -> None:
    if not employee_slug:
        return
    manager_webhook = _manager_webhook_for_employee(employee_slug)
    if manager_webhook:
        await asyncio.to_thread(send_teams_message, message, webhook_url=manager_webhook)


async def apply_leave(
    employee: str,
    leave_type: str,
    start_date: str,
    end_date: str,
    reason: str,
) -> ToolResponse[dict]:
    # FastMCP tool call -> DB mutation -> Teams webhook notification (best-effort).
    result = db.apply_leave(employee, leave_type, start_date, end_date, reason)
    if result.success and isinstance(result.data, dict) and "request" in result.data:
        req = result.data["request"] or {}
        employee_slug = req.get("employee_slug")
        await _notify_teams(format_leave_teams_message("submitted", req, audience="channel"))
        await _notify_manager_if_configured(
            format_leave_teams_message("submitted", req, audience="manager"),
            employee_slug,
        )

        # Prefab UI-style success payload (best-effort; the actual UI adapter may vary).
        result.data["ui_success_notification"] = {
            "title": "Leave request submitted",
            "message": f"Sent to approval. Request #{req.get('id')}.",
            "variant": "success",
        }
    return result


async def approve_leave(request_id: int) -> ToolResponse[dict]:
    result = db.approve_leave(request_id)
    if result.success and isinstance(result.data, dict) and "request" in result.data:
        req = result.data["request"] or {}
        employee_slug = req.get("employee_slug")
        msg = format_leave_teams_message("approved", req, audience="channel")
        await _notify_teams(msg)
        await _notify_manager_if_configured(
            format_leave_teams_message("approved", req, audience="manager"),
            employee_slug,
        )
    return result


async def reject_leave(request_id: int) -> ToolResponse[dict]:
    result = db.reject_leave(request_id)
    if result.success and isinstance(result.data, dict) and "request" in result.data:
        req = result.data["request"] or {}
        employee_slug = req.get("employee_slug")
        msg = format_leave_teams_message("rejected", req, audience="channel")
        await _notify_teams(msg)
        await _notify_manager_if_configured(
            format_leave_teams_message("rejected", req, audience="manager"),
            employee_slug,
        )
    return result


async def announce_holiday(holiday_date: str, description: str) -> ToolResponse[dict]:
    result = db.announce_holiday(holiday_date, description)
    if result.success and isinstance(result.data, dict) and "announcement" in result.data:
        ann = result.data["announcement"] or {}
        await _notify_teams(format_holiday_teams_message(ann))
    return result

