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

**Evidence.** the Dockerfile installs with `pip install .` (ignoring `uv.lock`) and starts `uvicorn src.waft.api.main:app --host 0.0.0.0`, a source-tree path that bypasses the installed package. It has no `USER` line (the container runs as root) and no `HEALTHCHECK`. It was never built: a `docker` binary exists on this machine but my attempt to query it was declined by the permission check, so I did not try. Given B1 the installed wheel is broken, so a container may work only because it imports from the copied `src/`. `docker-compose.yml` publishes `8000:8000` on all host interfaces, mounts the whole checkout writable at `/app` (`./:/app`) and runs uvicorn with `--host 0.0.0.0` (E17).

**First step.** build it in CI; choose one run path; pin the base image; add a health check (`/api/decision/health` exists).

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading B10.
