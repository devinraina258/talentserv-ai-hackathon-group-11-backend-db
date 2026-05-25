---
type: "query"
date: "2026-05-25T11:55:19.045617+00:00"
question: "Is grok giving recommendations for MCP office-leave?"
contributor: "graphify"
source_nodes: ["generate_output_recommendations", "_json_response_enriched", "office-leave", "Grok"]
---

# Q: Is grok giving recommendations for MCP office-leave?

## Answer

Yes. The office-leave FastMCP server (src/server.py) wraps every tool in _json_response_enriched, which adds a grok block via generate_output_recommendations when GROK_ENRICH_OUTPUTS=1. Tools: list_employees, get_employee, get_leave_balance, apply_leave, check_leave_status, list_leave_requests. advise_on_leave uses generate_leave_advice_with_grok. Resources use _resource_response_enriched. Live x.ai calls require GROK_API_KEY and credits; otherwise source=fallback-rules and used_grok=false.

## Source Nodes

- generate_output_recommendations
- _json_response_enriched
- office-leave
- Grok