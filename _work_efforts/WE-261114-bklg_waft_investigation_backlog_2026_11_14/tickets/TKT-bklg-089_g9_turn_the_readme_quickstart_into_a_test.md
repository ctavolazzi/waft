---
id: TKT-bklg-089
title: "G9 Turn the README quickstart into a test"
status: pending
created: 2026-11-14T15:43:40.227Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# G9 Turn the README quickstart into a test

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `waft new`, `waft verify` and `waft evolve` ran end to end here from a scratch directory (see F2, G8, F14 for what they showed).

**First step.** a CI job that runs the quickstart in a temp directory and fails on a non-zero exit.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading G9.
