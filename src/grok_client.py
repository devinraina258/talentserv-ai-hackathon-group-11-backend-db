from __future__ import annotations

import json
import os
import re
from typing import Any

import httpx

from src.models import LeaveAdvice, utc_now_iso

GROK_URL = os.environ.get("GROK_API_URL", "https://api.x.ai/v1")
GROK_MODEL = os.environ.get("GROK_MODEL", "grok-2-1212")


def parse_json_from_content(content: str) -> dict[str, Any]:
    match = re.search(r"\{[\s\S]*\}", content)
    if not match:
        return {}
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return {}


def default_next_steps(context: dict[str, Any]) -> list[str]:
    profile = context.get("profile") or {}
    steps: list[str] = []
    annual = float(profile.get("annual_remaining", 0))
    sick = float(profile.get("sick_remaining", 0))
    if annual < 2:
        steps.append("Annual balance is low — plan leave carefully or speak with HR")
    if sick < 2:
        steps.append("Sick balance is low — keep medical documentation if needed")
    pending = context.get("pending_requests") or []
    if pending:
        steps.append(f"You have {len(pending)} pending request(s) — check status before applying more")
    if not steps:
        steps.append("Use apply_leave with ISO dates (YYYY-MM-DD) to submit a new request")
    return steps


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
            f"Rule-based advice (Grok API key not set or call failed). Question: \"{question}\"."
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
    api_key = os.environ.get("GROK_API_KEY", "")
    if not api_key or api_key == "your_grok_api_key_here":
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
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            parsed = parse_json_from_content(content)
            conf = str(parsed.get("confidence", "medium"))
            if conf not in ("high", "medium", "low"):
                conf = "medium"
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
                confidence=conf,
                next_steps=next_steps,
                source="grok-api",
                timestamp=utc_now_iso(),
                used_grok=True,
            )
    except Exception:
        return generate_fallback_advice(context, question)
