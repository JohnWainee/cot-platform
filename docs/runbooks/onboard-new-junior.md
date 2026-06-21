# Runbook — Onboard a new junior engineer

## Purpose

Get a new engineer productive and on-call-capable within their first week, in keeping
with the prime directive: they must be able to **operate, debug, and extend** COT.

## Day 1 — orient

1. Read, in order: [`README`](../../README.md) → [master PRD](../prd/COT-master-PRD.md)
   → [phase-0 PRD](../prd/phase-0-mvp.md) → [architecture overview](../architecture/overview.md).
2. Internalize **the loop**: ticket → triage → diagnose → propose → **human approves**
   → act. Nothing touches production without a gate.
3. Read [CONTRIBUTING](../../CONTRIBUTING.md): branch/PR flow, conventional commits, and
   the **sandbox boundary** (architect-owned vs engineer-owned).

## Day 2 — access & tools

- Cluster (`kubectl` context, namespace `cot`), Temporal UI, Grafana, Loki, Vault
  (least-privilege policy), GitHub repo, Teams + ClickUp.
- Verify each by reading-only: list pods, open a workflow, open a dashboard, run a
  search query. No writes yet.

## Day 3–4 — guided operations (read the runbook, then do it)

- Restart a Chief in a safe window: [deploy-restart-chief](deploy-restart-chief.md).
- Rebuild a Tier-1 index: [rebuild-memory-index](rebuild-memory-index.md).
- Trace one real ticket end-to-end from the IDs in its Teams thread.

## Day 5 — first contribution

- Pick a `good-first-issue`; branch → PR → CI green → self-review → merge. Likely a
  docs/runbook improvement or a stub fill-in (only within an approved phase).

## Guardrails to memorize

- Never bypass `wks_teams_await_approval`.
- Never add egress without an architect-approved matrix row.
- Never commit secrets/model blobs (`.gitignore` enforces; double-check).
- When unsure, **disable the Chief** (revert to humans) rather than risk a live fix.

## Where to get unstuck

- Operational: [`docs/runbooks/`](README.md) (start at [incident-response](incident-response.md)).
- Architectural "why": the [ADRs](../adr/).
- Anything Critical (egress/secrets/data loss): the owner, immediately.
