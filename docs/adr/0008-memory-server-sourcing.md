# ADR-0008 — Memory server sourcing: fork smriti-mcp into a standalone repo

## Status

Accepted

## Context

[ADR-0006](0006-two-tier-memory.md) accepted a two-tier memory model and
[ADR-0004](0004-shared-semantic-store.md) chose Postgres + pgvector for Tier 2.
The follow-up review in
[`docs/analysis/memory-implementation-options.md`](../analysis/memory-implementation-options.md)
compared three external memory projects and recommended **Option 1 — smriti-core,
phased two-tier**: take `smriti-mcp` (a Python, MCP-native, Markdown + YAML + FTS
memory server) as the Tier-1 engine and grow Tier-2 behind the same MCP server.

This ADR records the **sourcing and packaging** decision that Option 1 implies:
where the memory server code lives and how we take on `smriti-mcp`. The upstream
licence has been **confirmed to permit a fork** (the gate flagged in the analysis
doc is cleared). Severity: **Medium** (packaging/ownership; reversible, but sets the
contribution and deploy boundary for every Chief's memory).

## Options

### A. Build the memory server from scratch in `mcp-hub/servers/memory/`

- ➕ No external code to vet; lives in the monorepo next to the contracts.
- ➖ Re-implements storage, frontmatter, FTS, and indexing that `smriti-mcp` already
  provides; slowest path to a working Tier-1; contradicts the "reuse over rewrite"
  finding of the analysis.

### B. Vendor `smriti-mcp` as an upstream dependency, wrap it

- ➕ Gets upstream fixes for free; thin adapter surface.
- ➖ Couples COT to upstream's release cadence and API; our PACE tiers, per-Chief
  vault isolation, lazy-maintenance flags, and `wks_memory_*` contracts need changes
  the upstream may not accept; air-gapped on-prem deploys want a pinned, in-house tree.

### C. Fork `smriti-mcp` into a standalone `cot-memory` repo

- ➕ We own the tree: adapt tools to the `wks_memory_*` contracts, add PACE tiers and
  per-Chief isolation, and pin it for air-gapped deploys; independently versioned,
  tested, and containerised; a clean boundary the monorepo references but does not vendor.
- ➕ Tier 2 (pgvector) is added later behind the **same** server, per ADR-0006.
- ➖ One more repo to operate; we carry the merge burden for any upstream changes we
  want (mitigated: we cherry-pick, we do not track upstream continuously).

## Decision

**Option C — fork `smriti-mcp` into a new standalone repo, `cot-memory`.** It is the
home for the two-tier memory MCP server. The monorepo's `mcp-hub/servers/memory/`
becomes a thin reference/pointer to that repo, not a second implementation.

The full **P0 scaffold** (package skeleton, adapted `wks_memory_*` contracts,
architecture notes, CI, no business logic) was first staged in this monorepo under
`incubating/cot-memory/`, then extracted — with history preserved via
`git subtree split` — into the standalone `JohnWainee/cot-memory` repo, which is now
its home. The staging directory has since been removed.

## Consequences

- **Positive:** fastest path to a working Tier-1 that every Chief depends on; we keep
  full control for PACE tiers, contract alignment, and air-gapped pinning; Tier-2
  slots in behind the same server with no contract churn for Chiefs.
- **Negative / mitigations:** a separate repo to operate — mitigated by reusing the
  same docs-CI conventions and keeping `mcp-hub/servers/memory/` as the single
  in-monorepo pointer. Upstream drift — mitigated by cherry-picking, not tracking.
- **Follow-ups:** the `cot-memory` repo now hosts the extracted scaffold and carries
  the upstream `smriti-mcp` attribution/licence (see its `NOTICE.md` and
  `LICENSE.smriti-mcp`); set the embedding model and HNSW params when Tier-2 lands
  (ADR-0004 placeholders).
