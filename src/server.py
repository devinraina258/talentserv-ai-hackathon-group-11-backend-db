#!/usr/bin/env python3
"""FastMCP office leave server — stdio transport for Cursor / Claude."""
from __future__ import annotations

import json
from typing import Any

from dotenv import load_dotenv
from fastmcp import FastMCP

from src import db
from src.grok_client import (
    generate_leave_advice_with_grok,
    generate_output_recommendations,
    grok_enrich_enabled,
)
from src.models import ToolResponse, leave_advice_to_grok, utc_now_iso

load_dotenv()

mcp = FastMCP("office-leave-agent")


def _payload_from_result(result: Any) -> dict[str, Any]:
    if hasattr(result, "to_dict"):
        return result.to_dict()
    if isinstance(result, dict):
        return result
    return {"success": True, "data": result}


def _employee_slug_from_args(args: dict[str, Any] | None) -> str | None:
    if not args:
        return None
    employee = args.get("employee")
    if employee:
        return str(employee)
    return None


async def _employee_context_for_args(args: dict[str, Any] | None) -> dict[str, Any] | None:
    slug = _employee_slug_from_args(args)
    if not slug:
        return None
    ctx = db.get_employee_context_for_advice(slug)
    return ctx.data if ctx.success else None


async def _json_response_enriched(
    result: Any,
    *,
    source: str,
    args: dict[str, Any] | None = None,
    grok: dict[str, Any] | None = None,
) -> str:
    payload = _payload_from_result(result)
    if grok is not None:
        payload["grok"] = grok
    elif grok_enrich_enabled():
        employee_context = await _employee_context_for_args(args)
        suggestions = await generate_output_recommendations(
            source,
            args or {},
            payload,
            employee_context,
        )
        payload["grok"] = suggestions.to_dict()
    return json.dumps(payload, indent=2)


async def _resource_response_enriched(
    resource_uri: str,
    raw_json: str,
) -> str:
    try:
        content = json.loads(raw_json)
    except json.JSONDecodeError:
        content = {"raw": raw_json}

    wrapper: dict[str, Any] = {
        "resource": resource_uri,
        "content": content,
    }
    if grok_enrich_enabled():
        result_payload = {"success": True, "data": content}
        suggestions = await generate_output_recommendations(
            resource_uri,
            {},
            result_payload,
            None,
        )
        wrapper["grok"] = suggestions.to_dict()
    return json.dumps(wrapper, indent=2)


@mcp.tool
async def list_employees() -> str:
    """List all office employees with leave balances."""
    return await _json_response_enriched(
        db.list_employees(), source="list_employees", args={}
    )


@mcp.tool
async def get_employee(employee: str) -> str:
    """Get employee profile and leave balances. employee: slug or name (devin, nisha, gautam)."""
    return await _json_response_enriched(
        db.get_employee(employee),
        source="get_employee",
        args={"employee": employee},
    )


@mcp.tool
async def get_leave_balance(employee: str) -> str:
    """Get remaining annual and sick leave for an employee."""
    return await _json_response_enriched(
        db.get_leave_balance(employee),
        source="get_leave_balance",
        args={"employee": employee},
    )


@mcp.tool
async def apply_leave(
    employee: str,
    leave_type: str,
    start_date: str,
    end_date: str,
    reason: str,
) -> str:
    """Submit a pending leave request. Dates: YYYY-MM-DD. leave_type: annual or sick."""
    args = {
        "employee": employee,
        "leave_type": leave_type,
        "start_date": start_date,
        "end_date": end_date,
        "reason": reason,
    }
    return await _json_response_enriched(
        db.apply_leave(employee, leave_type, start_date, end_date, reason),
        source="apply_leave",
        args=args,
    )


@mcp.tool
async def check_leave_status(
    request_id: int | None = None,
    employee: str | None = None,
) -> str:
    """Check leave request status by request_id or latest request for employee."""
    args: dict[str, Any] = {}
    if request_id is not None:
        args["request_id"] = request_id
    if employee is not None:
        args["employee"] = employee
    return await _json_response_enriched(
        db.check_leave_status(request_id, employee),
        source="check_leave_status",
        args=args,
    )


@mcp.tool
async def list_leave_requests(
    employee: str | None = None,
    status: str | None = None,
) -> str:
    """List leave requests, optionally filtered by employee slug and status."""
    args: dict[str, Any] = {}
    if employee is not None:
        args["employee"] = employee
    if status is not None:
        args["status"] = status
    return await _json_response_enriched(
        db.list_leave_requests(employee, status),
        source="list_leave_requests",
        args=args,
    )


@mcp.tool
async def advise_on_leave(employee: str, question: str) -> str:
    """Get AI leave guidance using Grok from employee data and balances."""
    args = {"employee": employee, "question": question}
    ctx = db.get_employee_context_for_advice(employee)
    if not ctx.success:
        return await _json_response_enriched(ctx, source="advise_on_leave", args=args)

    advice = await generate_leave_advice_with_grok(ctx.data or {}, question)
    return await _json_response_enriched(
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
        ),
        source="advise_on_leave",
        args=args,
        grok=leave_advice_to_grok(advice),
    )


@mcp.resource("leave://employees")
async def employees_resource() -> str:
    """Directory of employees and departments."""
    return await _resource_response_enriched(
        "leave://employees",
        db.get_employees_resource(),
    )


@mcp.resource("leave://policy")
async def policy_resource() -> str:
    """Office leave policy rules."""
    return await _resource_response_enriched(
        "leave://policy",
        db.get_policy_resource(),
    )


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
