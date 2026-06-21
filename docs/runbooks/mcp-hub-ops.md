# Runbook — MCP Hub operations

## Purpose

Register, disable, or troubleshoot an MCP tool/server. The Hub is the single place
Chiefs discover and call tools; the registry is the source of truth.

## When to use

- Registering a new server/tool (the human-gated step after Jules scaffolds it).
- Disabling a misbehaving tool fast.
- A Chief can't see/call a tool it should have.

## Register a new server/tool (human-gated)

1. Confirm the contract exists in [`mcp-hub/contracts/`](../../mcp-hub/contracts/)
   (`wks_<area>_<verb>`), with `kind`, `gate`, and `egress` set.
2. If it needs **egress**, the egress-matrix row must be architect-approved first
   ([ADR-0007](../adr/0007-egress-human-in-loop.md)) — this is **Critical**.
3. Append the server/tools to
   [`registry/registry.yaml`](../../mcp-hub/registry/registry.yaml) **via PR** (this is
   the human gate; not a self-service tool).
4. Grant the tool to specific Chiefs in their `chief.yaml`.
5. `helm upgrade` / reload the Hub.

## Disable a tool fast

Remove (or comment) the tool/server entry in `registry.yaml` and reload. Revert the
PR for a permanent removal. Chiefs lose access immediately on reload.

## Verification

- `wks_hub_list` shows the expected servers/tools.
- The granted Chief can call the tool; a non-granted Chief cannot (enforced by the
  registry).

## Troubleshooting

- **Chief can't call a tool:** check (a) it's in `registry.yaml`, (b) it's granted in
  the Chief's `chief.yaml`, (c) the server pod is healthy, (d) any required Vault
  secret resolves.
- **Tool with egress fails:** confirm the NetworkPolicy allowlist matches the matrix
  row ([incident-response](incident-response.md) for egress debugging).

## Rollback

`git revert` the registry commit + reload. The registry is declarative and versioned —
the last good commit is always the rollback target.

## Escalation

An ungated write tool discovered in the registry, or unexplained egress, is a
**Critical** security finding → owner immediately.
