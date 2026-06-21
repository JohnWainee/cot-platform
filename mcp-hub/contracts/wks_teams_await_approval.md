# `wks_teams_await_approval` — contract (STUB)

- **Server:** teams · **Kind:** write-block · **Gate:** human · **Egress:** graph.microsoft.com

## Purpose

**The** human-in-loop primitive. Posts a summarized proposal to a Teams channel and
**blocks** the workflow until a human approves, rejects, or edits. Every
production-affecting action funnels through this.

## Inputs

| Field | Type | Required | Notes |
|---|---|---|---|
| `summary` | string | yes | 10-second-readable description of the proposed action |
| `detail` | string | no | full context / diff / fix spec |
| `options` | string[] | no | default `["approve","reject"]`; may add `"edit"` |
| `timeout_s` | int | no | default escalates to a named human if unanswered |

## Outputs

| Field | Type | Notes |
|---|---|---|
| `decision` | enum(approve,reject,edit) | |
| `actor` | string | who decided |
| `edited_payload` | object | present when `decision=edit` |

## Side effects

Posts to Teams; durably parks the orchestrator workflow (Temporal signal) until a
human responds. No production action occurs unless `decision=approve`.

## Errors

- `timeout` → re-routes per escalation policy; never auto-approves.
