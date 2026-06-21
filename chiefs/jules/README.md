# Jules — CoDevOps (P0, framework)

Builds and maintains the COT framework and the **MCP Hub**. Other Chiefs request
tooling/skills via a Kanban card + Teams tag; Jules fulfills hands-off within
guardrails. Registering a new MCP server into the Hub is **human-gated**.

- **Phase:** P0 (framework) · **Model tier:** reasoning · **Egress:** none
- Owns: [`mcp-hub/`](../../mcp-hub/), the base Chief image, and platform plumbing.

## Debugging Jules

- The Hub registry is declarative: [`mcp-hub/registry/registry.yaml`](../../mcp-hub/registry/registry.yaml).
- Runbook: [`docs/runbooks/mcp-hub-ops.md`](../../docs/runbooks/mcp-hub-ops.md).

> Stub. Logic added in Phase 0 — [`docs/prd/phase-0-mvp.md`](../../docs/prd/phase-0-mvp.md).
