# Jules — MCP tool contract (STUB)

| Tool | Kind | Gate |
|---|---|---|
| `wks_hub_list` | read | list registered servers/tools |
| `wks_hub_scaffold` | write | scaffold from template (no register) |
| `wks_repo_read` | read | — |
| `wks_ticket_update` | write | — |
| `wks_memory_search` | read | private vault + shared tier |
| `wks_memory_capture` | write | private vault |
| `wks_teams_post` | write | — |

Registering a new MCP server into the Hub is **human-gated** (not a tool Jules can
self-execute). Egress: **none**.
