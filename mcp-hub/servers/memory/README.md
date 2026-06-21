# memory — MCP server (STUB)

Serves the **two-tier memory** (ADR-0006):

- **Tier 1 (per-Chief vault):** Markdown + YAML + **SQLite FTS5**, PACE-style tiers
  (working → long_term → project → followups → archived), lazy in-session
  maintenance via `wks_memory_status` flags (compact/review/heartbeat), **no cron**.
- **Tier 2 (shared semantic):** **Postgres + pgvector** holding the 8-repo indexes +
  curated org context; exposed read-only via `wks_repo_search` / `wks_memory_search`.

Tools: `wks_memory_capture`, `wks_memory_search`, `wks_memory_status`,
`wks_repo_search`, `wks_repo_read`. Schemas in [`../../contracts/`](../../contracts/).

Layout & schema: [`platform/memory/`](../../../platform/memory/). No logic yet.
