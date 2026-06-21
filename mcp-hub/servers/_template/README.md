# _template — new MCP server scaffold (STUB)

Copy this directory to create a new server (`wks_hub_scaffold`). Checklist for Jules:

1. Rename to the server's domain (e.g. `vault`, `terraform`).
2. Write one contract per tool in `mcp-hub/contracts/` (`wks_<area>_<verb>`).
3. Default `egress: none`. If the server needs egress, get architect sign-off and
   add it to the egress matrix first.
4. Implement the server (phase-gated — only after the relevant phase PRD).
5. **Human-gated:** append the server + tools to `registry/registry.yaml`.
6. Grant tools to specific Chiefs in their `chief.yaml`.

Keep it the simplest server that works. A junior should understand it in one read.
