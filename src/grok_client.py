from __future__ import annotations

import json
import os
import re
from typing import Any

import httpx

from src.models import GrokSuggestions, LeaveAdvice, utc_now_iso

GROK_URL = os.environ.get("GROK_API_URL", "https://api.x.ai/v1")
GROK_MODEL = os.environ.get("GROK_MODEL", "grok-2-1212")

VALID_EMPLOYEES = ("devin", "nisha", "gautam")


def grok_enrich_enabled() -> bool:
    return os.environ.get("GROK_ENRICH_OUTPUTS", "1").strip().lower() not in (
        "0",
        "false",
        "no",
        "off",
    )


def _api_key_configured() -> bool:
    api_key = os.environ.get("GROK_API_KEY", "")
    return bool(api_key and api_key != "your_grok_api_key_here")


def parse_json_from_content(content: str) -> dict[str, Any]:
    match = re.search(r"\{[\s\S]*\}", content)
    if not match:
        return {}
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return {}


def default_next_steps(context: dict[str, Any]) -> list[str]:
    profile = context.get("profile") or context if "annual_remaining" in context else {}
    steps: list[str] = []
    annual = float(profile.get("annual_remaining", 0))
    sick = float(profile.get("sick_remaining", 0))
    if annual < 2:
        steps.append("Annual balance is low — plan leave carefully or speak with HR")
    if sick < 2:
        steps.append("Sick balance is low — keep medical documentation if needed")
    pending = context.get("pending_requests") or []
    if pending:
        steps.append(
            f"You have {len(pending)} pending request(s) — check status before applying more"
        )
    if not steps:
        steps.append("Use apply_leave with ISO dates (YYYY-MM-DD) to submit a new request")
    return steps


def _normalize_confidence(value: Any) -> str:
    conf = str(value or "medium")
    if conf not in ("high", "medium", "low"):
        return "medium"
    return conf


def _parse_suggestions_list(parsed: dict[str, Any], fallback: list[str]) -> list[str]:
    raw = parsed.get("suggestions")
    if isinstance(raw, list) and raw:
        return [str(s) for s in raw]
    raw_steps = parsed.get("next_steps")
    if isinstance(raw_steps, list) and raw_steps:
        return [str(s) for s in raw_steps[:3]]
    return fallback[:3] if fallback else ["Review the result and choose a follow-up tool"]


def _parse_next_steps_list(parsed: dict[str, Any], fallback: list[str]) -> list[str]:
    raw = parsed.get("next_steps")
    if isinstance(raw, list) and raw:
        return [str(s) for s in raw]
    return fallback


async def _call_grok(prompt: str) -> str | None:
    if not _api_key_configured():
        return None
    api_key = os.environ.get("GROK_API_KEY", "")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{GROK_URL}/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": GROK_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                },
            )
            response.raise_for_status()
            data = response.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content", "")
    except Exception:
        return None


def _grok_from_parsed(
    parsed: dict[str, Any],
    *,
    content: str,
    fallback_steps: list[str],
    used_grok: bool,
    source: str,
    default_explanation: str,
) -> GrokSuggestions:
    suggestions = _parse_suggestions_list(parsed, fallback_steps)
    next_steps = _parse_next_steps_list(parsed, fallback_steps)
    return GrokSuggestions(
        recommendation=str(
            parsed.get("recommendation", content[:200] or "See explanation.")
        ),
        suggestions=suggestions,
        explanation=str(parsed.get("explanation", default_explanation)),
        confidence=_normalize_confidence(parsed.get("confidence")),
        next_steps=next_steps,
        source=source,
        timestamp=utc_now_iso(),
        used_grok=used_grok,
    )


