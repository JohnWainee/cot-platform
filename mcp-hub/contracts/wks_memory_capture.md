# `wks_memory_capture` — contract (STUB)

- **Server:** memory · **Kind:** write · **Gate:** none · **Egress:** none

## Purpose

Persist durable context (a decision, name, date, preference, finding) into the
calling Chief's **private vault** (Markdown + YAML frontmatter, FTS5-indexed).

## Inputs

| Field | Type | Required | Notes |
|---|---|---|---|
| `kind` | enum(decision,fact,person,followup,note) | yes | drives retention/promotion |
| `topic` | string | yes | short title |
| `text` | string | yes | the content |
| `tags` | string[] | no | `#person`/`#decision`/`#high-signal` are retention-exempt |
| `project` | string | no | routes into a project memory if set |

## Outputs

| Field | Type | Notes |
|---|---|---|
| `id` | string | vault entry id |
| `path` | string | file written (runtime vault, not git) |

## Side effects

Writes one Markdown file to the Chief's working tier and updates the FTS5 index.
Does **not** write the shared semantic tier (that path is curation-gated).

## Errors

- `vault_uninitialized` → run `wks_memory_status`; onboarding initializes the vault.
- `working_over_hard_cap` → triggers lazy compaction next status call (PACE pattern).
