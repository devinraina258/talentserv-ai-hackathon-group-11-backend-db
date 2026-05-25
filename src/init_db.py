"""Create SQLite database from packaged schema.sql and seed.sql."""
from __future__ import annotations

import os
import sqlite3
from pathlib import Path

from src.db import get_workspace_root, resolve_db_path

SQL_DIR = Path(__file__).resolve().parent / "sql"


def run_sql_file(conn: sqlite3.Connection, path: Path) -> None:
    conn.executescript(path.read_text(encoding="utf-8"))


def init_db(db_path: Path | str | None = None) -> Path:
    path = resolve_db_path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()

    schema = SQL_DIR / "schema.sql"
    seed = SQL_DIR / "seed.sql"
    if not schema.is_file() or not seed.is_file():
        raise FileNotFoundError(
            f"SQL files not found under {SQL_DIR}. Reinstall office-leave-mcp package."
        )

    conn = sqlite3.connect(path)
    try:
        run_sql_file(conn, schema)
        run_sql_file(conn, seed)
        conn.commit()
        count = conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
        print(f"Database ready: {path}")
        print(f"Employees seeded: {count}")
    finally:
        conn.close()

    return path


def main() -> None:
    init_db(os.environ.get("DATABASE_PATH"))


if __name__ == "__main__":
    main()
