# Orchestrator (STUB)

Hybrid coordination (ADR-0001): a **durable orchestrator** (Temporal; Prefect as the
lighter fallback) drives task workflows; a **light NATS bus** carries async
notifications. Chiefs are **LangGraph** workers (ADR-0002).

Why durable: the ticket loop is long-running and human-gated. Workflow state is
persisted, so a Chief or the orchestrator can be restarted cleanly and resume —
which is exactly why a single instance per Chief is acceptable at 90–95% uptime.

```mermaid
sequenceDiagram
  participant U as Human (Teams/ClickUp)
  participant G as Geoff (orchestrator workflow)
  participant A as Addie
  participant F as Franklin
  U->>G: ticket created
  G->>A: assign triage
  A-->>G: findings (config error? defect?)
  G->>F: root-cause (if defect)
  F-->>G: fix spec
  G->>U: wks_teams_await_approval (BLOCKS)
  U-->>G: approve / reject / edit
  G->>U: act only on approve; update card
```

The LangGraph node wiring, Temporal worker, and NATS subjects are added in Phase 0.
No logic yet — see [`docs/prd/phase-0-mvp.md`](../../docs/prd/phase-0-mvp.md).
