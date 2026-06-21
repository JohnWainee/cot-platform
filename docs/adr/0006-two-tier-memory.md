# ADR-0006 — Two-tier memory architecture

## Status

Accepted

## Context

PACE (the reference implementation) is single-machine, per-agent-siloed, and
**intentionally avoids a vector DB** (SQLite FTS5 only). COT needs **shared** semantic
memory across Chiefs (holistic context) plus **vector indexes over the 8 repos**. We
must resolve this tension while honoring the junior-operability directive. Severity:
**High** (foundational; touches every Chief).

## Options

### A. PACE as-is (per-Chief FTS5 only, no sharing, no vectors)

- ➕ Maximally simple, grep-able, proven.
- ➖ No cross-Chief context; no semantic recall over repos — fails Franklin's needs.

### B. Single shared vector store for everything (drop per-Chief siloing)

- ➕ One store; semantic everywhere.
- ➖ Loses PACE's debuggable per-agent vaults; mixes private episodic memory with
  shared knowledge; higher poisoning blast radius.

### C. Two-tier: PACE-style per-Chief vaults + a shared semantic tier

- ➕ Keep PACE's strengths for personal/episodic memory; add exactly the shared
  semantic capability COT needs, no more.
- ➖ Two stores to understand (mitigated: each is simple and has one job).

## Decision

**Option C — two tiers.**

- **Tier 1 (per-Chief):** Markdown + YAML + **SQLite FTS5**, isolated vault, PACE tiers
  (working→long_term→project→followups→archived), **lazy maintenance, no cron**,
  conservative promotion, retention exemptions.
- **Tier 2 (shared):** **Postgres + pgvector** ([ADR-0004](0004-shared-semantic-store.md))
  for the 8-repo indexes + curated org context; **read by all Chiefs**, **writes
  curation/approval-gated**.

## Consequences

- **Positive:** private memory stays grep-able and debuggable; shared semantic recall
  exists where needed; clear blast-radius separation; provenance on every shared write.
- **Negative / mitigations:** two stores — mitigated by exposing both behind one
  `memory` MCP server with a small tool set (`wks_memory_*`, `wks_repo_*`). Shared-tier
  poisoning is mitigated by gated writes + `curated_by` provenance.
- **Adopted from PACE:** local-first MD+FTS5, tiered memory, lazy maintenance, per-agent
  identity, no cron, retention exemptions. **Rejected/extended:** siloed-only → shared
  tier; no-vector-DB → pgvector (Tier 2 only); single-`.plugin` packaging →
  containerized MCP services.
