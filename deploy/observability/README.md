# Observability (STUB)

Prometheus + Grafana + Loki. Goal: a junior can answer "what is each Chief doing
and is it healthy?" from one Grafana folder.

- **Metrics (Prometheus):** per-Chief workflow counts, approval-gate latency, model
  tokens/latency, memory compaction runs, error rates. Add `ServiceMonitor`s per
  component at its phase.
- **Logs (Loki):** structured logs labeled by `chief`, `workflow_id`, `ticket_id` so
  a single ticket is traceable end-to-end.
- **Dashboards:** `dashboards/` (JSON) — "COT Overview", "Per-Chief", "Model
  Serving", "Memory". Stubs added in Phase 0.

SLOs and alert rules are defined in the Phase 1 (harden & scale) PRD. No manifests
yet — this is the PRD phase.
