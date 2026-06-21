# Chief of Teams (COT) — Master PRD

- **Status:** Draft for owner review (PRD phase — no implementation started)
- **Owner:** Project owner (lead architect)
- **Last updated:** 2026-06-20
- **Prime directive:** A **junior engineer must be able to operate, debug, and
  extend** this system. Operational simplicity beats cleverness everywhere a
  simpler design costs only performance/scale we do not need.

---

## 1. Vision

COT is an on-premises, **fully local-model** multi-agent platform that automates a
3-person platform/systems-engineering team's daily operations: ticket triage,
troubleshooting, maintenance, and infrastructure provisioning. It is a framework of
named, domain-specialized agents ("**Chiefs**"), each with a persistent identity,
persistent memory, and a small MCP tool contract, coordinated by a central
orchestrator. **Humans stay in the loop for every significant decision and any code
change.** No agent reasoning ever leaves the premises.

The MVP is not a demo: it delivers a real **ticket → triage → diagnose → propose →
human-approve** loop end-to-end.

## 2. Scope & non-goals

**In scope (this build):** internal platform/systems administration for the team's
own environment; the four P0 Chiefs and the framework around them; two-tier memory;
the human window (Teams + ClickUp); Vault; observability; RKE2 deployment.

**Non-goals:**

- ❌ Customer-facing marketing/design/web-traffic agents (explicitly dropped).
- ❌ High availability beyond 90–95%. Single-instance-per-Chief is acceptable where
  a clean restart recovers state. No multi-region, no active/active.
- ❌ Autonomous production changes. Nothing acts on production without a human gate.
- ❌ Cloud/hosted models or telemetry leaving the premises.
- ❌ Premature scale engineering (sharded vector DBs, multi-cluster) for a 3-user,
  12–24 ticket/day load.

## 3. The Chief roster

Right-sized for MVP. Incident-response and observability duties are **folded into
Geoff/Addie** for MVP rather than spawning dedicated Chiefs; Jane adds specialists
later if load justifies it.

| Chief | Role | Domain | Phase |
|---|---|---|---|
| **Geoff** | CoOrchestration | Task assignment, scheduling, standups, human-in-loop gating | **P0** |
| **Addie** | CoSupport | L3 triage, read-only diagnostics, escalation | **P0** |
| **Franklin** | CoDev | Code knowledge over the 8 repos, root-cause, fix specs | **P0** |
| **Jules** | CoDevOps | COT framework + MCP Hub; fulfills tooling requests | **P0** |
| **Terry** *(proposed name; CoInfra)* | Provisioning | Terraform/vSphere, Packer, RKE2 node lifecycle, vCenter 8.0.3.x | P2 |
| **Ansel** *(proposed name; CoConfig)* | Config mgmt | Ansible, drift detection, patching, compliance baselines | P2 |
| **Ida** *(proposed name; CoIdentity)* | Identity/secrets | Windows AD + Entra + Vault, account lifecycle, secret rotation, DNS/IP reclamation | P3 |
| **Jane** | CoStaff | Chief lifecycle; **spawns new Chiefs (human-approval-gated)** | P3 |

> **Open question for owner:** confirm the three proposed names (Terry/Ansel/Ida).

## 4. Memory architecture (two-tier)

COT resolves the central design tension from the PACE reference: PACE is
single-machine, per-agent-siloed, and intentionally avoids a vector DB; COT needs
**shared** semantic memory across Chiefs plus vector indexes over our repos.

### Tier 1 — per-Chief episodic/personal (PACE-style)

Markdown + YAML frontmatter + **SQLite FTS5**, one isolated vault per Chief. Tiers:
`working → long_term → project → followups → archived`. **Lazy in-session
maintenance** (compact/review/heartbeat flags via a status tool — **no cron**).
Wikilinks/tags; conservative promotion; retention exemptions for
`#user`/`#decision`/`#high-signal`. Human-readable, grep-able, git-ignored runtime
state. Layout: [`platform/memory/per-chief/`](../../platform/memory/per-chief/README.md).

### Tier 2 — shared semantic (the part PACE omits)

**Postgres + pgvector** holding: (a) the **8-repo vector indexes** Franklin relies
on; (b) curated cross-Chief org context (decisions, runbook distillations, glossary).
**All Chiefs read** via `wks_memory_search` / `wks_repo_search`. **Writes are
curation/approval-gated** to prevent memory poisoning. Schema:
[`platform/memory/shared/schema.sql`](../../platform/memory/shared/schema.sql).
Rationale in [ADR-0006](../adr/0006-two-tier-memory.md).

### PACE — patterns adopted / patterns rejected

