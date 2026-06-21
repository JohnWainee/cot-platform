# Phase 0 PRD — MVP: the real ticket loop

- **Status:** Draft for owner approval (gate to start building)
- **Depends on:** [Master PRD](COT-master-PRD.md) approved
- **Theme:** Stand up the four P0 Chiefs and the framework so a real
  **ticket → triage → diagnose → propose → human-approve** loop runs end-to-end.

## Goal

A ticket in ClickUp is picked up by **Geoff**, triaged by **Addie** (read-only
diagnostics), root-caused by **Franklin** against the 8-repo indexes when it's a
defect, and every production-affecting step is **approved by a human in Teams**.
**Jules** delivers the MCP Hub and the memory servers that make this possible.

## Scope

**In:**

- Platform: MCP Hub (registry + memory/teams/clickup servers), two-tier memory
  (per-Chief FTS5 vaults + pgvector shared tier with the 8-repo indexes), Temporal
  orchestrator + NATS, Ollama model serving, Vault wiring, baseline Prom/Graf/Loki.
- Chiefs: Geoff, Addie, Franklin, Jules (identities, prompts, LangGraph loops, tool
  grants).
- The human-gate primitive `wks_teams_await_approval` end-to-end.

**Out:** provisioning/config/identity Chiefs (P2/P3); vLLM; SLO/alerting depth (P1);
autonomous remediation (never).

## Components in this phase

| Component | Path | Notes |
|---|---|---|
| MCP Hub | [`mcp-hub/`](../../mcp-hub/) | registry-driven; `wks_` naming |
| memory server | [`mcp-hub/servers/memory/`](../../mcp-hub/servers/memory/README.md) | Tier 1 FTS5 + Tier 2 pgvector |
| teams / clickup servers | [`mcp-hub/servers/`](../../mcp-hub/servers/) | human window + tickets |
| orchestrator | [`platform/orchestrator/`](../../platform/orchestrator/README.md) | Temporal + LangGraph workers |
| Chiefs | [`chiefs/`](../../chiefs/) | geoff, addie, franklin, jules |

## MCP tool contracts (P0 surface)

All `wks_` + snake_case; full schemas in [`mcp-hub/contracts/`](../../mcp-hub/contracts/).

| Tool | Server | Kind | Gate |
|---|---|---|---|
| `wks_memory_capture` / `wks_memory_search` / `wks_memory_status` | memory | write/read/read | none |
| `wks_repo_search` / `wks_repo_read` | memory | read | none |
| `wks_ticket_list` / `wks_ticket_update` / `wks_task_assign` | clickup | read/write/write | none (status change gated per Chief) |
| `wks_teams_post` | teams | write | none |
| `wks_teams_await_approval` | teams | write-block | **human** |
| `wks_diag_run` | (Addie) | read | read-only diagnostics |

## Acceptance criteria

- [ ] A ClickUp ticket triggers a Temporal workflow visible in the Temporal UI with a
      stable `workflow_id`.
- [ ] Addie attaches a triage finding (config-error vs defect) to the card using only
      **read-only** diagnostics.
- [ ] For a defect, Franklin attaches a root-cause + fix spec citing a specific
      file/line from a repo index (`wks_repo_search`/`wks_repo_read`).
- [ ] Every production-affecting step blocks on `wks_teams_await_approval`; no action
      occurs without `decision=approve`. Verified by audit log.
- [ ] Each Chief reads/writes its **own** vault; cross-Chief reads go through the
      shared tier only.
- [ ] `wks_memory_status` returns compact/review flags and lazy maintenance runs
      in-session (no cron present anywhere).
- [ ] Logs for one ticket are retrievable in Loki by `ticket_id` across all Chiefs.
- [ ] All secrets resolve from Vault; none present in images/config (grep clean).

## Test plan

- **Unit/contract:** each MCP tool validated against its contract schema (inputs,
  outputs, error modes); read-only tools proven side-effect-free.
- **Memory:** seed a vault, exceed the working soft cap, confirm lazy compaction
  promotes oldest non-exempt entries and exempt tags survive; rebuild the FTS5 index
  and confirm search parity.
- **Repo index:** index a known repo, assert `wks_repo_search` returns the expected
  file/line for a planted symbol.
- **Gate:** simulate approve / reject / edit / timeout; assert prod action happens
  only on approve and timeout never auto-approves.
- **End-to-end:** scripted ticket (one config-error, one defect) drives the full loop;
  assert card notes, fix spec, gate, and correlated logs.
- **Restart recovery:** kill the orchestrator mid-workflow; assert it resumes from
  durable state.

## Rollback

- Chiefs are disabled declaratively (`chiefs.<name>.enabled=false` in
  [`deploy/helm/cot/values.yaml`](../../deploy/helm/cot/values.yaml)) — flip off and
  redeploy; the loop reverts to humans (L2) with no data loss.
- Memory vaults and the pgvector store are backed up
  ([`docs/runbooks/backup-restore-postgres-pgvector.md`](../runbooks/backup-restore-postgres-pgvector.md));
  restore to the last good snapshot.
- The MCP Hub registry is declarative and versioned — revert the registry commit to
  drop a misbehaving tool.
- Tear-down order and verification: see the deploy/restart runbook.

## Operability

- **Run/restart a Chief:** [`docs/runbooks/deploy-restart-chief.md`](../runbooks/deploy-restart-chief.md).
- **Where to look first:** Temporal UI (workflow trace) → Loki by `ticket_id` →
  the Chief's card notes/vault.
- **Common failure → runbook:** stale repo recall →
  [`rebuild-memory-index`](../runbooks/rebuild-memory-index.md); auth/egress error →
  [`incident-response`](../runbooks/incident-response.md); secret expired →
  [`vault-secret-rotation`](../runbooks/vault-secret-rotation.md).
- A junior should be able to trace any ticket end-to-end from the IDs in the Teams
  thread.

## Copilot prompt blocks

```copilot-prompt
# MCP Hub: memory server skeleton (Phase 0)
Implement an MCP server named "memory" exposing wks_memory_capture, wks_memory_search,
wks_memory_status, wks_repo_search, wks_repo_read per mcp-hub/contracts/.
Tier 1 = per-Chief Markdown vault + SQLite FTS5 (see platform/memory/per-chief/README.md);
Tier 2 = Postgres + pgvector (see platform/memory/shared/schema.sql).
Single source of truth for every read/write. No cron: wks_memory_status returns
needs_compact/needs_review/needs_heartbeat flags. Pin deps; air-gapped mirror only.
Add contract tests asserting read-only tools have no side effects.
```

```copilot-prompt
# Human-gate primitive (Phase 0)
Implement wks_teams_await_approval (teams server): post a summarized proposal to a
Teams channel via Graph API (creds from Vault), then park the Temporal workflow on a
signal until a human approves/rejects/edits. Return {decision, actor, edited_payload}.
On timeout, re-route per escalation policy — NEVER auto-approve. Mirror the contract
in mcp-hub/contracts/wks_teams_await_approval.md exactly.
```

```copilot-prompt
# Geoff orchestrator workflow (Phase 0)
Implement Geoff as a LangGraph graph driven by a Temporal workflow: on a new ClickUp
ticket, assign triage to Addie; if Addie returns "defect", assign root-cause to
Franklin; gate any production-affecting step through wks_teams_await_approval; update
the card and capture decisions to Geoff's vault. Egress: none. Emit OTEL spans labeled
with workflow_id and ticket_id.
```
