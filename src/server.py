#!/usr/bin/env python3
"""FastMCP office leave server — stdio transport for Cursor / Claude."""
from __future__ import annotations

import asyncio
import json
from typing import Any

from dotenv import load_dotenv
from fastmcp import FastMCP

from src import db
from src.grok_client import generate_leave_advice_with_grok

load_dotenv()

mcp = FastMCP("office-leave-agent")


def _json_response(result: Any) -> str:
    if hasattr(result, "to_dict"):
        payload = result.to_dict()
    elif isinstance(result, dict):
        payload = result
    else:
        payload = {"success": True, "data": result}
    return json.dumps(payload, indent=2)


@mcp.tool
def list_employees() -> str:
    """List all office employees with leave balances."""
    return _json_response(db.list_employees())


@mcp.tool
def get_employee(employee: str) -> str:
    """Get employee profile and leave balances. employee: slug or name (devin, nisha, gautam)."""
    return _json_response(db.get_employee(employee))


@mcp.tool
def get_leave_balance(employee: str) -> str:
    """Get remaining annual and sick leave for an employee."""
    return _json_response(db.get_leave_balance(employee))


@mcp.tool
def apply_leave(
    employee: str,
    leave_type: str,
    start_date: str,
    end_date: str,
    reason: str,
) -> str:
    """Submit a pending leave request. Dates: YYYY-MM-DD. leave_type: annual or sick."""
    return _json_response(
        db.apply_leave(employee, leave_type, start_date, end_date, reason)
    )


@mcp.tool
def check_leave_status(
    request_id: int | None = None,
    employee: str | None = None,
) -> str:
    """Check leave request status by request_id or latest request for employee."""
    return _json_response(db.check_leave_status(request_id, employee))


@mcp.tool
def list_leave_requests(
    employee: str | None = None,
    status: str | None = None,
) -> str:
    """List leave requests, optionally filtered by employee slug and status."""
    return _json_response(db.list_leave_requests(employee, status))


@mcp.tool
async def advise_on_leave(employee: str, question: str) -> str:
    """Get AI leave guidance using Grok from employee data and balances."""
    ctx = db.get_employee_context_for_advice(employee)
    if not ctx.success:
        return _json_response(ctx)
    advice = await generate_leave_advice_with_grok(ctx.data or {}, question)
    from src.models import ToolResponse, utc_now_iso

    return _json_response(
        ToolResponse(
            success=True,
            data={
                "context": ctx.data,
                "advice": {
                    "recommendation": advice.recommendation,
                    "explanation": advice.explanation,
                    "confidence": advice.confidence,
                    "next_steps": advice.next_steps,
                    "source": advice.source,
                    "used_grok": advice.used_grok,
                    "timestamp": advice.timestamp,
                },
            },
            timestamp=utc_now_iso(),
        )
    )


@mcp.resource("leave://employees")
def employees_resource() -> str:
    """Directory of employees and departments."""
    return db.get_employees_resource()


@mcp.resource("leave://policy")
def policy_resource() -> str:
    """Office leave policy rules."""
    return db.get_policy_resource()


@mcp.prompt
def leave_assistant(employee: str, user_question: str) -> str:
    """Template prompt for leave questions using employee context."""
    ctx = db.get_employee_context_for_advice(employee)
    data = ctx.data if ctx.success else {}
    return f"""You are helping {employee} with office leave.

Employee context:
{json.dumps(data, indent=2)}

User question: {user_question}

Use MCP tools (apply_leave, check_leave_status, get_leave_balance) when the user wants actions.
Be concise and actionable."""


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
