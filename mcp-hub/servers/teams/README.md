# teams — MCP server (STUB)

The human window. P0 target: **Microsoft Teams** (Graph API). OSS fallback:
**Mattermost**, behind the same adapter interface so Chiefs are unaware which is live
(ADR-0005).

Tools: `wks_teams_post`, `wks_teams_await_approval` (the human-gate primitive).

**Egress:** `graph.microsoft.com` — an architect-approved entry in the egress matrix
is required (ADR-0007). Credentials come from Vault, never from config. No logic yet.
