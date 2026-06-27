# Memory subsystem — resource review & implementation options

> **Status:** Analysis / recommendation (not a decision record). Feeds a future
> `ADR-0008` once an option is chosen. No code is implemented by this document —
> COT is phase-gated ("no logic yet").
>
> **Scope:** how to build COT's two-tier memory ([ADR-0006](../adr/0006-two-tier-memory.md),
> [ADR-0004](../adr/0004-shared-semantic-store.md)) from the existing stubs in
> [`mcp-hub/servers/memory/`](../../mcp-hub/servers/memory/README.md) and
> [`platform/memory/`](../../platform/memory/per-chief/README.md), reusing three
> external projects we were asked to review.

## Context

COT has **accepted** a two-tier memory model but only **stubs** exist:

- **Tier 1 (per-Chief):** Markdown + YAML + **SQLite FTS5**, isolated vault, PACE
  tiers (`working → long_term → archived`, plus `projects/`, `followups/`), lazy
  in-session maintenance, **no cron**. Stubs:
  [`platform/memory/per-chief/README.md`](../../platform/memory/per-chief/README.md),
  contract [`wks_memory_capture`](../../mcp-hub/contracts/wks_memory_capture.md).
- **Tier 2 (shared):** **Postgres + pgvector** — the 8-repo indexes + curated
  `org_context`; read by all Chiefs, writes curation/approval-gated. Stub schema:
  [`platform/memory/shared/schema.sql`](../../platform/memory/shared/schema.sql).
- Both tiers are exposed behind **one** `memory` MCP server with a small tool set:
  `wks_memory_capture`, `wks_memory_search`, `wks_memory_status`, `wks_repo_search`,
  `wks_repo_read` ([`mcp-hub/servers/memory/README.md`](../../mcp-hub/servers/memory/README.md)).

We were asked to review three external memory projects and recommend three
implementation options for bringing real memory into this environment. All three
turn out to be agent-memory systems that map onto the model above.

## Resource reviews

### 1. `smriti-mcp` — deepak-bhardwaj-ps

A **portable, database-free memory server for the Model Context Protocol**, in
**Python 3.10+**. Stores memories as **Markdown files with YAML frontmatter**,
organized by category, with full-text search, `[[wikilink]]` cross-references,
auto-generated indexes, and archive (soft-delete) support.

- **Components:** `MemoryStore` (file I/O engine), `Server` (MCP stdio server),
  `CLI`, `Frontmatter` (YAML parser). Storage under `~/.smriti/memory/<category>/`.
- **Tools:** `create_memory`, `get_memory`, `append_memory`, `update_memory`,
  `delete_memory`, `remember`, `consolidate_memory`, `search_memory`,
  `list_memories`, `archive_memory`, `build_memory_index`, `rebuild_memory`,
  `load_memory_index`.
- **Notable:** filenames track titles (Obsidian-style link resolution); `remember()`
  treats supplied metadata as authoritative; `rebuild_memory` repairs frontmatter
  and normalizes wikilinks.

**Fit:** the closest of the three to COT's **Tier-1** — same language (Python),
same protocol (**MCP**), same storage philosophy (**Markdown + frontmatter, no
DB**, full-text search). Its `search_memory` / `consolidate_memory` / `archive_memory`
/ `rebuild_memory` line up with COT's `wks_memory_search`, lazy compaction, archive
tier, and the index-rebuild runbook.

**Risks / gaps:** flat category model, not COT's PACE tiers
(`working/long_term/archived` + budgets/promotion/retention-exemption); no
per-Chief vault isolation; no lazy-maintenance status flags; **license must be
confirmed before forking** (see Open items).

### 2. `echoes-vault-opencode` — psinetron

A **TypeScript OpenCode plugin** (MIT) giving agents persistent, Obsidian-compatible
memory as Markdown files committed in the repo, following Google's **Open Knowledge
Format (OKF)** frontmatter. Vault: `index.md` (registry), `pages/` (encyclopedia),
`daily/` (`YYYY-MM-DD.md` session logs), `assets/`, `raw/` (read-only sources).

