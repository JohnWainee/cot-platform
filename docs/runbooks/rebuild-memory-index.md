# Runbook — Rebuild a memory index

## Purpose

Restore correct recall when a Chief's search is stale or wrong. Covers both tiers:
**Tier 1** per-Chief SQLite FTS5, and **Tier 2** shared pgvector repo indexes.

## When to use

- Franklin cites stale/missing code → rebuild the repo (Tier 2) index.
- A Chief's `wks_memory_search` misses recent captures → rebuild its FTS5 index.

## Tier 1 — per-Chief FTS5 (safe; index is auxiliary)

The vault Markdown is the source of truth; the index is rebuildable.

```bash
# [finalize at impl] e.g. the memory server CLI:
cot-memory reindex --chief <name>
```

Verification: search a phrase you know exists; confirm the hit. No data is mutated —
only `system/index.db` is regenerated.

## Tier 2 — shared pgvector repo index

```bash
# Re-index one repo (idempotent upsert by repo/path/ref):
cot-index --repo <name>           # [finalize at impl]
# Full rebuild (all 8) — heavier; schedule off-peak:
cot-index --all
```

Verification: run a query with a known answer (a planted symbol) via `wks_repo_search`
and confirm the expected file/line. Check `repo_chunk` row counts moved as expected:

```sql
SELECT repo, count(*) FROM repo_chunk GROUP BY repo ORDER BY repo;
```

## Troubleshooting

- **Embeddings dim mismatch:** the embedding model changed → the `vector(N)` column and
  the model must agree; re-embed all rows, don't mix dimensions.
- **Recall still poor after rebuild:** revisit chunking + HNSW params (see
  [ADR-0004](../adr/0004-shared-semantic-store.md)); this is a tuning task, not an
  outage.

## Rollback

Indexes are derived data — a rebuild is itself the recovery. If a rebuild is
interrupted, re-run; upserts are idempotent. For Tier 2 corruption, restore pgvector
from backup ([backup-restore](backup-restore-postgres-pgvector.md)) then re-index.

## Escalation

Persistent recall failure that blocks Franklin → open an issue tagged `mcp-hub` and
notify the owner; it's a quality issue, not a Critical incident, unless paired with
data loss.
