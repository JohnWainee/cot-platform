# Contributing to Chief of Teams

This repo runs the **full audit-shop** flow even solo. The point is a clean audit
trail and low-surprise changes, not ceremony.

## Branch & PR flow

1. **Issue first.** Every change starts from a GitHub issue (use the templates in
   `.github/ISSUE_TEMPLATE/`).
2. **Branch.** `git switch -c <type>/<short-slug>` off `main`
   (e.g. `docs/phase-2-prd`, `feat/mcp-hub-registry`).
3. **`main` is protected.** No direct pushes. All changes land via PR with CI green.
4. **PR.** Fill in `.github/pull_request_template.md`. Self-review counts when solo,
   but the checklist must be honestly completed.
5. **Merge** after CI passes and the PR checklist is satisfied. Squash-merge to keep
   `main` linear.

## Conventional commits

Format: `<type>(<scope>): <subject>`. Types: `feat`, `fix`, `docs`, `chore`,
`refactor`, `test`, `ci`, `build`, `perf`. Examples:

```text
docs(prd): add phase-2 provisioning & config PRD
chore(scaffold): add MCP Hub server template
ci: add markdownlint + link-check workflows
```

PR titles are also linted as conventional commits (the squash-merge subject).

## CI gates

- **`docs-ci`** — `markdownlint` across all Markdown + a structure check (every ADR
  has the required sections; every phase PRD has Acceptance Criteria, Test Plan,
  Rollback).
- **`link-check`** — Markdown link checker on changed docs.

Run locally before pushing:

```bash
npx markdownlint-cli2 "**/*.md"
node scripts/check-doc-structure.mjs
```

## Sandbox allowlist & escalation boundaries

COT distinguishes **architect-owned** files (need sign-off) from **engineer-owned**
files (changeable unattended within guardrails). This boundary also governs what an
**agent** may change on its own. It is enforced socially via `CODEOWNERS` + PR review.

| Class | Examples | Who may change unattended |
|---|---|---|
| **Architect-owned** | `docs/prd/**`, `docs/adr/**`, `CODEOWNERS`, `deploy/k8s/network-policies/**` (egress), Vault policies, the egress matrix | Humans only, via PR + sign-off |
| **Engineer-owned** | `chiefs/*/system-prompt.md`, `chiefs/*/tools.md`, `mcp-hub/servers/**` (within contract), `scripts/**`, runbooks | Engineers (and, later, gated agents) within guardrails, via PR |
| **Generated/stub** | helm/k8s templates, server skeletons | Engineers; regenerate freely |

Severity tiers (**Critical / High / Medium / Low**) are used in ADRs and review
notes. Anything touching egress, secrets, or production action is **Critical** and
always requires a human gate.

## Docs conventions

- MCP tool names: **`wks_` prefix, `snake_case`** (e.g. `wks_ticket_update`).
- Every phase PRD and implementation plan embeds ` ```copilot-prompt ` blocks a
  junior can paste into GitHub Copilot.
- Keep prose dense and high-signal. No filler.
