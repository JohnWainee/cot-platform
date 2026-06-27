# NOTICE — attribution & provenance

`cot-memory` is a **fork of `smriti-mcp`** (a portable, database-free memory server
for the Model Context Protocol). The fork was confirmed to be **licence-permitted**
before this scaffold was created (the gate flagged in the COT memory analysis is
cleared).

## Obligations to carry forward

When this scaffold is lifted into the standalone `cot-memory` repo, the following
must be done **before** any upstream code is copied in:

1. **Copy upstream's `LICENSE`** into the repo verbatim and keep this `NOTICE.md`
   pointing at it. Record the exact upstream commit/tag the fork is based on.
2. **Preserve copyright headers** in any files derived from `smriti-mcp`.
3. **Mark COT-original files** (anything not derived from upstream — e.g. the PACE
   tiering, per-Chief vault isolation, and `wks_memory_*` adapters) under COT's own
   terms; see [`LICENSE`](LICENSE) in this directory.

## Upstream

- Project: `smriti-mcp`
- Relationship: fork (we cherry-pick fixes; we do not track upstream continuously)
- Base commit/tag: _to be recorded at fork time_
