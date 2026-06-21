# Runbook — Incident response

## Purpose

A single starting point when something is wrong: the loop stalls, an alert fires, or
an egress/auth failure appears.

## Severity (declare first)

- **Critical:** data loss, suspected egress/exfiltration, an ungated production action,
  secret compromise. → page the owner now.
- **High:** the loop is down for all tickets; orchestrator unavailable.
- **Medium:** one Chief degraded; recall poor; elevated errors.
- **Low:** cosmetic; single transient failure.

## First moves (in order)

1. **Temporal UI** — find the affected workflow(s); is it failed, stalled, or waiting
   on a human gate? (A "stall" is often just an unanswered `wks_teams_await_approval`.)
2. **Loki** — filter by `workflow_id` / `ticket_id` / `chief`; read the error.
3. **Grafana** — check SLO/model/memory panels for the blast radius.

## Common incidents → action

| Symptom | Likely cause | Action |
|---|---|---|
| Loop "stuck" on a ticket | waiting on approval | nudge the human in Teams; check the gate didn't time out |
| All Chiefs erroring on a call | model host or a shared server down | [model-serving-host-ops](model-serving-host-ops.md) / restart the server |
| Auth errors from teams/clickup | expired secret | [vault-secret-rotation](vault-secret-rotation.md) |
| Tool egress fails | NetworkPolicy vs matrix mismatch | compare the allowlist to §7.1 of the master PRD; fix the policy (architect-gated) |
| Stale/wrong recall | index drift | [rebuild-memory-index](rebuild-memory-index.md) |
| Data corruption/loss | storage failure / bad migration | [backup-restore](backup-restore-postgres-pgvector.md) — **Critical** |

## Containment principles

- Prefer **disabling** the affected Chief (revert to humans) over risky live fixes —
  [deploy-restart-chief](deploy-restart-chief.md).
- Never bypass a human gate to "unstick" a workflow. If a gate is the blocker, get the
  human decision.
- For suspected egress/secret compromise: rotate first, ask questions after.

## After action

Capture a short timeline + root cause; if reusable, curate it into the shared semantic
tier (gated write) and link it from the relevant runbook. Open issues for follow-ups.

## Escalation

Critical → owner immediately. High unresolved in 30 min → owner.
