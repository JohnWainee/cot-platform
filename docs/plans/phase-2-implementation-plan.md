# Phase 2 — Implementation plan (provisioning & config)

> Work breakdown for [`phase-2-provisioning-config.md`](../prd/phase-2-provisioning-config.md).
> Enter after P1 stable + owner approval. Adds **Terry** + **Ansel**. Every apply is
> human-gated and rehearsed in a non-prod sandbox first.

## Sequenced work breakdown

| # | Work item | Depends on | Owner | Est. |
|---|---|---|---|---|
| 2.1 | Non-prod vCenter/cluster sandbox for all P2 testing | P1 | infra | S |
| 2.2 | `terraform` server: `wks_tf_plan` (read) + `wks_tf_apply` (gated, plan→apply hash-match) | 2.1 | Jules | L |
| 2.3 | `packer` server: `wks_packer_build` (gated) from versioned templates | 2.1 | Jules | M |
| 2.4 | `vsphere` server: `wks_vsphere_inventory` (read) + `wks_rke2_node_lifecycle` (gated) | 2.1 | Jules | L |
| 2.5 | `ansible` server: `wks_ansible_check`/`wks_drift_report` (read) + `wks_ansible_apply` (gated) | 2.1 | Jules | L |
| 2.6 | Terry Chief: plan→propose→gated-apply graph | 2.2–2.4 | Terry dev | L |
| 2.7 | Ansel Chief: drift→propose-remediation→gated-apply graph; revert play per role | 2.5 | Ansel dev | L |
| 2.8 | Runbooks: `terraform-state-ops.md`, `ansible-drift-remediation.md` | 2.6, 2.7 | all | S |
| 2.9 | Egress-matrix rows for vCenter etc. (architect-approved) | 2.1 | architect | S |

## Definition of done (gate to P3)

All [Phase 2 acceptance criteria](../prd/phase-2-provisioning-config.md#acceptance-criteria)
pass in the sandbox; plan→apply hash-match proven; every role has a revert play.

## Copilot prompt blocks

```copilot-prompt
# Plan→apply hash-match (work item 2.2)
In the terraform server, make wks_tf_apply require an approval signal that carries the
SHA of the exact plan produced by wks_tf_plan. Refuse to apply if the current plan SHA
differs (drift between propose and apply). Use remote versioned state; creds from Vault
per run; egress limited to vCenter + internal mirror.
```
