---
id: TKT-bklg-028
title: "B10 Build and run the Dockerfile"
status: pending
created: 2026-11-14T15:43:40.224Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# B10 Build and run the Dockerfile

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `R` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** the Dockerfile installs with `pip install .` (ignoring `uv.lock`) and starts `uvicorn src.waft.api.main:app`, a source-tree path that bypasses the installed package. No Docker here, so it was never built. Given B1, the installed wheel is broken, so the container may work only because it imports from the copied `src/`.

**First step.** build it in CI; choose one run path; pin the base image; add a health check (`/api/decision/health` exists).

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading B10.
