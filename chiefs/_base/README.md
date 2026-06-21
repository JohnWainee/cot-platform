# Base Chief image

Shared base every Chief is built `FROM`. **Stub only — no agent logic yet.**

A Chief = **identity** (`IDENTITY.md`) + **system prompt** + **tool contract**
(`tools.md`, resolved against the MCP Hub) + **two-tier memory** (a private vault +
read access to the shared semantic tier) + a **LangGraph** run loop (added at its
phase). The base image bundles: the LangGraph runtime, the memory MCP client, the
Hub client, an OTEL exporter (Prometheus/Loki), and an identity loader.

```text
_base/
├── Dockerfile               # base image: runtime + clients + entrypoint (stub)
├── identity/IDENTITY.md.tmpl # per-Chief identity, filled at build/deploy
└── README.md
```

## Per-Chief directory contract

```text
chiefs/<name>/
├── chief.yaml         # declarative config: model tier, memory budgets, tools, egress
├── system-prompt.md   # the Chief's operating instructions (engineer-owned)
├── tools.md           # the MCP tool contract this Chief is granted (wks_*)
└── README.md          # what this Chief does, its gates, how to debug it
```

Implementation is **phase-gated**. Do not add a run loop until the Chief's phase PRD
is approved.
