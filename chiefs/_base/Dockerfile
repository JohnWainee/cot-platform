# Base Chief image — STUB. No business logic. Pinned digests added at build phase.
# syntax=docker/dockerfile:1
FROM python:3.11-slim AS base

# OCI labels for provenance (a junior can trace any running Chief back to here).
LABEL org.opencontainers.image.title="cot-chief-base" \
      org.opencontainers.image.source="https://github.com/JohnWainee/cot-platform" \
      org.opencontainers.image.description="Base image for COT Chiefs (stub)"

WORKDIR /chief

# Dependencies are intentionally NOT installed yet (phase-gated).
# Phase 0 will add: langgraph, the COT memory MCP client, the MCP Hub client,
# and an OpenTelemetry exporter — pinned, from an internal mirror (air-gapped).
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# Identity + config are mounted/copied per Chief at build time.
# COPY identity/IDENTITY.md /chief/identity/IDENTITY.md

# Runs as non-root (added with the real entrypoint).
# USER 10001

# Placeholder entrypoint so the stub image is inert and obvious.
ENTRYPOINT ["python", "-c", "print('COT Chief base image — stub. No logic yet.')"]
