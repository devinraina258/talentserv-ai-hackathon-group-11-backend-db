from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Generic, TypeVar

T = TypeVar("T")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class ToolResponse(Generic[T]):
    success: bool
    data: T | None = None
    error: str | None = None
    timestamp: str = ""

    def to_dict(self) -> dict[str, Any]:
        if not self.timestamp:
            self.timestamp = utc_now_iso()
        return asdict(self)


@dataclass
class Employee:
    id: int
    slug: str
    display_name: str
    department: str
    email: str
    annual_remaining: float
    sick_remaining: float


@dataclass
class LeaveRequest:
    id: int
    employee_slug: str
    employee_name: str
    leave_type: str
    start_date: str
    end_date: str
    days: float
    reason: str
    status: str
    created_at: str
    updated_at: str


@dataclass
class LeaveAdvice:
    recommendation: str
    explanation: str
    confidence: str
    next_steps: list[str]
    source: str
    timestamp: str
    used_grok: bool


@dataclass
class GrokSuggestions:
    recommendation: str
    suggestions: list[str]
    explanation: str
    next_steps: list[str]
    confidence: str
    source: str
    timestamp: str
    used_grok: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def leave_advice_to_grok(advice: LeaveAdvice) -> dict[str, Any]:
    """Map LeaveAdvice from advise_on_leave to the standard grok block shape."""
    suggestions = [
        s for s in advice.next_steps[:2] if s
    ] or [advice.recommendation]
    return GrokSuggestions(
        recommendation=advice.recommendation,
        suggestions=suggestions,
        explanation=advice.explanation,
        next_steps=advice.next_steps,
        confidence=advice.confidence,
        source=advice.source,
        timestamp=advice.timestamp,
        used_grok=advice.used_grok,
    ).to_dict()
