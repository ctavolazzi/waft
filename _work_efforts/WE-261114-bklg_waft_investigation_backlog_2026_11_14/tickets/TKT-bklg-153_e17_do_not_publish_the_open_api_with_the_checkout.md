---
id: TKT-bklg-153
title: "E17 Do not publish the open API with the checkout mounted writable"
status: pending
created: 2026-11-14T16:06:01.964Z
labels: ['pyrite']
---

# E17 Do not publish the open API with the checkout mounted writable

## Description

Evidence and first step are in the Notes below and in INVESTIGATION_BACKLOG.md.

## Status

- [ ] Not started

## Notes

Tags: `R` `agent` `P1`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `docker-compose.yml` publishes the API on `8000:8000` (every host interface), bind-mounts `./` at `/app` and sets `WAFT_PROJECT_PATH: /app`; the container runs as root (B10). Combined with E16 (the handshake returns the token), E2 (28 write routes need no token) and F19 (routes write relative to the code), a client on the network could create files in the mounted checkout. This follows from the configuration and my local probes; I did not run the container.

**First step.** publish on `127.0.0.1:8000:8000` by default; mount a separate data directory instead of the repo; fix E16 and E2 first; add a `USER` and a `HEALTHCHECK`.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading E17.