**Adopted:** local-first human-readable storage (Markdown + SQLite FTS5);
tiered memory by access pattern + decay; lazy, in-session self-maintenance with
no external scheduler; per-agent identity + isolated vault; conservative promotion
and retention exemptions; wikilinks + tags; "nothing is ever deleted — review
archives".

**Rejected / extended:** single-machine, per-agent-siloed-only → COT **adds a shared
tier** all Chiefs read; the deliberate no-vector-DB stance → COT **adds pgvector**
for shared semantic recall and the repo indexes (Tier 1 stays FTS5-only); single
`uvx`/single-`.plugin` packaging → COT packages MCP servers as **containerized
services** registered in the MCP Hub and deployed on RKE2.

## 5. Coordination & orchestration

**Decision: Hybrid (ADR-0001).** A durable orchestrator core drives task workflows;
a light NATS event bus carries async notifications. The orchestrator is the required
central coordinator; the bus keeps notifications decoupled.

- **Engine:** **Temporal** (recommended) for durable execution — workflow state is
  persisted, so a Chief or the orchestrator restarts cleanly and resumes. Its Web UI
  gives a junior a visual, replayable trace of every workflow. **Prefect** is the
  documented lighter-weight fallback if Temporal's operational footprint proves too
  heavy.
- **Workers:** Chiefs are **LangGraph** agents (ADR-0002) — explicit, inspectable
  state graphs, MCP-native, checkpointed.
- **SPOF:** the orchestrator is a single point of failure. **Acceptable here**
  because (a) target uptime is 90–95%, (b) durable state means a clean restart
  recovers in-flight work, and (c) a junior debugging one orchestrator is far
  simpler than reasoning about distributed choreography.

See coordination sequence diagram in [`platform/orchestrator/README.md`](../../platform/orchestrator/README.md).

## 6. Local model serving

**Decision (ADR-0003): Ollama-first for P0, vLLM for the reasoning tier at P1+
(mixed).** Ollama is single-binary and junior-operable for MVP; vLLM adds
throughput/batching for the heavy reasoning Chiefs when load justifies it.

**Model-per-Chief matrix (recommendation; validate against the host you buy):**

| Chief | Tier | Suggested open-weight class | Why |
|---|---|---|---|
| Addie | light | 7–8B instruct (e.g. Llama-3.x-8B / Qwen2.5-7B) | fast triage/routing |
| Geoff | reasoning | 30–70B instruct (e.g. Qwen2.5-32B / Llama-3.3-70B) | coordination, summarization, gating judgment |
| Franklin | reasoning (coder) | strong code model (e.g. Qwen2.5-Coder-32B) | root-cause over 8 repos |
| Jules | reasoning | 30B-class instruct | framework/codegen for MCP servers |
| Embeddings | — | local embedding model (e.g. nomic-embed-text / bge-large) | Tier-2 vectors |

## 7. Security

### 7.1 Egress matrix (air-gapped by default)

Outbound internet is **denied by default** (cluster-wide default-deny NetworkPolicy).
Egress is granted only to specific Chiefs/servers that demonstrably need it, each
with a documented justification. Changes here are **Critical** and human-gated
(ADR-0007).

| Component | Egress | Justification | Tier |
|---|---|---|---|
| Geoff, Addie, Franklin, Jules (reasoning) | **none** | all reasoning is local; repos mirrored internally | — |
| `teams` MCP server | `graph.microsoft.com` | the human window (Teams) | High |
| `clickup` MCP server | `api.clickup.com` | tickets/cards | High |
| Model serving, memory, orchestrator, Vault, obs | **none** | fully internal | — |
| (P2+) Terry/Ansel/Ida tool servers | per-tool, documented | vCenter/AD/Entra/Vault are internal; any internet access justified per row | Critical |

> Using the OSS fallbacks (Mattermost + Plane, self-hosted) reduces external egress
> to **near-zero** — a strong option for a hard air-gap. See ADR-0005.

### 7.2 Secrets — HashiCorp Vault

All credentials live in Vault; nothing in config or images. MCP servers fetch
secrets at runtime (Vault Agent / CSI). Secret rotation is a runbook
([`docs/runbooks/vault-secret-rotation.md`](../runbooks/vault-secret-rotation.md)).

### 7.3 Human-in-loop gates

`wks_teams_await_approval` is the single gate primitive: it posts a summarized
proposal and **blocks the workflow** until a human approves/rejects/edits. Gated
actions include: any production change, any code/PR, ticket status changes, escalation
routing, registering a new MCP server, and (P3) **spawning a new Chief**. Timeouts
re-route per escalation policy and **never auto-approve**.

### 7.4 Sandbox allowlist & escalation boundaries

