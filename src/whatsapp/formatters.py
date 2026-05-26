from __future__ import annotations

from typing import Any

from src.models import LeaveAdvice, ToolResponse


def format_help() -> str:
    return (
        "Office Leave bot (demo)\n"
        "help — this menu\n"
        "list — all employees + balances\n"
        "balance — your balances\n"
        "status — your latest leave request\n"
        "requests — your recent requests\n"
        "apply annual 2026-06-10 2026-06-11 family trip\n"
        "advise Can I take 2 days next week?"
    )


def format_error(message: str) -> str:
    return message


def format_employees(result: ToolResponse[list[dict]]) -> str:
    if not result.success or not result.data:
        return result.error or "No employees found."
    lines = ["Employees:"]
    for e in result.data:
        lines.append(
            f"• {e.get('display_name', e.get('slug'))}: "
            f"{e.get('annual_remaining')} annual, {e.get('sick_remaining')} sick"
        )
    return "\n".join(lines)


def format_balance(result: ToolResponse[dict]) -> str:
    if not result.success or not result.data:
        return result.error or "Could not load balance."
    d = result.data
    name = d.get("display_name") or d.get("employee", "You")
    return (
        f"{name}: {d.get('annual_remaining')} annual days, "
        f"{d.get('sick_remaining')} sick days remaining."
    )


def format_status(result: ToolResponse[dict]) -> str:
    if not result.success or not result.data:
        return result.error or "No leave request found."
    d = result.data
    if "request" in d:
        d = d["request"]
    return (
        f"Request #{d.get('id')}: {d.get('leave_type')} "
        f"{d.get('start_date')} → {d.get('end_date')} "
        f"({d.get('days')} days) — {d.get('status')}"
    )


def format_requests(result: ToolResponse[list[dict]]) -> str:
    if not result.success:
        return result.error or "Could not load requests."
    reqs = result.data or []
    if not reqs:
        return "No leave requests yet."
    lines = ["Your requests:"]
    for r in reqs[:5]:
        lines.append(
            f"• #{r.get('id')} {r.get('leave_type')} {r.get('start_date')} "
            f"({r.get('status')})"
        )
    return "\n".join(lines)


def format_apply(result: ToolResponse[dict]) -> str:
    if not result.success:
        return result.error or "Apply failed."
    req = (result.data or {}).get("request", {})
    return (
        f"Submitted request #{req.get('id')} ({req.get('leave_type')}, "
        f"{req.get('days')} days) — status: {req.get('status')}."
    )


def format_advice(advice: LeaveAdvice) -> str:
    steps = advice.next_steps[:2]
    extra = f"\nNext: {steps[0]}" if steps else ""
    return f"{advice.recommendation}{extra}"
