# Franklin — CoDev (P0)

Knows the platform and the 8 repos via the shared pgvector indexes. Receives L3
escalations, root-causes, writes fix specs on the card, and escalates to humans or
returns to support. Helps spec features/integrations. **Specs fixes; humans write
and merge the code.**

- **Phase:** P0 · **Model tier:** reasoning (coder-capable) · **Egress:** none
- Depends on the shared semantic tier (repo indexes) — see
  [`platform/memory/shared/`](../../platform/memory/shared/).

## Debugging Franklin

- His claims cite file/line from the index; verify against `wks_repo_read`.
- If recall looks stale, rebuild indexes:
  [`docs/runbooks/rebuild-memory-index.md`](../../docs/runbooks/rebuild-memory-index.md).

> Stub. Logic added in Phase 0 — [`docs/prd/phase-0-mvp.md`](../../docs/prd/phase-0-mvp.md).
