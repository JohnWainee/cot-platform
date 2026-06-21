# Phase 1 PRD — Harden & scale

- **Status:** Draft (enter after P0 acceptance met)
- **Depends on:** [Phase 0](phase-0-mvp.md) accepted
- **Theme:** Make the P0 loop production-grade. **No new Chiefs.**

## Goal

Raise reliability, performance, and operability of the existing four Chiefs:
introduce the vLLM reasoning tier, define SLOs + alerting, integrate the n8n L1→L3
escalation path, prove backup/restore, and harden egress.

## Scope

**In:** vLLM serving for reasoning Chiefs (Geoff/Franklin/Jules) with Ollama retained
for the light tier; Prometheus alert rules + Grafana SLO dashboards; n8n L1 flow
handing off to Addie (L3); scheduled backup + tested restore drills; egress policy
review/tightening; load test at 24 tickets/day.

**Out:** any new Chief; provisioning/config/identity domains (P2/P3).

## Components in this phase

| Component | Path | Change |
|---|---|---|
| model serving | `deploy/helm/cot` (values) | add vLLM reasoning tier (ADR-0003) |
| observability | [`deploy/observability/`](../../deploy/observability/README.md) | SLOs, alert rules, dashboards |
| backup/restore | runbook | scheduled + drilled |
| egress | [`deploy/k8s/network-policies/`](../../deploy/k8s/network-policies/README.md) | review + tighten |
| n8n integration | teams/clickup servers | L1→L3 handoff contract |

## MCP tool contracts

No new tools required by default. If the n8n handoff needs a dedicated intake tool,
add `wks_intake_escalation` (read+write, gate: none) via the standard Hub flow.

## Acceptance criteria

- [ ] Reasoning Chiefs served by vLLM; p95 reasoning latency improves vs the Ollama
      baseline under a 24-ticket/day load test (numbers recorded).
- [ ] SLOs defined (loop success rate, gate latency, model availability) with
      Prometheus alerts firing to Teams on breach.
- [ ] n8n L1 flow hands a qualifying escalation to Addie with full context; the loop
      proceeds unchanged.
- [ ] A restore drill recovers vaults + pgvector to a known snapshot with verified
      integrity; RTO/RPO recorded.
- [ ] Egress review confirms only matrix-approved endpoints are reachable
      (default-deny verified by a negative test).

## Test plan

- **Load:** replay 24 synthetic tickets/day for 3 days; capture latency/throughput/
  error budgets; confirm no workflow loss on a forced orchestrator restart under load.
- **Alerting:** induce each SLO breach (kill model serving, stall a gate) and confirm
  the alert reaches Teams.
- **Backup/restore:** snapshot → corrupt/drop → restore → assert data + search parity.
- **Egress negative test:** from a Chief pod, attempt a non-allowlisted endpoint;
  assert it is blocked.

## Rollback

- vLLM is additive: revert serving to Ollama-only via Helm values; Chiefs keep
  running on the light tier.
- Alert rules and dashboards are versioned; revert the commit.
- n8n handoff is gated behind a feature flag in the intake path; disable to revert to
  human L2 intake.

## Operability

- New dashboards land in the Grafana "COT" folder; each SLO links to its runbook.
- Backup/restore: [`docs/runbooks/backup-restore-postgres-pgvector.md`](../runbooks/backup-restore-postgres-pgvector.md).
- Model host operations: [`docs/runbooks/model-serving-host-ops.md`](../runbooks/model-serving-host-ops.md).
- Incident path unchanged: [`docs/runbooks/incident-response.md`](../runbooks/incident-response.md).

## Copilot prompt blocks

```copilot-prompt
# vLLM reasoning tier (Phase 1)
Add a vLLM deployment serving the reasoning models (Geoff/Franklin/Jules) behind an
OpenAI-compatible endpoint; keep Ollama for the light tier (Addie). Wire model
selection from each chief.yaml model_tier. Add a Grafana panel for tokens/sec and p95
latency per model. No public egress; pull weights from the internal mirror.
```

```copilot-prompt
# SLOs + alerting (Phase 1)
Define Prometheus recording+alerting rules for: loop success rate, approval-gate
latency p95, and model availability. Route alerts to Teams via wks_teams_post. Build a
"COT SLO" Grafana dashboard. Each alert annotation links to the matching runbook.
```
