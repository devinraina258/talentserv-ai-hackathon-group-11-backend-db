from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

Action = Literal[
    "help",
    "list",
    "balance",
    "status",
    "requests",
    "apply",
    "advise",
    "unknown",
]

_ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass(frozen=True)
class ParsedCommand:
    action: Action
    leave_type: str = ""
    start_date: str = ""
    end_date: str = ""
    reason: str = ""
    question: str = ""
    raw: str = ""


@dataclass(frozen=True)
class ParseError:
    message: str


def _parse_apply(tokens: list[str], raw: str) -> ParsedCommand | ParseError:
    if len(tokens) < 5:
        return ParseError(
            "Usage: apply <annual|sick> <YYYY-MM-DD> <YYYY-MM-DD> <reason>"
        )
    leave_type = tokens[1].lower()
    start_date, end_date = tokens[2], tokens[3]
    if leave_type not in ("annual", "sick"):
        return ParseError("leave_type must be annual or sick")
    if not _ISO_DATE.match(start_date) or not _ISO_DATE.match(end_date):
        return ParseError("Dates must be YYYY-MM-DD")
    reason = " ".join(tokens[4:]).strip()
    if not reason:
        return ParseError("reason is required")
    return ParsedCommand(
        action="apply",
        leave_type=leave_type,
        start_date=start_date,
        end_date=end_date,
        reason=reason,
        raw=raw,
    )


def parse_command(text: str) -> ParsedCommand | ParseError:
    raw = (text or "").strip()
    if not raw:
        return ParseError("Send help for available commands.")

    lowered = raw.lower()
    if lowered in ("help", "?", "menu"):
        return ParsedCommand(action="help", raw=raw)

    if lowered == "list":
        return ParsedCommand(action="list", raw=raw)

    if lowered == "balance":
        return ParsedCommand(action="balance", raw=raw)

    if lowered.startswith("balance "):
        return ParseError("Use balance (no name) — your account is tied to this phone.")

    if lowered == "status":
        return ParsedCommand(action="status", raw=raw)

    if lowered == "requests":
        return ParsedCommand(action="requests", raw=raw)

    if lowered.startswith("apply "):
        return _parse_apply(raw.split(), raw)

    if lowered.startswith("advise "):
        question = raw[6:].strip()
        if not question:
            return ParseError("Usage: advise <your question>")
        return ParsedCommand(action="advise", question=question, raw=raw)

    return ParsedCommand(action="unknown", raw=raw)
