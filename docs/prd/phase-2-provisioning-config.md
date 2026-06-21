# Phase 2 PRD — Provisioning & configuration

- **Status:** Draft (enter after P1 stable + owner approval)
- **Depends on:** [Phase 1](phase-1-harden-scale.md) stable
- **Theme:** Add two domain Chiefs — **Terry** (CoInfra) and **Ansel** (CoConfig).
  Both **propose**; humans approve all changes.

## Goal

Extend COT into infrastructure provisioning and configuration management, reusing the
P0 loop and gates. Terry handles IaC/provisioning; Ansel handles config/maintenance.

## Scope

**In:** Terry (Terraform `vmware/vsphere`, Packer golden images, RKE2 node lifecycle,
vCenter 8.0.3.x ops) and Ansel (Ansible `vmware.vmware`, drift detection, patching,
compliance baselines). New MCP servers for these tools, all behind human gates and the
egress matrix.

**Out:** identity/secrets domain (P3); autonomous apply (every apply is gated).

## Components in this phase

| Component | Path | Notes |
|---|---|---|
| Terry | `chiefs/terry/` (added this phase) | IaC/provisioning |
| Ansel | `chiefs/ansel/` (added this phase) | config mgmt |
| terraform / packer / vsphere servers | `mcp-hub/servers/` | gated apply |
| ansible server | `mcp-hub/servers/` | drift/patch/compliance |

## MCP tool contracts (proposed)

| Tool | Server | Kind | Gate |
|---|---|---|---|
| `wks_tf_plan` | terraform | read | none |
| `wks_tf_apply` | terraform | write | **human** |
| `wks_packer_build` | packer | write | **human** |
| `wks_vsphere_inventory` | vsphere | read | none |
| `wks_rke2_node_lifecycle` | vsphere | write | **human** |
| `wks_ansible_check` | ansible | read | none (dry-run/`--check`) |
| `wks_ansible_apply` | ansible | write | **human** |
| `wks_drift_report` | ansible | read | none |

Egress: internal only (vCenter, internal mirrors). Any exception is an
architect-approved egress-matrix row (ADR-0007).

## Acceptance criteria

- [ ] Terry produces a `terraform plan` for a scoped change and posts it for approval;
      `apply` runs **only** after `wks_teams_await_approval` returns approve.
- [ ] Packer builds a golden image from a versioned template; artifact is recorded.
- [ ] Ansel reports drift on a target group and proposes a remediation play; apply is
      gated.
- [ ] Both Chiefs' actions are correlated in Loki by `ticket_id`/`workflow_id`.
- [ ] No standing credentials: vCenter/Ansible creds resolve from Vault per run.

## Test plan

- **Plan/apply gating:** assert `wks_tf_apply` cannot execute without an approval
  signal; dry-run paths are side-effect-free.
- **Drift:** introduce a known drift; assert `wks_drift_report` detects it and the
  proposed play would correct it (in `--check`).
- **Sandbox:** run all P2 tests against a non-prod vCenter/cluster first.
- **Rollback rehearsal:** apply then revert a scoped Terraform change in the sandbox.

## Rollback

- Terry/Ansel are disabled via Helm values; the platform reverts to P1 behavior.
- Terraform state is remote and versioned; revert to the last good state and
  `apply` (gated).
- Ansible changes ship with a documented revert play per role.

## Operability

- IaC operations and state recovery: extend
  [`docs/runbooks/`](../runbooks/) with `terraform-state-ops.md` and
  `ansible-drift-remediation.md` (added this phase).
- All applies are visible as gated Temporal workflows; the plan/diff is in the Teams
  approval message.

## Copilot prompt blocks

```copilot-prompt
# Terry: Terraform server (Phase 2)
Implement a terraform MCP server exposing wks_tf_plan (read) and wks_tf_apply
(write, gate: human). Use remote, versioned state; creds from Vault per run. apply
MUST require a wks_teams_await_approval signal carrying the exact plan that was
approved (hash-match plan→apply). Egress: vCenter + internal mirror only.
```

```copilot-prompt
# Ansel: Ansible drift + remediation (Phase 2)
Implement an ansible MCP server: wks_ansible_check (--check, read), wks_drift_report
(read), wks_ansible_apply (write, gate: human). Every role ships a revert play.
Run against a non-prod inventory in tests. Correlate logs by ticket_id.
```
