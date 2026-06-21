-- Shared semantic memory (Tier 2) — Postgres + pgvector. STUB schema (ADR-0004/0006).
-- All Chiefs READ this tier; WRITES are curation/approval-gated to prevent poisoning.
-- Dimensions/index params are placeholders — set per the chosen local embedding model.

CREATE EXTENSION IF NOT EXISTS vector;

-- 1) Repo code/document chunks — the 8-repo indexes Franklin relies on.
CREATE TABLE IF NOT EXISTS repo_chunk (
    id           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    repo         TEXT        NOT NULL,
    path         TEXT        NOT NULL,
    ref          TEXT        NOT NULL,                 -- commit/sha indexed
    start_line   INT,
    end_line     INT,
    content      TEXT        NOT NULL,
    embedding    vector(768),                          -- match the embedding model dim
    indexed_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 2) Curated cross-Chief org context (decisions, runbook distillations, glossary).
CREATE TABLE IF NOT EXISTS org_context (
    id           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source       TEXT        NOT NULL,                 -- e.g. 'adr-0006', 'incident-123'
    title        TEXT        NOT NULL,
    content      TEXT        NOT NULL,
    embedding    vector(768),
    curated_by   TEXT        NOT NULL,                 -- human/Chief who approved the write
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Approximate-NN indexes (HNSW). Tune lists/m/ef at impl against real recall.
CREATE INDEX IF NOT EXISTS repo_chunk_embedding_hnsw
    ON repo_chunk USING hnsw (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS org_context_embedding_hnsw
    ON org_context USING hnsw (embedding vector_cosine_ops);

-- Plain b-tree helpers for filtering before/after vector search.
CREATE INDEX IF NOT EXISTS repo_chunk_repo_idx ON repo_chunk (repo);

-- This file is a STUB for review. It is not migrated by anything yet.
