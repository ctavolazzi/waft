---
id: TKT-bklg-036
title: "C7 Build and smoke-test the artifacts in CI"
status: in_progress
created: 2026-11-14T15:43:40.224Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# C7 Build and smoke-test the artifacts in CI

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] In progress

## Notes

Tags: `Q` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** nothing in CI builds the wheel (B1), the image (B10), `visualizer/` or `waft_desktop/`.

**First step.** add a job per artifact you keep: build, install in a clean env, run `--help`; remove artifacts nobody builds.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading C7.

**2026-11-14 (build pass).** The wheel is built and used in CI. The Docker image, the visualizer and the desktop app are not.