def generate_fallback_output_recommendations(
    source: str,
    args: dict[str, Any],
    result_payload: dict[str, Any],
    employee_context: dict[str, Any] | None,
) -> GrokSuggestions:
    success = result_payload.get("success", True)
    error = result_payload.get("error") or ""
    data = result_payload.get("data")
    ctx = employee_context or {}
    profile = ctx.get("profile") or (data if isinstance(data, dict) else {}) or {}
    steps: list[str] = []
    suggestions: list[str] = []
    recommendation = ""
    explanation = f"Rule-based guidance after {source}."

    if not success:
        if "unknown" in error.lower() or "supported" in error.lower():
            recommendation = (
                f"Use a valid employee slug: {', '.join(VALID_EMPLOYEES)}."
            )
            suggestions = [
                "Try get_employee with the slug before applying leave",
                "Supported slugs: devin, nisha, gautam",
            ]
            steps = ["Call list_employees to see all profiles and balances"]
        elif "insufficient" in error.lower():
            recommendation = "Requested days exceed remaining balance — shorten the range or change leave type."
            suggestions = [
                "Call get_leave_balance to see remaining days",
                "Reduce end_date or switch leave_type if appropriate",
            ]
            steps = [
                "Adjust dates and retry apply_leave",
                "Ask HR if an exception is needed",
            ]
        else:
            recommendation = error or "The operation failed — review inputs and retry."
            suggestions = ["Check tool arguments and employee slug", "Use list_employees for valid slugs"]
            steps = ["Read the error message and correct parameters"]
        return GrokSuggestions(
            recommendation=recommendation,
            suggestions=suggestions,
            explanation=explanation,
            next_steps=steps,
            confidence="medium",
            source="fallback-rules",
            timestamp=utc_now_iso(),
            used_grok=False,
        )

    if source == "list_employees":
        employees = data if isinstance(data, list) else []
        low = [e for e in employees if float(e.get("annual_remaining", 99)) < 3]
        recommendation = f"Listed {len(employees)} employees. Compare balances before scheduling team leave."
        if low:
            names = ", ".join(e.get("display_name", e.get("slug", "?")) for e in low)
            suggestions.append(f"Low annual balance: {names}")
        suggestions.append("Use get_employee for a full profile before apply_leave")
        steps = ["Pick an employee slug and call get_leave_balance or apply_leave"]

    elif source == "get_employee":
        name = profile.get("display_name", args.get("employee", "Employee"))
        annual = float(profile.get("annual_remaining", 0))
        sick = float(profile.get("sick_remaining", 0))
        recommendation = (
            f"{name}: {annual} annual and {sick} sick days remaining. "
            "Ready to apply or check pending requests."
        )
        suggestions = [f"Department: {profile.get('department', 'n/a')}"]
        steps = default_next_steps(ctx if ctx else {"profile": profile})

    elif source == "get_leave_balance":
        annual = float((data or {}).get("annual_remaining", 0))
        sick = float((data or {}).get("sick_remaining", 0))
        slug = args.get("employee", "employee")
        recommendation = f"{slug} has {annual} annual and {sick} sick days left."
        if annual < 3 or sick < 2:
            suggestions.append("Balance is tight — confirm dates before apply_leave")
        steps = ["Use apply_leave with YYYY-MM-DD dates when ready"]

    elif source == "apply_leave":
        req = (data or {}).get("request", {}) if isinstance(data, dict) else {}
        rid = req.get("id", "?")
        recommendation = (
            f"Leave request #{rid} is pending. Balance is unchanged until approved."
        )
        suggestions = [
            "Track approval with check_leave_status",
            f"Type: {req.get('leave_type', 'n/a')}, days: {req.get('days', 'n/a')}",
        ]
        steps = [
            f"Call check_leave_status with request_id={rid} or employee={args.get('employee')}",
            "Wait for manager approval before assuming time off is booked",
        ]

    elif source == "check_leave_status":
        status = (data or {}).get("status", "unknown") if isinstance(data, dict) else "unknown"
        recommendation = f"Latest request status: {status}."
        if status == "pending":
            suggestions.append("Follow up with your manager if approval is urgent")
        steps = ["Use list_leave_requests for full history if needed"]

    elif source == "list_leave_requests":
        reqs = data if isinstance(data, list) else []
        pending = sum(1 for r in reqs if r.get("status") == "pending")
        recommendation = f"Found {len(reqs)} request(s), {pending} pending."
        suggestions = ["Filter by employee or status to narrow results"]
        steps = ["Use check_leave_status for details on a specific request"]

    elif source == "leave://employees":
        employees = (data or {}).get("employees", []) if isinstance(data, dict) else []
        recommendation = (
            f"Directory lists {len(employees)} employees — use slugs in other tools."
        )
        suggestions = ["Slugs: devin, nisha, gautam", "Call get_employee for balances"]
        steps = ["Select an employee and run get_leave_balance or advise_on_leave"]

    elif source == "leave://policy":
        recommendation = "Review policy limits before apply_leave (annual vs sick, notice rules)."
        suggestions = [
            "Pending requests do not reduce balance until approved",
            "Dates must be YYYY-MM-DD",
        ]
        steps = ["Use apply_leave after confirming balance with get_leave_balance"]

    else:
        recommendation = "Operation completed successfully."
        steps = default_next_steps(ctx) if ctx else ["Continue with related leave tools"]

    if not suggestions:
        suggestions = [recommendation]
    if not steps:
        steps = default_next_steps(ctx) if ctx else ["Use another MCP tool for follow-up"]

    return GrokSuggestions(
        recommendation=recommendation,
        suggestions=suggestions,
        explanation=explanation,
        next_steps=steps,
        confidence="medium",
        source="fallback-rules",
        timestamp=utc_now_iso(),
        used_grok=False,
    )


