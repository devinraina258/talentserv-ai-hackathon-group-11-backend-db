---
type: "query"
date: "2026-05-25T11:53:35.735217+00:00"
question: "Why does init_db connect Database initialization to Leave database layer?"
contributor: "graphify"
source_nodes: ["init_db", "connect", "resolve_db_path"]
---

# Q: Why does init_db connect Database initialization to Leave database layer?

## Answer

init_db() in src/init_db.py creates and seeds data/employees.db via schema.sql and seed.sql using resolve_db_path() from src/db.py. connect() in src/db.py is the runtime entry for all leave tools; if the DB file is missing it imports and calls init_db(path) before opening SQLite. The graph bridge is this lazy-init coupling: initialization community (CLI office-leave-init-db, init-db.sh) and leave layer (list_employees, apply_leave) share path resolution and the same DB file.

## Source Nodes

- init_db
- connect
- resolve_db_path