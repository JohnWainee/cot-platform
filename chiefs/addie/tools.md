# Addie — MCP tool contract (STUB)

| Tool | Kind | Gate |
|---|---|---|
| `wks_ticket_list` | read | — |
| `wks_ticket_update` | write | findings/notes; reassignment needs a gate |
| `wks_diag_run` | read | **read-only** diagnostics only — no remediation |
| `wks_memory_search` | read | private vault + shared tier |
| `wks_memory_capture` | write | private vault |
| `wks_teams_post` | write | — |
| `wks_task_assign` | write | escalate to Franklin / human |

Egress: **none**.
