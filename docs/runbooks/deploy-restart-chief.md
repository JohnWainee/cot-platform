# Runbook — Deploy / restart / disable a Chief

## Purpose

Bring a Chief up, restart it cleanly (recovering in-flight work), or disable it.

## When to use

- A Chief is misbehaving and you want a clean restart.
- You need to take a Chief out of the loop (revert that work to humans).
- Rolling out an approved Chief config change.

## Prerequisites

- `kubectl` context on the RKE2 cluster, namespace `cot`.
- Helm access to the umbrella chart ([`deploy/helm/cot`](../../deploy/helm/cot)).
- Read [CONTRIBUTING](../../CONTRIBUTING.md) sandbox boundary if changing config.

## Restart a Chief (recovers durable workflow state)

```bash
kubectl -n cot rollout restart deploy/chief-<name>     # [finalize at impl]
kubectl -n cot rollout status  deploy/chief-<name>
```

In-flight workflows resume from Temporal's durable state — confirm in the Temporal UI
that the Chief's workflow continues (no lost steps).

## Deploy / update a Chief

```bash
# After the chief.yaml / values change is merged via PR:
helm -n cot upgrade cot deploy/helm/cot -f deploy/helm/cot/values.yaml   # [finalize at impl]
```

## Disable a Chief (revert to humans)

Set `chiefs.<name>.enabled=false` in [`values.yaml`](../../deploy/helm/cot/values.yaml)
(PR + approval), then `helm upgrade`. The loop falls back to L2/humans with no data
loss.

## Verification

- `kubectl -n cot get pods -l chief=<name>` → Running/Ready.
- Temporal UI: the Chief's workers are polling; a test ticket routes correctly.
- Loki: new structured logs labeled `chief=<name>` appear.

## Troubleshooting

- **CrashLoopBackOff:** `kubectl -n cot logs deploy/chief-<name> --previous`; common
  causes = Vault secret unavailable ([vault-secret-rotation](vault-secret-rotation.md))
  or model endpoint down ([model-serving-host-ops](model-serving-host-ops.md)).
- **Pod up but idle:** check it registered against the MCP Hub
  ([mcp-hub-ops](mcp-hub-ops.md)) and Temporal task queue name matches.

## Rollback

`helm -n cot rollback cot <previous-revision>` then re-verify. Chief disable is itself
the safest rollback for a misbehaving Chief.

## Escalation

If durable state appears corrupted or a restart loses work, treat as an incident →
[incident-response](incident-response.md) and notify the owner.
