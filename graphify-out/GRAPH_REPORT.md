# Graph Report - talentserv-ai-hackathon-group-11-backend-db  (2026-05-27)

## Corpus Check
- 65 files · ~19,483 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 634 nodes · 1148 edges · 61 communities (42 shown, 19 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 179 edges (avg confidence: 0.7)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `24a95928`
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
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]

## God Nodes (most connected - your core abstractions)
1. `ToolResponse` - 30 edges
2. `_json_response_enriched()` - 23 edges
3. `utc_now_iso()` - 18 edges
4. `generate_output_recommendations()` - 18 edges
5. `generate_leave_advice_with_grok()` - 18 edges
6. `ensure_enriched_text()` - 17 edges
7. `str` - 17 edges
8. `LeaveAdvice` - 15 edges
9. `str` - 15 edges
10. `str` - 15 edges

## Surprising Connections (you probably didn't know these)
- `test_puter_model_prefix()` --calls--> `_effective_model()`  [INFERRED]
  tests/test_grok_enrichment.py → src/grok_client.py
- `test_fallback_unknown_employee()` --calls--> `generate_fallback_output_recommendations()`  [INFERRED]
  tests/test_grok_enrichment.py → src/grok_client.py
- `office-leave MCP launcher` --semantically_similar_to--> `Office Leave MCP`  [INFERRED] [semantically similar]
  docs/MCP_SETUP.md → README.md
- `graphify MCP launcher` --semantically_similar_to--> `graphify knowledge graph`  [INFERRED] [semantically similar]
  docs/MCP_SETUP.md → README.md
- `temp_db()` --calls--> `init_db()`  [INFERRED]
  tests/test_whatsapp_commands.py → src/init_db.py

## Hyperedges (group relationships)
- **Dual MCP hackathon stack** — readme_office_leave_mcp, readme_graphify_knowledge_graph, mcp_setup_office_leave_launcher, mcp_setup_graphify_launcher [INFERRED 0.85]

