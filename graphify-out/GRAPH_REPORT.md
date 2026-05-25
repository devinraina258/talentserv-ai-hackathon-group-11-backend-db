# Graph Report - talentserv-ai-hackathon-group-11-backend-db  (2026-05-25)

## Corpus Check
- 32 files · ~4,324 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 124 nodes · 175 edges · 13 communities
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 24 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `69c59ebc`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]

## God Nodes (most connected - your core abstractions)
1. `utc_now_iso()` - 12 edges
2. `Office Leave MCP` - 11 edges
3. `ToolResponse` - 10 edges
4. `connect()` - 9 edges
5. `get_employee()` - 8 edges
6. `apply_leave()` - 8 edges
7. `_json_response()` - 8 edges
8. `resolve_slug()` - 7 edges
9. `check_leave_status()` - 7 edges
10. `get_employee_context_for_advice()` - 7 edges

## Surprising Connections (you probably didn't know these)
- `temp_db()` --calls--> `init_db()`  [INFERRED]
  tests/test_tools.py → scripts/init_db.py
- `row_to_leave_request()` --calls--> `LeaveRequest`  [INFERRED]
  src/db.py → src/models.py
- `generate_fallback_advice()` --calls--> `utc_now_iso()`  [INFERRED]
  src/grok_client.py → src/models.py
- `generate_leave_advice_with_grok()` --calls--> `utc_now_iso()`  [INFERRED]
  src/grok_client.py → src/models.py
- `advise_on_leave()` --calls--> `generate_leave_advice_with_grok()`  [INFERRED]
  src/server.py → src/grok_client.py

## Communities (13 total, 0 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.21
Nodes (22): apply_leave(), calendar_days_inclusive(), check_leave_status(), connect(), _fetch_requests(), get_db_path(), get_employee(), get_employee_context_for_advice() (+14 more)

### Community 1 - "Community 1"
Cohesion: 0.17
Nodes (3): init_db(), run_sql_file(), temp_db()

### Community 2 - "Community 2"
Cohesion: 0.14
Nodes (15): Add to Cursor, code:bash (copy .cursor\mcp.json.example .cursor\mcp.json), code:bash (gh auth login), code:bash (pip install "graphifyy[mcp]>=0.8.14"), code:bash (npm run graphify:sync), code:bash (graphify query "how does apply_leave connect to the database), Employees (seed data), Example prompts in Cursor (+7 more)

### Community 3 - "Community 3"
Cohesion: 0.18
Nodes (11): 1. Create the database, 2. Environment, 3. Run tests, 4. Run the MCP server (stdio), code:bash (git clone https://github.com/devinraina258/talentserv-ai-hac), code:bash (python scripts/init_db.py), code:bash (copy .env.example .env), code:bash (pytest) (+3 more)

### Community 4 - "Community 4"
Cohesion: 0.12
Nodes (19): apply_leave(), check_leave_status(), employees_resource(), get_employee(), get_leave_balance(), _json_response(), leave_assistant(), list_employees() (+11 more)

### Community 5 - "Community 5"
Cohesion: 0.67
Nodes (5): default_next_steps(), generate_fallback_advice(), generate_leave_advice_with_grok(), parse_json_from_content(), LeaveAdvice

### Community 6 - "Community 6"
Cohesion: 0.17
Nodes (11): DATABASE_PATH, args, command, cwd, mcpServers, graphify, office-leave, args (+3 more)

### Community 7 - "Community 7"
Cohesion: 0.67
Nodes (3): main(), Export graphify-out/graph.json as a compact JSONL tree for LLM context.  Each li, _walk_tree()

### Community 8 - "Community 8"
Cohesion: 0.22
Nodes (8): devDependencies, husky, name, private, scripts, graphify:sync, graphify:sync:unix, prepare

## Knowledge Gaps
- **28 isolated node(s):** `name`, `private`, `prepare`, `graphify:sync`, `graphify:sync:unix` (+23 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `advise_on_leave()` connect `Community 0` to `Community 4`, `Community 5`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Why does `utc_now_iso()` connect `Community 0` to `Community 5`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `utc_now_iso()` (e.g. with `list_employees()` and `get_employee()`) actually correct?**
  _`utc_now_iso()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `ToolResponse` (e.g. with `list_employees()` and `get_employee()`) actually correct?**
  _`ToolResponse` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `get_employee()` (e.g. with `ToolResponse` and `utc_now_iso()`) actually correct?**
  _`get_employee()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `name`, `private`, `prepare` to the rest of the system?**
  _39 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.14166666666666666 - nodes in this community are weakly interconnected._