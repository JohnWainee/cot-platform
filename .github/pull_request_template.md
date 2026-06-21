<!-- PR title MUST be a conventional commit, e.g. docs(prd): add phase-1 PRD -->

## What & why

<!-- One-paragraph summary. Link the issue: Closes #NN -->

Closes #

## Type

- [ ] docs (PRD / ADR / plan / runbook)
- [ ] scaffolding / stub
- [ ] tooling / CI
- [ ] feature (requires an approved phase PRD)
- [ ] fix

## Phase gate

- [ ] This change does **not** implement Chief business logic, **or** the relevant
      phase PRD is approved and linked above.

## Checklist

- [ ] Conventional-commit PR title.
- [ ] `npx markdownlint-cli2 "**/*.md"` passes locally.
- [ ] `node scripts/check-doc-structure.mjs` passes locally.
- [ ] New ADRs include Status / Context / Options+tradeoffs / Decision / Consequences.
- [ ] New phase PRDs include Acceptance Criteria, Test Plan, Rollback, Operability.
- [ ] MCP tool names use the `wks_` + `snake_case` convention.
- [ ] No secrets, model blobs, or vault data committed.
- [ ] Architect-owned files (egress, Vault policy, ADRs, PRDs) reviewed if touched.

## Verification

<!-- How you confirmed this is correct (commands run, output, screenshots). -->
