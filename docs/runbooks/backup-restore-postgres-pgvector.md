# Runbook — Backup & restore (Postgres + pgvector, per-Chief vaults)

## Purpose

Protect and recover COT's stateful data: the shared semantic store (Postgres +
pgvector) and the per-Chief vaults (Markdown + SQLite on a PVC).

## When to use

- Scheduled backups (set up in P0/P1).
- Restore after data loss, corruption, or a bad migration.
- The P1 restore **drill** (record RTO/RPO).

## What to back up

| Data | Where | Method |
|---|---|---|
| Shared store (relational + vectors) | Postgres `cot` | logical `pg_dump` + PVC snapshot |
| Per-Chief vaults | PVC `chief-<name>-vault` | volume snapshot (FTS5 index rebuildable) |
| Orchestrator state | Temporal's datastore | per Temporal's backup guidance |

## Backup

```bash
# Postgres logical dump (includes pgvector data):
kubectl -n cot exec deploy/postgres -- pg_dump -Fc cot > cot-$(stamp).dump   # [finalize at impl]
# PVC/volume snapshots via the RKE2 storage class CSI snapshotter.
```

> Pass a real timestamp in (`stamp`) — do not rely on ad-hoc clocks in scripts.

## Restore

1. Scale down consumers (Chiefs, memory server) to quiesce writes.
2. Restore Postgres:

   ```bash
   kubectl -n cot exec -i deploy/postgres -- pg_restore -d cot --clean < cot-<stamp>.dump
   ```

3. Restore vault PVCs from snapshot (or rebuild FTS5 after restoring Markdown —
   [rebuild-memory-index](rebuild-memory-index.md)).
4. Scale consumers back up; verify.

## Verification

- Row counts and `repo_chunk` per-repo counts match the snapshot.
- `wks_repo_search` returns expected hits on a fixed query set (recall parity).
- A Chief reads/writes its vault normally.
- **Drill metric:** record RTO (time to restore) and RPO (data-loss window).

## Rollback

If a restore is wrong, re-restore from a known-good earlier snapshot. Keep ≥N
generations of backups (set retention in the backup job).

## Escalation

Any unrecoverable loss → **Critical** incident
([incident-response](incident-response.md)) + owner immediately.