async def generate_output_recommendations(
    source: str,
    args: dict[str, Any],
    result_payload: dict[str, Any],
    employee_context: dict[str, Any] | None = None,
) -> GrokSuggestions:
    fallback_steps = default_next_steps(employee_context or {})
    fallback = generate_fallback_output_recommendations(
        source, args, result_payload, employee_context
    )

    prompt = f"""You are an office HR leave assistant. The user just invoked MCP "{source}".

Tool/resource arguments (JSON):
{json.dumps(args, indent=2)}

Operation result (JSON):
{json.dumps(result_payload, indent=2)}

Employee context if available (JSON):
{json.dumps(employee_context or {}, indent=2)}

Respond in JSON only with keys:
- recommendation (string, one concise actionable line)
- suggestions (array of 2-4 short strings)
- explanation (string, why this matters given the result)
- confidence (high|medium|low)
- next_steps (array of concrete follow-up actions using MCP tools)

If success is false, focus on recovery. Do not invent employees outside: {', '.join(VALID_EMPLOYEES)}."""

    content = await _call_grok(prompt)
    if not content:
        return fallback

    parsed = parse_json_from_content(content)
    if not parsed.get("recommendation"):
        return fallback

    return _grok_from_parsed(
        parsed,
        content=content,
        fallback_steps=fallback.next_steps or fallback_steps,
        used_grok=True,
        source="grok-api",
        default_explanation=f"AI-generated guidance for {source}.",
    )


def generate_fallback_advice(context: dict[str, Any], question: str) -> LeaveAdvice:
    profile = context.get("profile") or {}
    name = profile.get("display_name", "Employee")
    annual = float(profile.get("annual_remaining", 0))
    sick = float(profile.get("sick_remaining", 0))
    pending = context.get("pending_requests") or []

    recommendation = (
        f"{name} has {annual} annual and {sick} sick days remaining. "
        "You can submit leave via apply_leave; pending requests do not reduce balance until approved."
    )
    if pending:
        recommendation += f" There are {len(pending)} pending request(s) to track."

    return LeaveAdvice(
        recommendation=recommendation,
        explanation=(
            f'Rule-based advice (Grok API key not set or call failed). Question: "{question}".'
        ),
        confidence="medium",
        next_steps=default_next_steps(context),
        source="fallback-rules",
        timestamp=utc_now_iso(),
        used_grok=False,
    )


async def generate_leave_advice_with_grok(
    context: dict[str, Any],
    question: str,
) -> LeaveAdvice:
    if not _api_key_configured():
        return generate_fallback_advice(context, question)

    prompt = f"""You are an office HR leave assistant.
User question: {question}
Employee and leave context (JSON):
{json.dumps(context, indent=2)}

Respond in JSON only with keys:
- recommendation (string, concise actionable advice)
- explanation (string)
- confidence (high|medium|low)
- next_steps (array of strings)

Consider balances, pending requests, and policy. Do not invent employees outside the data."""

    content = await _call_grok(prompt)
    if not content:
        return generate_fallback_advice(context, question)

    parsed = parse_json_from_content(content)
    next_steps = parsed.get("next_steps")
    if not isinstance(next_steps, list):
        next_steps = default_next_steps(context)
    else:
        next_steps = [str(s) for s in next_steps]

    return LeaveAdvice(
        recommendation=str(
            parsed.get("recommendation", content[:200] or "See explanation.")
        ),
        explanation=str(
            parsed.get("explanation", "AI-generated from employee leave data.")
        ),
        confidence=_normalize_confidence(parsed.get("confidence")),
        next_steps=next_steps,
        source="grok-api",
        timestamp=utc_now_iso(),
        used_grok=True,
    )
