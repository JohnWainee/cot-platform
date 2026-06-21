# Runbook — Vault secret rotation

## Purpose

Rotate a credential (Teams/Graph, ClickUp, DB, vCenter, AD) safely, with a recovery
window. All secrets live in HashiCorp Vault — never in config or images.

## When to use

- A credential is expiring (Ida flags this in P3) or is suspected compromised.
- Routine rotation per policy.

## Prerequisites

- Vault access with a policy permitting the target path.
- Know which MCP servers/Chiefs consume the secret (check
  [`mcp-hub/registry/registry.yaml`](../../mcp-hub/registry/registry.yaml)).

## Steps

1. **Stage the new secret** (keep the old version recoverable):

   ```bash
   vault kv put secret/cot/<path> value=<new>      # [finalize at impl]
   vault kv metadata get secret/cot/<path>         # confirm prior version retained
   ```

2. **Roll consumers** so they re-read from Vault:

   ```bash
   kubectl -n cot rollout restart deploy/<consumer>
   ```

3. **Revoke the old credential at the source** (e.g. Azure/Graph app secret, ClickUp
   token) only **after** verifying the new one works.

## Verification

- The consuming server performs a real call successfully (e.g. `wks_teams_post` posts;
  `wks_ticket_list` returns).
- No auth errors in Loki for that server after the roll.

## Rollback (within the recovery window)

```bash
vault kv rollback -version=<previous> secret/cot/<path>   # [finalize at impl]
kubectl -n cot rollout restart deploy/<consumer>
```

Only do this **before** revoking the old credential at the source.

## Escalation

Suspected compromise → treat as a **Critical** incident
([incident-response](incident-response.md)), rotate immediately, and notify the owner.
Production-affecting rotations are human-gated (`wks_secret_rotate`, P3).
