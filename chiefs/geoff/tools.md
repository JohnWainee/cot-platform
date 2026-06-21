# Geoff — MCP tool contract (STUB)

Granted tools (resolved against the MCP Hub; `wks_` + snake_case). Full schemas live
in `mcp-hub/contracts/`.

| Tool | Kind | Gate |
|---|---|---|
| `wks_ticket_list` | read | — |
| `wks_ticket_update` | write | card notes only; status changes need a human gate |
| `wks_teams_post` | write | — |
| `wks_teams_await_approval` | write/block | **the** human gate primitive |
| `wks_task_assign` | write | routes work to a Chief |
| `wks_memory_capture` | write | private vault |
| `wks_memory_search` | read | private vault + shared semantic tier |

Egress: **none**. Geoff never reaches the internet.