Architect-owned files (PRDs, ADRs, egress policies, Vault policy, CODEOWNERS) change
only via human sign-off. Engineer-owned files (Chief prompts, MCP servers within
contract, scripts, runbooks) change within guardrails. This same boundary bounds what
a future gated agent may modify unattended. Full table: [`CONTRIBUTING.md`](../../CONTRIBUTING.md).

## 8. Observability

Prometheus + Grafana + Loki. A junior answers "what is each Chief doing and is it
healthy?" from one Grafana folder. Logs are labeled by `chief`, `workflow_id`, and
`ticket_id` so a single ticket is traceable end-to-end. Key signals: workflow
counts/outcomes, approval-gate latency, model latency/tokens, memory compaction runs,
error rates. SLOs/alerts are defined in the Phase 1 PRD. See
[`deploy/observability/`](../../deploy/observability/README.md).

## 9. Phased roadmap

Gated; nothing in a later phase is a hard dependency of MVP.

| Phase | Theme | Adds | Gate to enter |
|---|---|---|---|
| **P0** | MVP loop | Geoff, Addie, Franklin, Jules; two-tier memory; MCP Hub; Teams+ClickUp; Vault; Ollama; baseline obs | this PRD approved |
| **P1** | Harden & scale | vLLM reasoning tier; SLOs + alerting; n8n L1→L3 integration; backup/restore drills; egress hardening | P0 acceptance met |
| **P2** | Provisioning & config | Terry (IaC) + Ansel (config mgmt) | P1 stable + owner approval |
| **P3** | Identity & self-scaling | Ida (identity/secrets ops) + Jane (gated Chief spawning) | P2 stable + owner approval |

## 10. Risks

| Risk | Sev | Mitigation |
|---|---|---|
| Orchestrator SPOF causes a stall | High | Durable workflow state; documented restart runbook; modest uptime target |
| Local models too weak for Franklin's RCA | High | Reasoning/coder tier on a sized GPU host; human reviews every fix spec anyway |
| Shared-memory poisoning degrades all Chiefs | High | Tier-2 writes are curation/approval-gated; provenance (`curated_by`) on every row |
| Egress misconfig leaks internal data | Critical | Default-deny + explicit allowlist; egress changes human-gated; OSS fallback removes most egress |
| Over-engineering vs the team's real scale | Medium | YAGNI ladder; junior-operability gate on every component; pgvector/Ollama defaults |
| Junior can't debug a failure | Medium | Every recurring op has a runbook; visual workflow traces; structured, correlated logs |

## 11. Success metrics

- **Loop works:** ≥80% of eligible tickets get an Addie/Franklin triage+finding
  attached before a human looks, within MVP.
- **Human-in-loop integrity:** 100% of production-affecting actions pass through an
  approval gate (audited). Zero ungated production changes.
- **Operability:** a new junior can deploy, restart, and debug a Chief using only the
  runbooks within their first week.
- **Recovery:** orchestrator/Chief restart recovers in-flight workflows with no data
  loss (drill in P1).
- **Toil reduction:** measurable drop in owner coordination time (baseline at P0,
  re-measure at P1).

## 12. Open questions for the owner

1. Confirm proposed Chief names: **Terry** (CoInfra), **Ansel** (CoConfig), **Ida**
   (CoIdentity).
2. Orchestrator: **Temporal** (recommended) vs **Prefect** (lighter). Final call?
3. The **8 repos** to vector-index — names/locations (Franklin's PRD parameterizes
   them).
4. Hard air-gap posture: stay on Teams/ClickUp (needs egress) or adopt the
   **Mattermost + Plane** OSS fallbacks from day one for near-zero egress?
5. Hardware budget ceiling (drives the model tier you can run) — see
   [`docs/hardware-recommendation.md`](../hardware-recommendation.md).

## 13. References

- Per-phase PRDs: [P0](phase-0-mvp.md) · [P1](phase-1-harden-scale.md) ·
  [P2](phase-2-provisioning-config.md) · [P3](phase-3-identity-selfscaling.md)
- ADRs: [0001](../adr/0001-coordination-model.md) · [0002](../adr/0002-agent-framework.md)
  · [0003](../adr/0003-model-serving.md) · [0004](../adr/0004-shared-semantic-store.md)
  · [0005](../adr/0005-human-window-fallback.md) · [0006](../adr/0006-two-tier-memory.md)
  · [0007](../adr/0007-egress-human-in-loop.md)
- Implementation plans: [`docs/plans/`](../plans/) · Runbooks: [`docs/runbooks/`](../runbooks/)
- Reference studied: PACE — Persistent AI Context Engine (`jagbanana/PACE`).
