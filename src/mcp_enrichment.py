"""Grok header/footer formatting and FastMCP middleware for all office-leave outputs."""
from __future__ import annotations

import json
from typing import Any

import mcp.types as mt
from fastmcp.prompts.base import PromptResult
from fastmcp.resources.base import ResourceResult
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.tools.base import ToolResult
from mcp.types import TextContent

from src import db
from src.grok_client import generate_output_recommendations

GROK_HEADER_LINE = "━━ Grok advisory ━━"
GROK_FOOTER_LINE = "━━ End Grok advisory ━━"

# Every MCP tool on this server (used by tests and middleware).
ENRICHED_TOOL_NAMES: tuple[str, ...] = (
    "list_employees",
    "get_employee",
    "get_leave_balance",
    "apply_leave",
    "check_leave_status",
    "list_leave_requests",
    "advise_on_leave",
)

ENRICHED_RESOURCE_URIS: tuple[str, ...] = (
    "leave://employees",
    "leave://policy",
)

ENRICHED_PROMPT_NAMES: tuple[str, ...] = ("leave_assistant",)


def _grok_text_header(grok: dict[str, Any]) -> str:
    lines = [GROK_HEADER_LINE, grok.get("recommendation", "").strip()]
    suggestions = grok.get("suggestions") or []
    if suggestions:
        lines.append("Suggestions: " + "; ".join(str(s) for s in suggestions[:3]))
    source = grok.get("source", "unknown")
    live = "live" if grok.get("used_grok") else "fallback"
    lines.append(f"Source: {source} ({live})")
    return "\n".join(lines)


def _grok_text_footer(grok: dict[str, Any]) -> str:
    lines: list[str] = []
    next_steps = grok.get("next_steps") or []
    if next_steps:
        lines.append("Next steps:")
        lines.extend(f"  • {step}" for step in next_steps[:5])
    explanation = (grok.get("explanation") or "").strip()
    if explanation:
        lines.append(explanation)
    lines.append(GROK_FOOTER_LINE)
    return "\n".join(lines)


def ordered_payload_with_grok(payload: dict[str, Any], grok: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in payload.items() if k not in ("grok", "grok_footer")}
    return {"grok": grok, **base, "grok_footer": grok}


def format_enriched_response(payload: dict[str, Any]) -> str:
    grok = payload["grok"]
    body = json.dumps(payload, indent=2)
    return f"{_grok_text_header(grok)}\n\n{body}\n\n{_grok_text_footer(grok)}"


def parse_enriched_mcp_response(raw: str) -> dict[str, Any]:
    """Extract the JSON object from a header/footer-wrapped MCP tool string."""
    start = raw.find("{")
    end = raw.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("no JSON object in enriched MCP response")
    return json.loads(raw[start : end + 1])


def is_enriched_response(raw: str) -> bool:
    return GROK_HEADER_LINE in raw and GROK_FOOTER_LINE in raw


def _payload_from_parsed(parsed: Any) -> dict[str, Any]:
    if isinstance(parsed, dict) and (
        "success" in parsed or "data" in parsed or "error" in parsed or "resource" in parsed
    ):
        return parsed
    if isinstance(parsed, dict):
        return {"success": True, "data": parsed}
    return {"success": True, "data": parsed}


async def _employee_context_for_args(args: dict[str, Any] | None) -> dict[str, Any] | None:
    if not args:
        return None
    employee = args.get("employee")
    if not employee:
        return None
    ctx = db.get_employee_context_for_advice(str(employee))
    return ctx.data if ctx.success else None


async def resolve_grok_block(
    payload: dict[str, Any],
    *,
    source: str,
    args: dict[str, Any] | None,
    grok: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if grok is not None:
        return grok
    existing = payload.get("grok_footer") or payload.get("grok")
    if isinstance(existing, dict):
        return existing
    employee_context = await _employee_context_for_args(args)
    suggestions = await generate_output_recommendations(
        source,
        args or {},
        payload,
        employee_context,
    )
    return suggestions.to_dict()


async def ensure_enriched_text(
    raw: str,
    *,
    source: str,
    args: dict[str, Any] | None = None,
    grok: dict[str, Any] | None = None,
) -> str:
    """Apply header/footer + grok bookends to any tool/resource/prompt text response."""
    if is_enriched_response(raw):
        return raw

    payload: dict[str, Any]
    try:
        payload = json.loads(raw.strip())
        payload = _payload_from_parsed(payload)
    except json.JSONDecodeError:
        try:
            payload = _payload_from_parsed(parse_enriched_mcp_response(raw))
        except ValueError:
            payload = {"success": True, "data": raw}

    grok_block = await resolve_grok_block(payload, source=source, args=args, grok=grok)
    return format_enriched_response(ordered_payload_with_grok(payload, grok_block))


def _text_from_content(blocks: list[Any]) -> str | None:
    parts: list[str] = []
    for block in blocks:
        if isinstance(block, TextContent):
            parts.append(block.text)
        elif isinstance(block, dict) and block.get("type") == "text":
            parts.append(str(block.get("text", "")))
        elif getattr(block, "type", None) == "text":
            parts.append(str(getattr(block, "text", "")))
    return "\n".join(parts) if parts else None


def _replace_text_content(blocks: list[Any], new_text: str) -> list[TextContent]:
    return [TextContent(type="text", text=new_text)]


class GrokEnrichmentMiddleware(Middleware):
    """Guarantee Grok header/footer on every tool call, resource read, and prompt."""

    async def on_call_tool(
        self,
        context: MiddlewareContext[mt.CallToolRequestParams],
        call_next,
    ) -> ToolResult:
        result: ToolResult = await call_next(context)
        tool_name = context.message.name
        args = dict(context.message.arguments or {})
        text = _text_from_content(result.content)
        if not text:
            return result

        enriched = await ensure_enriched_text(text, source=tool_name, args=args)
        if enriched == text:
            return result

        structured = result.structured_content
        if isinstance(structured, dict) and "result" in structured:
            structured = {**structured, "result": enriched}
        return ToolResult(content=_replace_text_content(result.content, enriched), structured_content=structured)

    async def on_read_resource(
        self,
        context: MiddlewareContext[mt.ReadResourceRequestParams],
        call_next,
    ) -> ResourceResult:
        result: ResourceResult = await call_next(context)
        uri = str(context.message.uri)
        text = _text_from_content(result.content)
        if not text:
            return result

        enriched = await ensure_enriched_text(text, source=uri, args={})
        if enriched == text:
            return result
        return ResourceResult(content=_replace_text_content(result.content, enriched))

    async def on_get_prompt(
        self,
        context: MiddlewareContext[mt.GetPromptRequestParams],
        call_next,
    ) -> PromptResult:
        result: PromptResult = await call_next(context)
        prompt_name = context.message.name
        if prompt_name not in ENRICHED_PROMPT_NAMES:
            return result

        args = dict(context.message.arguments or {})
        messages = []
        for msg in result.messages:
            if msg.role != "user" or not msg.content:
                messages.append(msg)
                continue
            text = msg.content.text if hasattr(msg.content, "text") else str(msg.content)
            enriched = await ensure_enriched_text(
                text, source=prompt_name, args=args
            )
            if enriched == text:
                messages.append(msg)
            else:
                messages.append(
                    mt.PromptMessage(
                        role=msg.role,
                        content=mt.TextContent(type="text", text=enriched),
                    )
                )
        return PromptResult(messages=messages) if messages else result
