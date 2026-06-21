# clickup — MCP server (STUB)

Tickets/cards. P0 target: **ClickUp** (REST API). OSS fallback: **Plane**, behind the
same adapter interface (ADR-0005).

Tools: `wks_ticket_list`, `wks_ticket_update`, `wks_task_assign`.

**Egress:** `api.clickup.com` — architect-approved egress entry required (ADR-0007).
Token from Vault. No logic yet.
