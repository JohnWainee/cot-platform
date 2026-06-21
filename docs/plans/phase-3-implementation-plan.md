# Phase 3 — Implementation plan (identity & self-scaling)

> Work breakdown for [`phase-3-identity-selfscaling.md`](../prd/phase-3-identity-selfscaling.md).
> Enter after P2 stable + owner approval. Adds **Ida** + **Jane**. Chief spawning and
> every identity write are **human-gated (Critical)**.

## Sequenced work breakdown

| # | Work item | Depends on | Owner | Est. |
|---|---|---|---|---|
| 3.1 | `ad` server: `wks_ad_account_report` (read) + `wks_ad_account_lifecycle` (gated) + `wks_dns_ip_reclaim` (gated) | P2 | Jules | L |
| 3.2 | `entra` server: `wks_entra_review` (read) | P2 | Jules | M |
| 3.3 | `vault` server: `wks_secret_rotate` (gated) with previous-version recovery | P2 | Jules | M |
| 3.4 | Ida Chief: expiry-review → propose-rotation/lifecycle → gated-apply graph | 3.1–3.3 | Ida dev | L |
| 3.5 | `chief-factory`: `wks_chief_spawn` (gated, Critical) — scaffold + isolate + register approved tools | P2 | Jane dev | L |
| 3.6 | Jane Chief: research-domain → produce Chief spec → gated spawn | 3.5 | Jane dev | L |
| 3.7 | Runbooks: `ad-account-lifecycle.md`, `credential-expiry-review.md` | 3.4 | all | S |
| 3.8 | Spawn isolation test: new Chief is egress-denied, isolated vault, registry-gated tools | 3.5 | all | M |

## Definition of done

All [Phase 3 acceptance criteria](../prd/phase-3-identity-selfscaling.md#acceptance-criteria)
pass; `wks_chief_spawn` cannot create anything without approval; a spawned Chief is
provably isolated and egress-denied by default; rotations are reversible in-window.

## Copilot prompt blocks

```copilot-prompt
# Chief spawn isolation test (work item 3.8)
Write a test that drives Jane to propose a new Chief, asserts NOTHING is created before
approval, then after approval asserts: the new Chief has its own vault (no access to
others'), egress: none in its NetworkPolicy, and only the approved tools granted in the
Hub registry. Tear it down declaratively at the end.
```
