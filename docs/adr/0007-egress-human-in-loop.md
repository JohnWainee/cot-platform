# ADR-0007 — Egress policy & human-in-loop security model

## Status

Accepted

## Context

COT is air-gapped/internal-only by default and must keep humans in the loop for every
significant decision and any code change. We need an enforceable model for (a) network
egress and (b) action gating that a junior can understand and audit. Severity:
**Critical** (data exfiltration + unauthorized production change are the worst-case
failures).

## Options

### Egress

- **A. Allow-all, block known-bad:** ➖ unacceptable for an air-gapped posture.
- **B. Default-deny + explicit per-component allowlist:** ➕ matches the brief; auditable;
  least privilege. ➖ requires discipline adding rows.
- **C. Per-Chief sidecar proxy with policy:** ➕ fine-grained; ➖ more moving parts than a
  3-person team needs now.

### Human-in-loop

- **A. Trust + after-the-fact audit:** ➖ violates the prime guarantee.
- **B. A single blocking gate primitive every action funnels through:** ➕ one concept,
  uniformly auditable. ➖ must be impossible to bypass.
- **C. Per-tool ad-hoc confirmations:** ➖ inconsistent; easy to forget; hard to audit.

## Decision

- **Egress: Option B.** Cluster-wide **default-deny** NetworkPolicy
  ([`deploy/k8s/network-policies/00-default-deny-egress.yaml`](../../deploy/k8s/network-policies/00-default-deny-egress.yaml)),
  plus an explicit allowlist row per component that demonstrably needs egress, each
  citing its justification. The egress matrix lives in the master PRD (§7.1). Changes
  are **Critical** and human-gated; egress files are **architect-owned** (CODEOWNERS).
- **Human-in-loop: Option B.** `wks_teams_await_approval` is the single **write-block**
  gate primitive; every production-affecting action, code/PR, and (P3) Chief spawn
  funnels through it. Timeouts re-route per escalation policy and **never auto-approve**.

## Consequences

- **Positive:** least-privilege egress that's trivially auditable (read the matrix +
  the NetworkPolicies); one uniform, bypass-resistant gate; OSS human-window fallback
  can drive external egress to near-zero.
- **Negative / mitigations:** adding a legitimate egress need requires an architect
  PR (intentional friction). Default for every new Chief/server is `egress: none` and
  no ungated write tool; the MCP Hub registry enforces tool grants.
- **Severity tiers** (Critical/High/Medium/Low) are used in findings/reviews; anything
  touching egress, secrets, or production action is **Critical**.
