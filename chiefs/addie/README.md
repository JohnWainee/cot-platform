# Addie — CoSupport (P0)

L3 internal support. Receives escalations (L1 = n8n, L2 = humans), runs read-only
diagnostics, triages, and either returns to L2 (user/config error) or escalates
with findings. **Diagnoses; never remediates.**

- **Phase:** P0 · **Model tier:** light · **Egress:** none

## Debugging Addie

- Her diagnostic calls are read-only — safe to replay. Trace the workflow in the
  orchestrator UI; her findings are on the ClickUp card and in her vault.
- Runbook: [`docs/runbooks/incident-response.md`](../../docs/runbooks/incident-response.md).

> Stub. Logic added in Phase 0 — [`docs/prd/phase-0-mvp.md`](../../docs/prd/phase-0-mvp.md).