- **Lifecycle (the valuable part):** `/echoes-start` restores context from the last
  3 daily logs + full index; `echoes_append_to_daily_log` captures decisions
  mid-session; `/echoes-end` distills the session into vault entries;
  `/echoes-status` reports vault health.
- **Philosophy:** "maximum technical density" (ADR-style records, not chat
  transcripts); **idempotent** (never overwrites user edits); **deprecate, don't
  delete** (full audit trail).

**Fit:** the **session-lifecycle pattern** is what COT lacks — restore-on-start,
append-during, distill-on-end map naturally onto a LangGraph orchestration layer
around Tier-1. The `raw/` (immutable) vs `pages/` (maintained) split echoes
karpathy's model. The deprecate-don't-delete rule matches COT's "nothing is ever
deleted; review archives."

**Risks / gaps:** **TypeScript + OpenCode-bound** — wrong runtime for COT (Python /
LangGraph / MCP). Adopt the **patterns**, not the code. No vector/semantic tier.

### 3. karpathy LLM-wiki gist

A **conceptual method** (no shippable code) for a self-maintaining, LLM-curated
knowledge base in three layers: **raw sources** (immutable), an **LLM-maintained
wiki** (interconnected Markdown pages), and a **schema** doc defining conventions.
Three operations:

- **Ingest:** read a source, extract, integrate across 10–15 wiki pages, maintain
  cross-references, flag contradictions.
- **Query:** search the wiki index, synthesize a cited answer, optionally file the
  result back as a new page.
- **Lint:** periodic health check for contradictions, stale claims, orphan pages,
  missing links.

Core insight: *"the tedious part of maintaining a knowledge base is not the reading
or the thinking — it's the bookkeeping"*, which LLMs do well and humans abandon.

**Fit:** the **method** for COT's **Tier-2** curated `org_context` (ingest the 8
repos + ADRs/runbooks/incidents → maintained org wiki; query = `wks_repo_search` /
`wks_memory_search`; lint = the consolidation/health loop). Also reframes Tier-1's
"lazy maintenance" as a per-Chief lint pass.

**Risks / gaps:** intentionally abstract — needs a concrete schema, page format, and
tooling; the ingest/lint loop has real **LLM-token cost** that must be budgeted
(and, in COT, gated against poisoning).

## How the resources map to COT

| COT element | smriti-mcp | echoes-vault | karpathy wiki |
|---|---|---|---|
| Tier-1 storage (MD+YAML+FTS5) | **engine (fork)** | structure ideas | — |
| `wks_memory_capture` / `wks_memory_search` | adapt `remember` / `search_memory` | — | — |
| Lazy maintenance / `wks_memory_status` | `consolidate`/`rebuild` | `/echoes-status` | **lint** |
| Session loop (restore/distill) | — | **pattern (port)** | ingest/query |
| Tier-2 semantic (`wks_repo_*`, `org_context`) | — | `raw/` vs `pages/` split | **method** |
| Immutable sources / provenance | archive | `raw/`, deprecate-don't-delete | raw-source layer |

**Locked decisions (from the interview that produced this doc):** target the
**whole** subsystem (both tiers, phased); **fork & adapt smriti-mcp** as the engine;
house it in a **new standalone repo** (`cot-memory`) vendored/deployed into COT;
deliverable now is **this doc only**.

## Three implementation options

All three fork smriti-mcp into a new `cot-memory` repo and reach the same two-tier
end state. They differ on **which organizing principle leads and what ships first.**

### Option 1 — smriti-core, phased two-tier *(recommended)*

Fork smriti-mcp as the Tier-1 engine; grow into Tier-2 behind the same MCP server.

