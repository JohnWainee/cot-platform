# ADR-0001 — Coordination model

## Status

Accepted (recommended default; final engine choice is Open Question #2 in the master PRD)

## Context

A central orchestrator is **required** (mission constraint). The decision is the
substrate beneath it, weighed against: junior operability (prime directive), 90–95%
uptime (modest), 3 humans / 12–24 tickets/day, and a long-running, human-gated loop.
Severity of getting this wrong: **High** (it shapes every workflow and every debug
session).

## Options

### A. Central orchestrator + workflow engine (Temporal / Prefect / n8n)

- ➕ Durable workflow state; built-in retries, timers, signals (ideal for human gates).
- ➕ Visual, replayable traces a junior can follow; clean restart recovery.
- ➖ One more platform to run; Temporal is the heaviest of the three to operate.

### B. Choreography over a message/event bus (NATS / Redis Streams)

- ➕ Decoupled, no central SPOF; naturally async.
- ➖ Emergent control flow is **hard for a junior to reason about**; no single trace;
  human-gate semantics must be hand-built. Debugging distributed state is the
  opposite of the prime directive.

### C. Hybrid — central orchestrator for task assignment + a light event bus

- ➕ Durable, traceable workflows where it matters; cheap async notifications where it
  doesn't; Teams/ClickUp as the human window.
- ➖ Two moving parts instead of one (mitigated: the bus is small and optional).

## Decision

**Option C (Hybrid).** Durable orchestrator core = **Temporal** (recommended) with
**Prefect** as the documented lighter fallback; light async notifications = **NATS
JetStream**. Chiefs are LangGraph workers ([ADR-0002](0002-agent-framework.md)).

The orchestrator is a **single point of failure**, accepted because: target uptime is
modest, durable state makes a restart recover in-flight work (matching the
"single-instance-per-Chief is fine where a clean restart recovers state" constraint),
and one orchestrator is far more junior-debuggable than choreography.

## Consequences

- **Positive:** every ticket is one replayable workflow; human gates are first-class
  (durable signals); restart recovery is built in; the bus keeps notifications from
  coupling Chiefs.
- **Negative / mitigations:** Temporal's operational footprint (DB + services) — if it
  proves too heavy for the team, fall back to Prefect without changing the Chief code
  (LangGraph workers are engine-agnostic at the boundary). **High**-severity changes to
  orchestration are human-gated.
- **Follow-up:** owner picks Temporal vs Prefect before Phase 0 build (Open Question #2).
