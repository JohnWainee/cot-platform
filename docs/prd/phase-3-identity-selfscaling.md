# Phase 3 PRD — Identity & self-scaling

- **Status:** Draft (enter after P2 stable + owner approval)
- **Depends on:** [Phase 2](phase-2-provisioning-config.md) stable
- **Theme:** Add **Ida** (CoIdentity) and **Jane** (CoStaff). Jane can spawn new
  Chiefs — **always human-approval-gated.**

## Goal

Automate identity/secrets operations (Ida) and give COT the ability to grow its own
roster safely (Jane), without ever weakening the human-in-loop guarantee.

## Scope

**In:** Ida (Windows AD + Entra + Vault: account lifecycle, credential-expiry
monitoring, DNS/IP reclamation, secret rotation) and Jane (Chief lifecycle: research a
new domain, tag-team with Jules to stand up MCP servers, register in the Hub —
**spawning requires human approval**).

**Out:** any autonomous identity change or Chief spawn; both are gated.

## Components in this phase

| Component | Path | Notes |
|---|---|---|
| Ida | `chiefs/ida/` | identity/secrets ops |
| Jane | `chiefs/jane/` | roster lifecycle |
| ad/entra/vault servers | `mcp-hub/servers/` | gated identity actions |
| chief-factory | `platform/` | Jane's gated spawn pipeline |

## MCP tool contracts (proposed)

| Tool | Server | Kind | Gate |
|---|---|---|---|
| `wks_ad_account_report` | ad | read | none |
| `wks_ad_account_lifecycle` | ad | write | **human** |
| `wks_entra_review` | entra | read | none |
| `wks_secret_rotate` | vault | write | **human** |
| `wks_dns_ip_reclaim` | ad | write | **human** |
| `wks_chief_spawn` | chief-factory | write | **human** (Critical) |

## Acceptance criteria

- [ ] Ida reports expiring credentials and proposes rotations; rotation executes only
      after approval (`wks_secret_rotate` gated).
- [ ] Account lifecycle actions (create/disable) are gated and audited end-to-end.
- [ ] Jane can research a new domain and produce a Chief spec, but `wks_chief_spawn`
      **cannot** create a Chief without a human approval signal (Critical gate).
- [ ] A newly spawned Chief inherits the base image, an isolated vault, default
      `egress: none`, and registry-gated tools.

## Test plan

- **Gating:** prove every identity write and `wks_chief_spawn` blocks without
  approval; timeouts never auto-approve.
- **Spawn dry-run:** Jane proposes a Chief; assert nothing is created until approved,
  then assert the new Chief is fully isolated and egress-denied by default.
- **Rotation safety:** rotate a non-prod secret; assert dependent servers pick up the
  new value from Vault without downtime beyond the documented window.

## Rollback

- Ida/Jane disabled via Helm values; identity ops revert to humans.
- Secret rotations are reversible to the previous version in Vault within the rotation
  window.
- A spawned Chief is removed declaratively (disable + deregister from the Hub +
  archive its vault).

## Operability

- Identity runbooks added this phase: `ad-account-lifecycle.md`,
  `credential-expiry-review.md` under [`docs/runbooks/`](../runbooks/); secret rotation
  reuses [`vault-secret-rotation.md`](../runbooks/vault-secret-rotation.md).
- Chief spawning is a documented, gated pipeline; the approval message contains the
  full Chief spec and the egress it requests (default none).

## Copilot prompt blocks

```copilot-prompt
# Jane: gated chief-factory (Phase 3)
Implement wks_chief_spawn (chief-factory, write, gate: human, severity Critical):
input is a Chief spec (name, role, domain, model_tier, requested tools, egress).
It MUST require a wks_teams_await_approval signal before creating anything. On approve,
scaffold from chiefs/_base, create an isolated vault, set egress: none, and register
ONLY the approved tools in the Hub registry (itself a human-gated commit).
```

```copilot-prompt
# Ida: gated secret rotation (Phase 3)
Implement wks_secret_rotate (vault server, write, gate: human): propose a rotation
plan for expiring secrets (from wks_ad_account_report/wks_entra_review), execute only
on approval, and verify dependent MCP servers reload the new value from Vault. Keep the
previous version recoverable within the rotation window.
```
