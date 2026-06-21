# ADR-0004 — Shared semantic store (Tier 2)

## Status

Accepted

## Context

The two-tier memory ([ADR-0006](0006-two-tier-memory.md)) needs a shared semantic
store for the **8-repo vector indexes** and curated cross-Chief context. Selection
weight (from the brief): **the simplest thing a junior can operate**, at a scale of 8
repos and a 3-person team. Severity: **Medium-High** (data layer; migratable but
foundational).

## Options

### A. Postgres + pgvector

- ➕ One database technology; juniors already know SQL; inspect/debug with `psql`.
- ➕ Runs trivially on RKE2; backs up like any Postgres; can also hold relational/
  orchestrator state — **fewer moving parts**.
- ➖ Not the fastest ANN at very large scale (irrelevant at our scale).

### B. Qdrant

- ➕ Purpose-built vector DB; fast ANN; good filtering.
- ➖ Another system to learn/operate; separate backup story; overkill here.

### C. Weaviate

- ➕ Feature-rich (hybrid search, modules).
- ➖ Heaviest of the three operationally; most concepts for a junior to absorb.

## Decision

**Option A — Postgres + pgvector.** Simplest to operate, SQL-debuggable, doubles as
relational state, and more than sufficient for 8 repos. **Qdrant is the documented
escape hatch** if recall/latency at scale ever demands it.

## Consequences

- **Positive:** one backup/restore runbook covers both vectors and relational data;
  juniors debug with familiar tools; minimal new surface area.
- **Negative / mitigations:** if scale grows, migrate the vector tables to Qdrant
  behind the same `wks_repo_search`/`wks_memory_search` contracts — Chiefs are
  unaffected. HNSW index params are tuned against real recall at implementation.
- **Note:** Tier 1 (per-Chief vaults) stays **FTS5-only** — no vectors there, per PACE.