- **P0 — Tier-1 only.** Adapt smriti's tools to COT contracts
  (`wks_memory_capture`/`_search`/`_status`); replace flat categories with PACE
  tiers (`working → long_term → archived` + `projects/`, `followups/`); add
  per-Chief vault isolation, working-budget caps, conservative promotion,
  retention-exempt tags (`#person`/`#decision`/`#high-signal`), and lazy
  `needs_compact`/`needs_review` flags. Ship the one `memory` server every Chief uses.
- **P1 — Tier-2.** Add pgvector-backed `wks_repo_search` / `wks_repo_read` and the
  shared `wks_memory_search` over `org_context`, plus a **karpathy-style
  ingest/lint** path for curated writes (approval-gated, `curated_by` provenance) —
  same MCP server, second backend, per ADR-0006.
- **Echoes lifecycle** = a thin **LangGraph** layer (restore last N / distill) that
  *calls* Tier-1 tools — no new storage.

➕ Matches accepted ADR-0006/0004 exactly · fastest to the P0 foundation every Chief
needs · folds echoes + karpathy in at the right phase without over-building · best
fit to the prime directive (junior-operable, simplicity > cleverness).
➖ Cross-Chief semantic recall (Franklin's 8-repo need) waits for P1.

### Option 2 — unified wiki-first

Lead with karpathy's LLM-wiki **method** as the organizing principle across **both**
tiers: Tier-1 and Tier-2 are the same "wiki" at different scope/visibility
(per-Chief vs shared). smriti fork is the file/FTS substrate; pgvector is the shared
semantic layer; ingest/query/lint is the universal interface from day one.

➕ Richest cross-referencing/consolidation immediately · one mental model for all
memory · strongest long-term knowledge quality.
➖ Heaviest up-front build (schema doc, lint loop, ingest pipeline before first
value) · highest LLM-token maintenance cost · slowest to a usable P0 · more concepts
for a junior to hold at once (tension with the prime directive).

### Option 3 — lifecycle-first / session-centric

Lead with the echoes session UX: every Chief session does **start** (restore last N
daily logs + index) → **work** (`append_to_daily_log`) → **end** (distill into
vault). smriti fork is storage; a `daily/` + `pages/` layout mirrors echoes; Tier-2
semantic is deferred.

➕ Best audit trail and session experience earliest · very debuggable/grep-able ·
natural human-in-the-loop review surface (daily logs).
➖ Defers cross-Chief semantic recall (Franklin) longest · a `daily/`-centric layout
diverges from PACE `working/long_term/archived` and would need reconciling with
ADR-0006 · optimizes session ergonomics over the foundational capability gap.

## Recommendation

**Option 1 — smriti-core, phased two-tier.** It is the only option that matches the
already-accepted ADRs without re-litigating them, delivers the P0 capability every
Chief depends on the fastest, and still captures the best of all three resources:
smriti as the engine (P0), karpathy's ingest/lint for Tier-2 curation (P1), and
echoes' lifecycle as a thin orchestration layer (P1). Options 2 and 3 each front-load
one resource's philosophy at the cost of slower foundational value and friction with
ADR-0006 — keep them as documented escape hatches if the curation-quality (Option 2)
or session-audit (Option 3) needs ever dominate.

## Open items (gates before any code)

1. **License check on smriti-mcp** — confirm its license permits a fork and
   in-house modification before forking (echoes is MIT; smriti unconfirmed). Hard gate.
2. **Create the `cot-memory` repo** — recommended home, *not created by this doc*;
   scaffold it once Option 1 is approved (structure, README, the `wks_memory_*`
   contracts, CI), then vendor/deploy into COT.
3. **Follow-up records** — add `ADR-0008` capturing the "fork smriti into standalone
   `cot-memory`" sourcing decision, and update
   [`mcp-hub/servers/memory/README.md`](../../mcp-hub/servers/memory/README.md) to
   point at the new repo.
4. **Embedding model + HNSW params** for Tier-2 are set at implementation against
   the chosen local model (ADR-0004 leaves `vector(768)` and index params as
   placeholders).
