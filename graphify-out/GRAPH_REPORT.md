# Graph Report - talentserv-ai-hackathon-group-11-backend-db  (2026-05-25)

## Corpus Check
- 24 files · ~5,826 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 209 nodes · 369 edges · 21 communities (15 shown, 6 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 62 edges (avg confidence: 0.63)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `96f90f11`
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
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 22|Community 22]]

## God Nodes (most connected - your core abstractions)
1. `ToolResponse` - 25 edges
2. `utc_now_iso()` - 16 edges
3. `str` - 15 edges
4. `Employee` - 13 edges
5. `LeaveRequest` - 13 edges
6. `Office Leave MCP` - 13 edges
7. `str` - 12 edges
8. `generate_leave_advice_with_grok()` - 11 edges
9. `apply_leave()` - 11 edges
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

## Communities (21 total, 6 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.22
Nodes (33): date, Employee, float, LeaveRequest, Row, apply_leave(), calendar_days_inclusive(), check_leave_status() (+25 more)

### Community 1 - "Community 1"
Cohesion: 0.11
Nodes (32): LeaveAdvice, default_next_steps(), generate_fallback_advice(), generate_leave_advice_with_grok(), parse_json_from_content(), Any, str, LeaveAdvice (+24 more)

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (23): After any bootstrap, Both MCPs at once, code:bash (curl -fsSL https://raw.githubusercontent.com/devinraina258/t), code:bash (python scripts/bootstrap_mcp.py --all), code:powershell (irm https://raw.githubusercontent.com/devinraina258/talentse), code:bash (python scripts/bootstrap_mcp.py --office-leave), code:bash (curl -fsSL https://raw.githubusercontent.com/devinraina258/t), code:powershell (irm https://raw.githubusercontent.com/devinraina258/talentse) (+15 more)

### Community 3 - "Community 3"
Cohesion: 0.08
Nodes (24): Add to Cursor (one curl per MCP), Both MCPs, code:bash (curl -fsSL https://raw.githubusercontent.com/devinraina258/t), code:bash (npm run graphify:sync), code:bash (graphify query "how does apply_leave connect to the database), code:bash (curl -fsSL https://raw.githubusercontent.com/devinraina258/t), code:powershell (irm https://raw.githubusercontent.com/devinraina258/talentse), code:bash (curl -fsSL https://raw.githubusercontent.com/devinraina258/t) (+16 more)

### Community 4 - "Community 4"
Cohesion: 0.16
Nodes (5): init_db(), Connection, Path, run_sql_file(), temp_db()

### Community 5 - "Community 5"
Cohesion: 0.17
Nodes (11): DATABASE_PATH, args, command, cwd, mcpServers, graphify, office-leave, args (+3 more)

### Community 6 - "Community 6"
Cohesion: 0.18
Nodes (11): 1. Create the database, 2. Environment, 3. Run tests, 4. Run the MCP server (stdio), code:bash (git clone https://github.com/devinraina258/talentserv-ai-hac), code:bash (python scripts/init_db.py), code:bash (copy .env.example .env), code:bash (pytest) (+3 more)

### Community 7 - "Community 7"
Cohesion: 0.38
Nodes (13): bool, ensure_venv(), main(), merge_mcp_server(), print_done(), int, Path, str (+5 more)

### Community 8 - "Community 8"
Cohesion: 0.27
Nodes (8): devDependencies, husky, name, private, scripts, graphify:sync, graphify:sync:unix, prepare

### Community 12 - "Community 12"
Cohesion: 0.47
Nodes (5): main(), int, str, Export graphify-out/graph.json as a compact JSONL tree for LLM context.  Each li, _walk_tree()

## Knowledge Gaps
- **55 isolated node(s):** `prepare`, `graphify:sync`, `graphify:sync:unix`, `husky`, `Any` (+50 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolResponse` connect `Community 0` to `Community 1`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Why does `Office Leave MCP` connect `Community 3` to `Community 6`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `utc_now_iso()` connect `Community 0` to `Community 1`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `ToolResponse` (e.g. with `list_employees()` and `get_employee()`) actually correct?**
  _`ToolResponse` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `utc_now_iso()` (e.g. with `generate_fallback_advice()` and `generate_leave_advice_with_grok()`) actually correct?**
  _`utc_now_iso()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `str` (e.g. with `Employee` and `LeaveRequest`) actually correct?**
  _`str` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Employee` (e.g. with `row_to_employee()` and `Path`) actually correct?**
  _`Employee` has 11 INFERRED edges - model-reasoned connections that need verification._