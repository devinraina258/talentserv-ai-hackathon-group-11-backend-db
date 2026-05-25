# Graph Report - talentserv-ai-hackathon-group-11-backend-db  (2026-05-25)

## Corpus Check
- 15 files · ~4,102 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 147 nodes · 292 edges · 14 communities (12 shown, 2 thin omitted)
- Extraction: 79% EXTRACTED · 21% INFERRED · 0% AMBIGUOUS · INFERRED: 62 edges (avg confidence: 0.63)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `32c87e5c`
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
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 12|Community 12]]

## God Nodes (most connected - your core abstractions)
1. `ToolResponse` - 25 edges
2. `utc_now_iso()` - 16 edges
3. `str` - 15 edges
4. `Employee` - 13 edges
5. `LeaveRequest` - 13 edges
6. `str` - 12 edges
7. `generate_leave_advice_with_grok()` - 11 edges
8. `apply_leave()` - 11 edges
9. `Office Leave MCP` - 11 edges
10. `_json_response()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `temp_db()` --calls--> `init_db()`  [INFERRED]
  tests/test_tools.py → scripts/init_db.py
- `Any` --uses--> `ToolResponse`  [INFERRED]
  src/server.py → src/models.py
- `int` --uses--> `ToolResponse`  [INFERRED]
  src/server.py → src/models.py
- `generate_fallback_advice()` --calls--> `utc_now_iso()`  [INFERRED]
  src/grok_client.py → src/models.py
- `generate_leave_advice_with_grok()` --calls--> `utc_now_iso()`  [INFERRED]
  src/grok_client.py → src/models.py

## Communities (14 total, 2 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.25
Nodes (31): date, Employee, float, LeaveRequest, Row, apply_leave(), calendar_days_inclusive(), check_leave_status() (+23 more)

### Community 1 - "Community 1"
Cohesion: 0.16
Nodes (5): init_db(), Connection, Path, run_sql_file(), temp_db()

### Community 2 - "Community 2"
Cohesion: 0.14
Nodes (15): Add to Cursor, code:bash (copy .cursor\mcp.json.example .cursor\mcp.json), code:bash (gh auth login), code:bash (pip install "graphifyy[mcp]>=0.8.14"), code:bash (npm run graphify:sync), code:bash (graphify query "how does apply_leave connect to the database), Employees (seed data), Example prompts in Cursor (+7 more)

### Community 3 - "Community 3"
Cohesion: 0.18
Nodes (11): 1. Create the database, 2. Environment, 3. Run tests, 4. Run the MCP server (stdio), code:bash (git clone https://github.com/devinraina258/talentserv-ai-hac), code:bash (python scripts/init_db.py), code:bash (copy .env.example .env), code:bash (pytest) (+3 more)

### Community 4 - "Community 4"
Cohesion: 0.13
Nodes (24): advise_on_leave(), apply_leave(), check_leave_status(), employees_resource(), get_employee(), get_leave_balance(), _json_response(), leave_assistant() (+16 more)

### Community 5 - "Community 5"
Cohesion: 0.67
Nodes (8): LeaveAdvice, default_next_steps(), generate_fallback_advice(), generate_leave_advice_with_grok(), parse_json_from_content(), Any, str, LeaveAdvice

### Community 6 - "Community 6"
Cohesion: 0.17
Nodes (11): DATABASE_PATH, args, command, cwd, mcpServers, graphify, office-leave, args (+3 more)

### Community 7 - "Community 7"
Cohesion: 0.47
Nodes (5): main(), int, str, Export graphify-out/graph.json as a compact JSONL tree for LLM context.  Each li, _walk_tree()

### Community 8 - "Community 8"
Cohesion: 0.22
Nodes (8): devDependencies, husky, name, private, scripts, graphify:sync, graphify:sync:unix, prepare

## Knowledge Gaps
- **31 isolated node(s):** `name`, `private`, `prepare`, `graphify:sync`, `graphify:sync:unix` (+26 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolResponse` connect `Community 0` to `Community 12`, `Community 4`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Why does `utc_now_iso()` connect `Community 0` to `Community 5`, `Community 12`, `Community 4`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `str` connect `Community 4` to `Community 0`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `ToolResponse` (e.g. with `list_employees()` and `get_employee()`) actually correct?**
  _`ToolResponse` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `utc_now_iso()` (e.g. with `generate_fallback_advice()` and `generate_leave_advice_with_grok()`) actually correct?**
  _`utc_now_iso()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `str` (e.g. with `Employee` and `LeaveRequest`) actually correct?**
  _`str` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Employee` (e.g. with `row_to_employee()` and `Path`) actually correct?**
  _`Employee` has 11 INFERRED edges - model-reasoned connections that need verification._