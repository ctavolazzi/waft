---
id: TKT-bklg-134
title: "R5 Test determinism of waft evolve"
status: pending
created: 2026-11-14T15:43:40.230Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# R5 Test determinism of waft evolve

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `Q` `research` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** FogSift #234 says the lab is deterministic for a seed; `waft evolve` itself reuses ids and saturates at 100 (F2).

**First step.** run twice with a fixed seed and diff; then with different seeds and look at the spread.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading R5.
