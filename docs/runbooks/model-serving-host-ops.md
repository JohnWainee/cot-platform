# Runbook — Model serving host operations

## Purpose

Keep local model serving healthy; add/swap a model; recover a slow or down host.

## When to use

- Reasoning latency alert fired, or a Chief reports model timeouts.
- You need to add/swap an open-weight model (from the internal mirror only).

## Prerequisites

- Access to the GPU/accelerator host(s) and the `cot` namespace.
- The internal model mirror reference (no public pulls — air-gapped, ADR-0007).

## Health check

```bash
kubectl -n cot get pods -l app in (ollama,vllm)        # [finalize at impl]
# Ollama:
kubectl -n cot exec deploy/ollama -- ollama list
# vLLM (P1+): hit the OpenAI-compatible endpoint health route.
```

Check the "Model Serving" Grafana panel: tokens/sec, p95 latency, GPU memory.

## Add / swap a model (from the internal mirror)

```bash
kubectl -n cot exec deploy/ollama -- ollama pull <model-from-mirror>   # [finalize at impl]
```

Then point the Chief's `model_tier` at it (chief.yaml, via PR) and
`helm upgrade`. Validate latency before relying on it.

## Recover a slow/down host

1. Confirm GPU availability (driver/VRAM): `nvidia-smi` on the host.
2. Restart the serving deployment: `kubectl -n cot rollout restart deploy/<ollama|vllm>`.
3. If a single model is wedged, reload just that model.
4. If the host is hard-down, Chiefs degrade — light tier (Ollama) can temporarily
   serve reasoning Chiefs at reduced quality; note it and open an incident.

## Verification

- Grafana model panel back within SLO; a test ticket completes within expected latency.

## Rollback

Revert the `model_tier` change (PR + `helm upgrade`) to the previously validated model.

## Escalation

Hardware/driver failure → owner; track a hardware spare per
[hardware-recommendation](../hardware-recommendation.md).
