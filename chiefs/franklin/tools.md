# Franklin — MCP tool contract (STUB)

| Tool | Kind | Gate |
|---|---|---|
| `wks_repo_search` | read | semantic search over 8-repo pgvector indexes |
| `wks_repo_read` | read | read file/blob at a ref |
| `wks_ticket_update` | write | findings/fix-spec on the card |
| `wks_memory_search` | read | private vault + shared tier |
| `wks_memory_capture` | write | private vault |
| `wks_teams_post` | write | — |
| `wks_task_assign` | write | escalate / return |

Egress: **none** (repos are mirrored internally).
