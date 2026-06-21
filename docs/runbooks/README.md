# Runbooks

Operational procedures for COT. Each is written so a **junior on call** can execute it
without prior context: purpose, prerequisites, exact steps, verification,
troubleshooting, rollback, escalation.

> **PRD-phase note:** commands referencing not-yet-built components are marked
> `[finalize at impl]`. The structure and decision points are correct now; exact flags
> are pinned when the component ships.

| Runbook | Use when |
|---|---|
| [deploy-restart-chief](deploy-restart-chief.md) | Deploy, restart, or disable a Chief |
| [model-serving-host-ops](model-serving-host-ops.md) | Model host is slow/down; add/swap a model |
| [vault-secret-rotation](vault-secret-rotation.md) | A credential is expiring or compromised |
| [rebuild-memory-index](rebuild-memory-index.md) | Recall is stale/wrong; FTS5 or pgvector index rebuild |
| [backup-restore-postgres-pgvector](backup-restore-postgres-pgvector.md) | Back up or restore memory/state |
| [mcp-hub-ops](mcp-hub-ops.md) | Register/disable an MCP tool; Hub troubleshooting |
| [incident-response](incident-response.md) | The loop stalls, an alert fires, or egress/auth fails |
| [onboard-new-junior](onboard-new-junior.md) | A new engineer joins |

**First move for almost any incident:** Temporal UI (find the workflow) → Loki by
`ticket_id`/`workflow_id` → the Chief's card notes/vault.
