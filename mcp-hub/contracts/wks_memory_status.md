# `wks_memory_status` — contract (STUB)

- **Server:** memory · **Kind:** read · **Gate:** none · **Egress:** none

## Purpose

Report vault health and any **lazy-maintenance** work due, and initialize the vault
on first call. This is the no-cron heartbeat: the Chief calls it once per session and
runs whatever it flags, silently, after replying to the first message.

## Inputs

| Field | Type | Required | Notes |
|---|---|---|---|
| `chief` | string | no | defaults to the calling Chief's identity |

## Outputs

| Field | Type | Notes |
|---|---|---|
| `initialized` | bool | false → the call just created the vault layout |
| `needs_compact` | bool | working tier older than 24h or over the hard cap |
| `needs_review` | bool | promotion/retention review due (7d+) |
| `needs_heartbeat` | bool | opt-in proactive followup sweep due |
| `counts` | object | entries per tier (`working`/`long_term`/`archived`) |

## Side effects

May create the vault layout on first call (`initialized: false`). Never deletes.

## Errors

- `vault_locked` → another process holds the index; retry after a short backoff.
