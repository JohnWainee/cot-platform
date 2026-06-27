# `wks_memory_search` — contract (STUB)

- **Server:** memory · **Kind:** read · **Gate:** none · **Egress:** none

## Purpose

Retrieve relevant entries for a Chief. Searches the caller's **private vault**
(Tier-1 FTS5) and, in P1, the **shared semantic tier** (Tier-2 pgvector, read-only).

## Inputs

| Field | Type | Required | Notes |
|---|---|---|---|
| `query` | string | yes | natural-language or keyword query |
| `scope` | enum(vault,shared,both) | no | default `vault`; `shared`/`both` need P1 |
| `kind` | string | no | filter by capture kind |
| `project` | string | no | restrict to a project's memories |
| `limit` | int | no | max results (default 10) |

## Outputs

| Field | Type | Notes |
|---|---|---|
| `results` | object[] | each: `id`, `path` (vault) or `source` (shared), `score`, `snippet` |

## Side effects

None. Read-only.

## Errors

- `vault_uninitialized` → run `wks_memory_status`; onboarding initializes the vault.
- `shared_tier_unavailable` → Tier-2 not yet enabled (P1) or Postgres unreachable;
  fall back to `scope: vault`.
