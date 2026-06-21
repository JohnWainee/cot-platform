# Hardware recommendation (sized BOM)

- **Status:** Recommendation only — **no hardware is committed.** Drives Open Question
  #5 (budget ceiling) in the [master PRD](prd/COT-master-PRD.md).
- **Sizing target:** 3 users · 12–24 tickets/day · **90–95% uptime** (modest). This is
  a **low-QPS** workload — peak concurrency is a handful of requests, not a fleet.
  Size for **model quality at low concurrency**, not throughput.

## The one decision that dominates cost: GPU VRAM

The reasoning tier (Geoff/Franklin/Jules) wants a ~32B coder model and a 30–70B
instruct model. VRAM needed (4–5-bit quant, the practical local default):

| Model class | Approx VRAM (Q4–Q5) | Serves |
|---|---|---|
| 7–8B (light/triage) | 6–10 GB | Addie |
| ~32B (reasoning/coder) | 22–28 GB | Franklin, Jules |
| 70B (strong reasoning) | 40–48 GB | Geoff (optional; 32B is fine to start) |
| Embeddings (768-dim) | ~2 GB | Tier-2 indexing |

At this load you can **run models serially on one GPU** — you don't need them all
resident at once. The choice is how much you keep hot.

## Tier 1 — Model serving host (the GPU box)

### Cheapest viable starting point

- **1× 24 GB GPU** (e.g. used RTX 3090 / RTX 4090) in a workstation:
  16-core CPU, 64–128 GB system RAM, 2 TB NVMe.
- Runs the **light tier + a 32B Q4 reasoning/coder model** comfortably (serially).
  70B is out unless offloaded (slow). **This is enough to ship P0** with Ollama.
- Est. **$2.5k–4k** (used GPU) as a single-box start.

### Recommended (P0→P1 headroom)

- **1× 48 GB GPU** (RTX 6000 Ada / A6000 48 GB): keeps a 32B model hot **and** fits a
  70B Q4 when you want stronger Geoff reasoning; supports vLLM batching at P1.
- Host: 16–32-core CPU, 128 GB RAM, 2–4 TB NVMe.
- Est. **$8k–12k** depending on GPU sourcing.

### Headroom option — Strix Halo class (unified memory)

- **AMD Ryzen AI Max ("Strix Halo")** mini-workstations expose up to **~128 GB unified
  memory** to the iGPU/NPU. Attractive as a **cheap, low-power, single-box** inference
  node that can hold large models in unified memory — at **lower throughput** than a
  discrete 48 GB GPU. Good fit for a hard-air-gap, low-QPS site, or as a second
  inference node for resilience. Validate token/sec on your target models before
  committing; treat as a cost/power play, not a throughput play.

> Spare-parts note: keep one GPU/host spare path in mind — model serving is the most
> likely hardware SPOF. The light tier can temporarily cover reasoning at reduced
> quality during an outage (see [model-serving-host-ops](runbooks/model-serving-host-ops.md)).

## Tier 2 — RKE2 Kubernetes nodes (everything else)

Orchestrator, NATS, Postgres+pgvector, MCP servers, memory, observability — all CPU/RAM
work, modest at this scale.

### Cheapest viable

- **1 node** (can be the GPU box itself, or a second server): 16 vCPU, 64 GB RAM,
  1–2 TB NVMe. Single control-plane = no HA, acceptable at 90–95% with clean restarts.

### Recommended

- **3 small nodes** (e.g. 8–16 vCPU, 32–64 GB RAM, 1 TB NVMe each) for RKE2
  control-plane quorum + room to schedule workloads. Gives you node-failure tolerance
  without true HA ambitions. Est. **$3k–6k** total (or VMs on existing vSphere — COT
  already targets vCenter 8.0.3.x, so these can be **VMs, not metal**).

## Tier 3 — Storage

| Need | Size | Notes |
|---|---|---|
| Postgres + pgvector | 100–500 GB NVMe | grows with the 8 repo indexes; budget headroom |
| Per-Chief vaults | tens of GB | Markdown + SQLite; tiny |
| Model weights | 100–300 GB | depends on how many models you keep |
| Backups | 2–3× live data | retention per backup policy |

Use the RKE2 storage class with CSI **snapshot** support (required by the
[backup/restore runbook](runbooks/backup-restore-postgres-pgvector.md)).

## Bottom line

| Posture | Spend (rough) | What you get |
|---|---|---|
| **Cheapest viable** | ~$3k–5k | 1× 24 GB GPU box doubling as the node; ships P0 on Ollama |
| **Recommended** | ~$11k–18k | 1× 48 GB GPU host + 3 RKE2 VMs/nodes; P0→P1 with vLLM headroom |
| **Air-gap / low-power** | varies | add a Strix Halo-class node for large models in unified memory |

The biggest lever is the GPU. Start at 24 GB if budget is tight (P0 works); step to
48 GB when Geoff's reasoning quality or P1 throughput justifies it. Reuse existing
vSphere for the non-GPU nodes to avoid buying metal.
