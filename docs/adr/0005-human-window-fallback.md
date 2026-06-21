# ADR-0005 — Human window & OSS fallbacks

## Status

Accepted

## Context

Humans interact with COT through a chat window (notifications + approvals) and a ticket
system. P0 targets are **Microsoft Teams** + **ClickUp**. The brief requires an
open-source fallback for each, with a migration note. Both touch the **egress matrix**
([ADR-0007](0007-egress-human-in-loop.md)). Severity: **Medium** (swappable behind an
adapter).

## Options

Per surface, the choice is proprietary-SaaS (P0 target) vs a self-hostable OSS analog:

### Chat: Teams (P0) vs Mattermost (OSS) vs Rocket.Chat (OSS)

- **Teams:** ➕ already the team's tool; ➖ requires `graph.microsoft.com` egress.
- **Mattermost:** ➕ self-hosted, K8s-deployable, bots + incoming/outgoing webhooks,
  near-zero external egress; ➖ another service to run.
- **Rocket.Chat:** similar to Mattermost; chosen against for slightly heavier ops.

### Tickets: ClickUp (P0) vs Plane (OSS) vs OpenProject/Vikunja (OSS)

- **ClickUp:** ➕ already in use; ➖ requires `api.clickup.com` egress.
- **Plane:** ➕ closest ClickUp analog, self-hosted, REST API, K8s-deployable.
- **OpenProject/Vikunja:** viable but further from the ClickUp model.

## Decision

**P0 = Teams + ClickUp.** **OSS fallbacks = Mattermost (↔Teams) + Plane (↔ClickUp).**
Both surfaces sit behind a **swappable adapter** in the `teams`/`clickup` MCP servers,
so Chief logic never knows which backend is live.

## Consequences

- **Positive:** ship on the team's existing tools now; a hard-air-gap path exists
  (self-host Mattermost + Plane → external egress drops to near-zero).
- **Negative / mitigations:** maintaining two adapters per surface — mitigated by
  keeping the adapter interface tiny (post message, await approval; list/update/assign
  ticket).
- **Migration note:** switching Teams→Mattermost or ClickUp→Plane = implement the same
  adapter interface + update the egress matrix; no Chief code changes. This is **Open
  Question #4** for the owner (adopt OSS from day one for air-gap, or start on SaaS).
