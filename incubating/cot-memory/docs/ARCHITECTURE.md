# Architecture — cot-memory

This server implements COT's two-tier memory ([ADR-0006](../../../docs/adr/0006-two-tier-memory.md),
[ADR-0004](../../../docs/adr/0004-shared-semantic-store.md)) as a single MCP server
with two backends. It is a fork of `smriti-mcp`; the storage engine, frontmatter
parsing, and full-text search come from upstream and are adapted to the contracts
below.

## Tiers

### Tier 1 — per-Chief vault (P0)

Each Chief gets an **isolated** vault: its own files and its own SQLite FTS5 index.
Human-readable, grep-able, git-ignored runtime state.

```text
<chief>/vault/
├── memories/
│   ├── working/        # today's captures (soft cap 16k / hard 32k chars)
│   ├── long_term/      # promoted stable facts
│   └── archived/       # aged-out, search-only
├── projects/<name>/{summary.md, notes/}
├── followups/          # proactive inbox; <id>.md + done/
└── system/
    ├── index.db        # SQLite FTS5 (rebuildable)
    ├── config.yaml     # budgets, retention, heartbeat opt-in
    └── logs/
```

- **Tiers/promotion:** promote `working → long_term` when an entry is ≥N days old
  **and** referenced, **or** carries a long-term tag, **or** would overflow the
  working budget. Never evict `#user` / `#high-signal` / `#decision`.
- **Lazy maintenance, no cron:** `wks_memory_status` returns `needs_compact` (24h+),
  `needs_review` (7d+), `needs_heartbeat` (opt-in). The Chief runs whatever is
  flagged silently after replying to the first message of a session. Nothing is ever
  deleted; review archives.

### Tier 2 — shared semantic (P1)

Postgres + pgvector holding the 8-repo indexes + curated org context, read by all
Chiefs, **writes curation/approval-gated**. Exposed read-only via `wks_repo_search`,
`wks_repo_read`, and the shared path of `wks_memory_search`. The schema of record is
the monorepo's `platform/memory/shared/schema.sql`. Embedding dimension and HNSW
params are set against the chosen local embedding model at implementation time.

## What maps from upstream `smriti-mcp`

| Upstream | cot-memory use |
|---|---|
| `MemoryStore` (Markdown + YAML I/O) | Tier-1 vault storage engine |
| full-text search | backs `wks_memory_search` |
| `consolidate` / `rebuild` | lazy compaction + `index.db` rebuild |
| `archive` (soft-delete) | the `archived/` tier |
| wikilinks / index | cross-references within a vault |

COT-original additions (not from upstream): PACE tiering + budgets, per-Chief vault
isolation, the `wks_memory_status` flag model, and the Tier-2 pgvector backend.

## Phasing

- **P0:** Tier-1 server only — `wks_memory_capture`, `wks_memory_search`,
  `wks_memory_status`. One server, one backend.
- **P1:** add Tier-2 behind the same server — `wks_repo_search`, `wks_repo_read`, and
  the shared path of `wks_memory_search`. No contract changes for Chiefs.