## Communities (61 total, 19 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.19
Nodes (16): _employee_context_for_args(), _employee_slug_from_args(), _format_enriched_response(), _grok_text_footer(), _grok_text_header(), _json_response_enriched(), _ordered_payload_with_grok(), parse_enriched_mcp_response() (+8 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (43): 1. Groomed Requirements Document, 2. Solution Plan / Implementation Plan, 3. Product / Technical Architecture, 4. Test Plan and Test Cases, 5. Detailed Critical Review, 6. Agentic Coding Evidence, 7. Source Code and Deployment, Acceptance criteria (+35 more)

### Community 2 - "Community 2"
Cohesion: 0.21
Nodes (35): date, Employee, float, LeaveRequest, Row, apply_leave(), calendar_days_inclusive(), check_leave_status() (+27 more)

### Community 3 - "Community 3"
Cohesion: 0.17
Nodes (19): CopyTo(), create_shortcut(), fixup_dbi(), get_root_hkey(), get_shortcuts_folder(), get_special_folder_path(), get_system_dir(), install() (+11 more)

### Community 4 - "Community 4"
Cohesion: 0.23
Nodes (28): GrokSuggestions, LeaveAdvice, _api_key_configured(), _call_grok(), _chat_completions_url(), default_next_steps(), _effective_model(), generate_fallback_advice() (+20 more)

### Community 5 - "Community 5"
Cohesion: 0.12
Nodes (16): DATABASE_PATH, GROK_API_URL, GROK_ENRICH_OUTPUTS, GROK_MODEL, GROK_PROVIDER, OFFICE_LEAVE_WORKSPACE, args, command (+8 more)

### Community 6 - "Community 6"
Cohesion: 0.12
Nodes (9): init_db(), main(), Connection, Path, str, run_sql_file(), temp_db(), temp_db() (+1 more)

### Community 7 - "Community 7"
Cohesion: 0.27
Nodes (8): devDependencies, husky, name, private, scripts, graphify:sync, graphify:sync:unix, prepare

### Community 8 - "Community 8"
Cohesion: 0.32
Nodes (8): clone-free MCP install via curl, graphify MCP launcher, office-leave MCP launcher, graphify knowledge graph, Grok tool response enrichment, Office Leave MCP, SQLite employees database, CI graphify-out sync workflow

### Community 10 - "Community 10"
Cohesion: 0.60
Nodes (4): find_and_run(), main(), A test runner for pywin32, run_test()

### Community 11 - "Community 11"
Cohesion: 0.47
Nodes (5): main(), int, str, Export graphify-out/graph.json as a compact JSONL tree for LLM context.  Each li, _walk_tree()

### Community 12 - "Community 12"
Cohesion: 0.21
Nodes (13): Request, Response, load_workspace_env(), Load .env from Cursor workspace before other modules read os.environ., Load .env from cwd, repo root, and OFFICE_LEAVE_WORKSPACE (MCP sets this)., bool, str, health() (+5 more)

### Community 26 - "Community 26"
Cohesion: 0.22
Nodes (9): get_employee(), get_leave_balance(), Get employee profile and leave balances. employee: slug or name (devin, nisha, g, Get employee profile and leave balances. employee: slug or name (devin, nisha, g, Get remaining annual and sick leave for an employee., Get remaining annual and sick leave for an employee., Get employee profile and leave balances. employee: slug or name (devin, nisha, g, Get employee profile and leave balances. employee: slug or name (devin, nisha, g (+1 more)

### Community 32 - "Community 32"
Cohesion: 0.07
Nodes (30): 1. Create the database, 2. Environment, 3. Run tests, 4. Run the MCP server (stdio), Add to Cursor, code:bash (curl -fsSL https://raw.githubusercontent.com/devinraina258/t), code:bash (npm run graphify:sync), code:bash (graphify query "how does apply_leave connect to the database) (+22 more)

### Community 33 - "Community 33"
Cohesion: 0.08
Nodes (24): After install, Both servers, code:bash (curl -fsSL https://raw.githubusercontent.com/devinraina258/t), code:powershell (irm https://raw.githubusercontent.com/devinraina258/talentse), code:bash (python scripts/mcp_install_lib.py office-leave), code:bash (curl -fsSL https://raw.githubusercontent.com/devinraina258/t), code:powershell (irm https://raw.githubusercontent.com/devinraina258/talentse), code:bash (python scripts/mcp_install_lib.py graphify) (+16 more)

### Community 34 - "Community 34"
Cohesion: 0.26
Nodes (18): ReadResourceRequestParams, ResourceResult, _employee_context_for_args(), ensure_enriched_text(), format_enriched_response(), _grok_text_footer(), _grok_text_header(), is_enriched_response() (+10 more)

### Community 35 - "Community 35"
Cohesion: 0.50
Nodes (3): Answer, Q: Why does init_db connect Database initialization to Leave database layer?, Source Nodes

### Community 36 - "Community 36"
Cohesion: 0.50
Nodes (3): Answer, Q: Is grok giving recommendations for MCP office-leave?, Source Nodes

### Community 37 - "Community 37"
Cohesion: 0.13
Nodes (29): bool, int, Path, str, allow(), allow_note(), allow_updated_shell(), cache_key() (+21 more)

### Community 39 - "Community 39"
Cohesion: 0.18
Nodes (10): cache-cow hooks (Cursor), code:powershell (Get-Content $env:TEMP\cursor-hooks.log -Wait -Tail 20), code:bash (git update-index --chmod=+x .cursor/hooks/*.sh), code:bash (chmod +x .cursor/hooks/*.sh), Configuration, Make scripts executable (Git on Windows), Prerequisites, Upstream (+2 more)

### Community 40 - "Community 40"
Cohesion: 0.29
Nodes (6): hooks, postToolUse, preCompact, preToolUse, sessionStart, version

### Community 47 - "Community 47"
Cohesion: 0.22
Nodes (23): ensure_venv(), main(), merge_mcp_server(), print_done(), bool, int, Path, str (+15 more)

### Community 48 - "Community 48"
Cohesion: 0.10
Nodes (22): Middleware, GrokEnrichmentMiddleware, Guarantee Grok header/footer on every tool call, resource read, and prompt., check_leave_status(), employees_resource(), list_leave_requests(), _payload_from_result(), Any (+14 more)

### Community 49 - "Community 49"
Cohesion: 0.14
Nodes (29): ParsedCommand, str, str, bool, str, list still requires registration per plan — verify registered user can list., test_handle_apply_for_mapped_user(), test_handle_balance_for_mapped_user() (+21 more)

### Community 50 - "Community 50"
Cohesion: 0.40
Nodes (5): apply_leave(), Submit a pending leave request. Dates: YYYY-MM-DD. leave_type: annual or sick., Submit a pending leave request. Dates: YYYY-MM-DD. leave_type: annual or sick., Submit a pending leave request. Dates: YYYY-MM-DD. leave_type: annual or sick., Submit a pending leave request. Dates: YYYY-MM-DD. leave_type: annual or sick.

### Community 51 - "Community 51"
Cohesion: 0.40
Nodes (5): leave_assistant(), Template prompt for leave questions using employee context., Template prompt for leave questions using employee context., Template prompt for leave questions using employee context., Template prompt for leave questions using employee context.

### Community 52 - "Community 52"
Cohesion: 0.14
Nodes (23): run(), grok_enrich_enabled(), Grok enrichment is always on for MCP tools/resources., parse_enriched_mcp_response(), Extract the JSON object from a header/footer-wrapped MCP tool string., advise_on_leave(), Get AI leave guidance using Grok from employee data and balances., Get AI leave guidance using Grok from employee data and balances. (+15 more)

### Community 53 - "Community 53"
Cohesion: 0.11
Nodes (17): Before demo (once), code:powershell (powershell -ExecutionPolicy Bypass -File .\scripts\demo.ps1), code:powershell (cd C:\Users\Admin\Documents\talentserv-ai-hackathon-group-11), code:powershell (& $py -m pip install -e ".[whatsapp]"), code:powershell (cd C:\Users\Admin\Documents\talentserv-ai-hackathon-group-11), code:powershell (& "C:\Program Files (x86)\cloudflared\cloudflared.exe" tunne), code:powershell (cd C:\Users\Admin\Documents\talentserv-ai-hackathon-group-11), code:text (https://YOUR-NEW-URL.trycloudflare.com/whatsapp/webhook) (+9 more)

### Community 55 - "Community 55"
Cohesion: 0.12
Nodes (16): 1. Install, 2. Twilio WhatsApp Sandbox, 3. Run webhook locally + ngrok, 4. Try commands on WhatsApp, 5. Optional: Render (free tier), code:bash (pip install -e ".[dev,whatsapp]"), code:env (WHATSAPP_PHONE_MAP={"+1YOUR_MOBILE":"devin"}), code:bash (office-leave-init-db) (+8 more)

### Community 56 - "Community 56"
Cohesion: 0.33
Nodes (11): LeaveAdvice, str, ToolResponse, format_advice(), format_apply(), format_balance(), format_employees(), format_error() (+3 more)

### Community 57 - "Community 57"
Cohesion: 0.25
Nodes (6): CallToolRequestParams, GetPromptRequestParams, MiddlewareContext, PromptResult, TextContent, ToolResult

### Community 61 - "Community 61"
Cohesion: 0.40
Nodes (5): list_employees(), List all office employees with leave balances., List all office employees with leave balances., List all office employees with leave balances., List all office employees with leave balances.

## Knowledge Gaps
- **149 isolated node(s):** `prepare`, `graphify:sync`, `graphify:sync:unix`, `husky`, `Connection` (+144 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `init_db()` connect `Community 6` to `Community 49`, `Community 2`, `Community 52`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Why does `ToolResponse` connect `Community 2` to `Community 0`, `Community 4`, `Community 48`, `Community 52`, `Community 56`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `run()` connect `Community 52` to `Community 47`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 25 inferred relationships involving `ToolResponse` (e.g. with `list_employees()` and `get_employee()`) actually correct?**
  _`ToolResponse` has 25 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `_json_response_enriched()` (e.g. with `resolve_grok_block()` and `format_enriched_response()`) actually correct?**
  _`_json_response_enriched()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `utc_now_iso()` (e.g. with `_grok_from_parsed()` and `generate_fallback_output_recommendations()`) actually correct?**
  _`utc_now_iso()` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `generate_output_recommendations()` (e.g. with `resolve_grok_block()` and `_json_response_enriched()`) actually correct?**
  _`generate_output_recommendations()` has 4 INFERRED edges - model-reasoned connections that need verification._