# cot-memory

> **Staging copy.** This directory is the P0 scaffold for the standalone
> `JohnWainee/cot-memory` repository. It lives under `incubating/` only because the
> session that generated it could not create the external repo (GitHub access was
> scoped to `cot-platform`). Once the repo exists, lift this tree into it (see
> [Extraction](#extraction)) and delete this directory.

The **two-tier memory MCP server** for Chief of Teams (COT). A fork of `smriti-mcp`,
adapted to COT's `wks_memory_*` contracts. See
[ADR-0008](../../docs/adr/0008-memory-server-sourcing.md) for why this is a fork in
its own repo, and
[`docs/analysis/memory-implementation-options.md`](../../docs/analysis/memory-implementation-options.md)
for the option it implements (Option 1 — smriti-core, phased two-tier).

## What it serves

- **Tier 1 — per-Chief vault (P0):** Markdown + YAML + **SQLite FTS5**, isolated per
  Chief, PACE-style tiers (`working → long_term → archived`, plus `projects/`,
  `followups/`), lazy in-session maintenance, **no cron**. This is what the scaffold
  targets first.
- **Tier 2 — shared semantic (P1):** **Postgres + pgvector** (the 8-repo indexes +
  curated org context), read by all Chiefs, writes curation/approval-gated. Added
  later behind the **same** server.

Tool surface (contracts in [`docs/contracts/`](docs/contracts/)):
`wks_memory_capture`, `wks_memory_search`, `wks_memory_status` (P0); `wks_repo_search`,
`wks_repo_read` (P1). These mirror the contracts of record in the monorepo at
`mcp-hub/contracts/`.

## Status

**Scaffold only — no business logic.** Every module raises `NotImplementedError`.
COT is phase-gated; implementation is unblocked per phase by the Phase-0 plan, not by
this scaffold existing.

## Layout

```text
cot-memory/
├── pyproject.toml          # package skeleton + entry point (no deps pinned yet)
├── src/cot_memory/
│   ├── store.py            # MemoryStore — PACE-tiered MD+FTS5 vault (stub)
│   ├── server.py           # MCP stdio server exposing wks_memory_* (stub)
│   └── cli.py              # `cot-memory` console entry point (stub)
├── docs/
│   ├── ARCHITECTURE.md     # tiers, data model, what is P0 vs P1
│   └── contracts/          # wks_memory_* contracts (impl-side mirror)
├── tests/
│   └── test_smoke.py       # import smoke test
└── .github/workflows/ci.yml
```

Runtime vault data (`**/vault/`, `*.db`) is git-ignored — it is per-Chief runtime
state, never source.

## Extraction

When the `cot-memory` repo exists, split this directory out preserving history:

```sh
# from a clone of cot-platform
git subtree split --prefix=incubating/cot-memory -b cot-memory-export
# then, in an empty clone of the new repo:
git pull <path-to-cot-platform> cot-memory-export
```

Then remove `incubating/cot-memory/` from `cot-platform` and leave
`mcp-hub/servers/memory/` as the pointer it already is.

## Provenance

Forked from `smriti-mcp`. Upstream attribution and licence obligations are recorded
in [`NOTICE.md`](NOTICE.md); the fork was confirmed licence-permitted before this
scaffold was created.
