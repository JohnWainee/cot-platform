# ADR-0002 — Agent framework for local-model Chiefs

## Status

Accepted

## Context

Each Chief is a local-model agent with persistent memory and an MCP tool contract.
Selection weights (from the brief): **memory-centricity, MCP support, debuggability**,
plus fit with our own two-tier memory ([ADR-0006](0006-two-tier-memory.md)) and the
durable orchestrator ([ADR-0001](0001-coordination-model.md)). Severity: **High**.

## Options

### A. LangGraph

- ➕ Explicit state-graph model — a junior can see exactly what node ran and why.
- ➕ MCP-native; checkpointing aligns with durable/restart-recovery.
- ➕ We layer our own memory cleanly (no opinionated memory to fight).
- ➖ More wiring than a high-level role framework.

### B. CrewAI

- ➕ Fast to express role/task crews.
- ➖ Higher abstraction hides control flow; less deterministic; harder to debug a
  misstep — counter to the prime directive.

### C. Letta / MemGPT

- ➕ Memory-centric by design.
- ➖ Its memory model is the framework; we'd fight it to run our two-tier design, and
  its internals are more opaque to a junior.

### D. Thin custom orchestration

- ➕ Maximum control, minimal deps.
- ➖ Maximum maintenance burden for a 3-person team; reinvents checkpointing/tracing.

## Decision

**Option A — LangGraph.** Best balance of debuggability + MCP-native + checkpointing,
and it lets COT own its memory design rather than inherit Letta's.

## Consequences

- **Positive:** inspectable graphs; clean MCP tool binding; checkpoints complement
  Temporal's durability; the framework stays out of the way of two-tier memory.
- **Negative / mitigations:** more explicit wiring per Chief — mitigated by the shared
  base image and per-Chief stubs (`chiefs/_base`), so a new Chief is mostly config.
- Keeps the worker layer engine-agnostic, preserving the Temporal↔Prefect fallback.
