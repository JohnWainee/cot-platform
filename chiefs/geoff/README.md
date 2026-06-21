# Geoff — CoOrchestration (P0)

Central orchestrator. Runs standups, checks/updates tickets, routes work to the
right Chief, and gates every significant decision through a human. Long-term goal:
absorb the owner's coordination load. **Geoff proposes; humans dispose.**

- **Phase:** P0 · **Model tier:** reasoning · **Egress:** none
- **Reads:** ClickUp tickets, shared semantic memory · **Writes:** card notes, Teams
  messages, task assignments — all production-affecting steps behind a human gate.

## Debugging Geoff

- Every run is a LangGraph workflow with a durable trace in the orchestrator UI
  (Temporal). Start there: find the workflow id from the Teams thread or ticket.
- His decisions are captured to his vault — grep `chiefs/geoff` runtime vault (not
  in git) or use `wks_memory_search`.
- Runbook: [`docs/runbooks/deploy-restart-chief.md`](../../docs/runbooks/deploy-restart-chief.md).

> Stub. Logic is added in Phase 0 — see [`docs/prd/phase-0-mvp.md`](../../docs/prd/phase-0-mvp.md).
