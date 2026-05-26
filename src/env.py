"""Load .env from Cursor workspace before other modules read os.environ."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

_REPO_ROOT = Path(__file__).resolve().parent.parent


def load_workspace_env() -> None:
    """Load .env from cwd, repo root, and OFFICE_LEAVE_WORKSPACE (MCP sets this)."""
    load_dotenv()
    load_dotenv(_REPO_ROOT / ".env")
    ws = os.environ.get("OFFICE_LEAVE_WORKSPACE", "").strip()
    if ws:
        load_dotenv(Path(ws) / ".env")
