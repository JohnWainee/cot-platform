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

## Implementation lives in `cot-memory`

Per [ADR-0008](../../../docs/adr/0008-memory-server-sourcing.md), the server itself
is **not** built here — it is a fork of `smriti-mcp` in a standalone repo,
`JohnWainee/cot-memory`. This directory stays a thin pointer; the contracts above
remain the source of truth for the tool surface. The P0 scaffold awaiting that repo
is staged at [`incubating/cot-memory/`](../../../incubating/cot-memory/README.md).
