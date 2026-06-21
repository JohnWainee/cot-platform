# ADR-0003 — Local model serving & model-per-Chief matrix

## Status

Accepted

## Context

Models must be **fully local / open-weight**; no reasoning leaves the premises. We
need fast/cheap inference for triage and stronger reasoning for Geoff/Franklin/Jules,
on a single GPU host tier sized later ([hardware rec](../hardware-recommendation.md)).
Weights: junior operability vs throughput. Severity: **High** (cost + latency).

## Options

### A. Ollama everywhere

- ➕ Single binary, trivial model add/swap, great dev ergonomics — junior-operable.
- ➖ Lower throughput/concurrency than vLLM for the heavy models.

### B. vLLM everywhere

- ➕ High throughput, batching, OpenAI-compatible API — best for reasoning load.
- ➖ Heavier to operate; overkill for tiny triage models; steeper for a junior.

### C. Mixed tiers (Ollama + vLLM)

- ➕ Right tool per job: Ollama for the light/triage tier and dev, vLLM for reasoning.
- ➖ Two serving stacks to run.

## Decision

**Option C, phased: Ollama-first for P0, add vLLM for the reasoning tier at P1+.**
P0 favors the simplest thing that works (Ollama); P1 introduces vLLM for
Geoff/Franklin/Jules once the loop is real and load is measured.

**Model-per-Chief matrix (recommendation; validate on the chosen host):**

| Chief | Tier | Suggested open-weight class |
|---|---|---|
| Addie | light | 7–8B instruct |
| Geoff | reasoning | 30–70B instruct |
| Franklin | reasoning (coder) | strong code model (~32B) |
| Jules | reasoning | ~30B instruct |
| Embeddings | — | local embedding model (768-dim class) |

## Consequences

- **Positive:** cheapest viable start; clear upgrade path; latency where it matters.
- **Negative / mitigations:** running two stacks at P1 — mitigated by serving both
  behind the same OpenAI-compatible interface so Chief config only references a
  `model_tier`. Exact model IDs are pinned at build against an internal mirror
  (air-gapped).
