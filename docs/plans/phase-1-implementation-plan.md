# Phase 1 — Implementation plan (harden & scale)

> Work breakdown for [`phase-1-harden-scale.md`](../prd/phase-1-harden-scale.md).
> Enter after P0 acceptance. **No new Chiefs.**

## Sequenced work breakdown

| # | Work item | Depends on | Owner | Est. |
|---|---|---|---|---|
| 1.1 | vLLM deployment behind OpenAI-compatible endpoint; route reasoning tier to it | P0 | infra | M |
| 1.2 | Keep Ollama for the light tier; `model_tier` selection wired from chief.yaml | 1.1 | Jules | S |
| 1.3 | Prometheus recording + alerting rules (loop success, gate latency, model avail) | P0 | infra | M |
| 1.4 | Grafana "COT SLO" dashboard; alert annotations link to runbooks | 1.3 | infra | S |
| 1.5 | n8n L1 → Addie (L3) handoff contract + feature flag | P0 | Addie dev | M |
| 1.6 | Scheduled backups + tested restore drill (vaults + pgvector); record RTO/RPO | P0 | infra | M |
| 1.7 | Egress review + tighten; negative test from a Chief pod | P0 | architect | S |
| 1.8 | 24-ticket/day load test; record latency/throughput; restart-under-load test | 1.1–1.6 | all | M |

## Definition of done (gate to P2)

All [Phase 1 acceptance criteria](../prd/phase-1-harden-scale.md#acceptance-criteria)
pass; SLOs are live with working alerts; a restore drill succeeded with recorded
RTO/RPO; egress negative test blocks non-allowlisted traffic.

## Copilot prompt blocks

```copilot-prompt
# Restore drill automation (work item 1.6)
Automate: snapshot pgvector + per-Chief vaults → simulate loss → restore → assert row
counts, FTS5 search parity, and vector recall on a fixed query set. Emit RTO/RPO. Wire
into docs/runbooks/backup-restore-postgres-pgvector.md as the canonical procedure.
```

```copilot-prompt
# Egress negative test (work item 1.7)
Add a CI/cluster job that, from a Chief pod, attempts to reach a non-allowlisted host
and asserts the connection is denied by NetworkPolicy, while an allowlisted host (per
the egress matrix) succeeds. Fail loudly if default-deny is not enforced.
```
