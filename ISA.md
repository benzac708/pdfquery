---
task: Swap ChromaDB → pgvector + proper CI/CD
slug: ccep-pgvector-swap
project: ccep-rag
effort: E4
phase: observe
progress: 0/32
mode: algorithm
started: 2026-05-25T12:45:00Z
---

## Problem

ChromaDB bloat (527MB of unnecessary deps including Kubernetes client, pyarrow, onnxruntime) makes the Docker image 1.27GB, CI/CD painfully slow under QEMU cross-arch builds, and the tech stack doesn't demonstrate the Postgres competency recruiters look for.

## Vision

A sub-500MB Docker image, native ARM64 CI/CD via self-hosted runner, pgvector-backed RAG pipeline that shows enterprise-grade stack choice, and a full pipeline (lint → test → build → push → deploy) that runs in under 5 minutes.

## Out of Scope

- Multi-arch images (we target ARM64 VPS only)
- HA/failover for Postgres
- Migration of existing chroma_db data
- Web-based DB admin UI
- Performance benchmarking

## Principles

- Same artifact from test through prod (via registry)
- Postgres connection via env var, no hardcoded creds
- Zero ChromaDB code survives (clean break)

## Constraints

- ARM64 VPS (Hetzner) — no x86 emulation in production
- GitHub-hosted runner for lint/test (AMD64)
- Self-hosted runner for build + deploy (ARM64)

## Goal

Replace ChromaDB with pgvector in the vectordb module, add Postgres container to docker-compose, reduce image to <500MB, prove the full pipeline works end-to-end with a green GH Actions run.

## Criteria

- [ ] ISC-1: setup.py replaces chromadb with psycopg2-binary
- [ ] ISC-2: config.py has DATABASE_URL env var, no CHROMA_DIR
- [ ] ISC-3: vectordb.py rewritten to use pgvector SQL queries
- [ ] ISC-4: docker-compose.yml has db service (pgvector) + app depends_on db
- [ ] ISC-5: docker-compose volumes use pgdata, not chroma_db
- [ ] ISC-6: Dockerfile builds without chromadb (pip install succeeds)
- [ ] ISC-7: .env.example has DATABASE_URL placeholder
- [ ] ISC-8: AGENTS.md updated with new stack
- [ ] ISC-9: Image built locally on VPS is <500MB
- [ ] ISC-10: `docker-compose up` starts both containers and app connects to db
- [ ] ISC-11: CLI ingest + query works end-to-end on VPS
- [ ] ISC-12: Streamlit app upload → ingest → query works
- [ ] ISC-13: lint job (ruff) added to CI
- [ ] ISC-14: test job uses pytest import check
- [ ] ISC-15: Self-hosted runner registered on VPS
- [ ] ISC-16: docker job runs on self-hosted runner (ARM64 native)
- [ ] ISC-17: Docker build + push to GHCR works from self-hosted runner
- [ ] ISC-18: deploy job pulls from GHCR, restarts
- [ ] ISC-19: Full pipeline green: lint → test → build → push → deploy
- [ ] ISC-20: Anti: image never contains chromadb again
- [ ] ISC-21: Anti: no chroma_db volume in docker-compose
- [ ] ISC-22: Anti: no hardcoded Postgres credentials in code

## Features

| name | satisfies | depends_on | parallelizable |
|------|-----------|------------|---------------|
| F1: pgvector vectordb | ISC-1..3, ISC-20 | — | no |
| F2: docker-compose pgvector | ISC-4..5, ISC-21 | F1 | no |
| F3: env/config updates | ISC-2, ISC-7..8 | — | yes (with F2) |
| F4: build & verify locally | ISC-9..12 | F1..3 | no |
| F5: self-hosted runner | ISC-15 | — | yes |
| F6: CI/CD pipeline rewrite | ISC-13..14, ISC-16..19 | F5 | no |

## Decisions

*(populated during execution)*

## Changelog

*(populated at learn)*

## Verification

*(populated during execute/verify)*
