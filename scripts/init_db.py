#!/usr/bin/env python3
"""Create SQLite database from schema.sql and seed.sql."""
from __future__ import annotations

import os
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SQL_DIR = ROOT / "sql"
DEFAULT_DB = ROOT / "data" / "employees.db"


def run_sql_file(conn: sqlite3.Connection, path: Path) -> None:
    sql = path.read_text(encoding="utf-8")
    conn.executescript(sql)


def init_db(db_path: Path | None = None) -> Path:
    db_path = db_path or Path(os.environ.get("DATABASE_PATH", DEFAULT_DB))
    if not db_path.is_absolute():
        db_path = ROOT / db_path

    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    try:
        run_sql_file(conn, SQL_DIR / "schema.sql")
        run_sql_file(conn, SQL_DIR / "seed.sql")
        conn.commit()
        count = conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
        print(f"Database ready: {db_path}")
        print(f"Employees seeded: {count}")
    finally:
        conn.close()

    return db_path


if __name__ == "__main__":
    init_db()
