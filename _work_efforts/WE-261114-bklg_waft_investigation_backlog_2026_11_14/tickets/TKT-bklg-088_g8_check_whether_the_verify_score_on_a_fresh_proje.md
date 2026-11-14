---
id: TKT-bklg-088
title: "G8 Check whether the verify score on a fresh project is a false alarm"
status: pending
created: 2026-11-14T15:43:40.227Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# G8 Check whether the verify score on a fresh project is a false alarm

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** after `waft new demo`, `waft verify` reports "Project structure has issues" and "Integrity: 90%" because `uv.lock` is missing.

**First step.** make `new` run `uv lock`, or make `verify` treat a missing lock as a hint.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading G8.
