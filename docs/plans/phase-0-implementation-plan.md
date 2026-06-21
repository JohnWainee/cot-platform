# Phase 0 — Implementation plan (MVP loop)

> Granular work breakdown for [`phase-0-mvp.md`](../prd/phase-0-mvp.md). **Do not start
> until the master PRD + this phase are approved.** Each work item maps to a GitHub
> issue and a PR. Sequencing respects dependencies; items on the same line can run in
> parallel.

## Sequenced work breakdown

| # | Work item | Depends on | Owner | Est. |
|---|---|---|---|---|
| 0.1 | RKE2 namespace `cot`, Helm umbrella scaffolding, internal image mirror, Vault reachable | — | infra | S |
| 0.2 | Postgres + pgvector deployed; apply `schema.sql`; backup job | 0.1 | infra | S |
| 0.3 | Temporal (or Prefect) + NATS deployed; Web UI reachable | 0.1 | infra | M |
| 0.4 | Ollama serving; pull light + reasoning models from mirror | 0.1 | infra | S |
| 0.5 | MCP Hub: registry loader + tool-grant enforcement | 0.1 | Jules | M |
| 0.6 | `memory` server: Tier 1 FTS5 vault ops + lazy status flags | 0.2, 0.5 | Jules | L |
| 0.7 | `memory` server: Tier 2 `wks_repo_search`/`wks_repo_read` over pgvector | 0.2, 0.6 | Jules | M |
| 0.8 | Repo indexer: chunk + embed the 8 repos into pgvector | 0.7 | Jules | M |
| 0.9 | `teams` server: `wks_teams_post` + `wks_teams_await_approval` (Vault creds) | 0.3, 0.5 | Jules | L |
| 0.10 | `clickup` server: list/update/assign | 0.5 | Jules | M |
| 0.11 | Base Chief image: LangGraph runtime + memory/Hub clients + OTEL | 0.5 | Jules | M |
| 0.12 | Geoff: orchestrator workflow + routing + gating | 0.9–0.11 | Geoff dev | L |
| 0.13 | Addie: triage graph + `wks_diag_run` (read-only) | 0.11, 0.12 | Addie dev | M |
| 0.14 | Franklin: RCA graph over repo indexes; fix-spec output | 0.8, 0.12 | Franklin dev | L |
| 0.15 | Baseline observability: Loki labels, COT Overview dashboard | 0.3, 0.11 | infra | M |
| 0.16 | End-to-end test harness (config-error + defect tickets) + restart-recovery test | 0.12–0.14 | all | M |

Est. key: S ≈ ≤1 day, M ≈ 2–4 days, L ≈ ~1 week (solo-ish, 3-person team).

## Definition of done (gate to P1)

All [Phase 0 acceptance criteria](../prd/phase-0-mvp.md#acceptance-criteria) pass; the
restart-recovery test is green; secrets-grep is clean; a junior completes the
deploy/restart runbook unaided.

## Risks specific to P0

- Embedding/recall quality over the 8 repos (mitigate: tune chunking + HNSW params,
  assert on planted symbols in 0.16).
- Graph API / ClickUp auth + egress (mitigate: validate the allowlist early, 0.9/0.10).

## Copilot prompt blocks

```copilot-prompt
# Repo indexer (work item 0.8)
Write an indexer that walks each of the 8 repos (internal mirror), chunks code/docs,
computes embeddings with the local embedding model, and upserts into repo_chunk
(platform/memory/shared/schema.sql) with repo/path/ref/start_line/end_line. Idempotent
re-index by (repo, path, ref). Expose a CLI `cot-index --repo <name>`; document it in
docs/runbooks/rebuild-memory-index.md.
```

```copilot-prompt
# End-to-end harness (work item 0.16)
Build a test that creates two ClickUp tickets (one config-error, one defect), runs the
loop, and asserts: Addie finding present; Franklin fix-spec cites a real file/line;
wks_teams_await_approval blocked the prod step; logs correlate by ticket_id. Then kill
the orchestrator mid-run and assert the workflow resumes from durable state.
```
