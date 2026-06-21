# NetworkPolicies — egress enforcement (architect-owned)

COT is **air-gapped by default**. The model is: a cluster-wide **default-deny**
egress policy, plus **explicit per-Chief allowlists** that mirror the egress matrix
in the master PRD. Changing anything here is a **Critical**, human-gated change
(ADR-0007). Files here are stubs; real policies land per phase.

- `00-default-deny-egress.yaml` — deny all egress in the `cot` namespace.
- `<chief>-egress-allow.yaml` — one per Chief that *demonstrably* needs egress, each
  citing the matrix row that justifies it.

> RKE2 ships a CNI that enforces NetworkPolicy. Verify enforcement is on before
> relying on these (see incident-response runbook).
