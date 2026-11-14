---
id: TKT-bklg-067
title: "F4 Resolve the overlapping names pyrite, empirica and fogsift"
status: pending
created: 2026-11-14T15:43:40.226Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# F4 Resolve the overlapping names pyrite, empirica and fogsift

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `CT` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `src/waft/pyrite.py` ("The Steward", 1,139 lines, singleton, locks, "genetic algorithms") shares a name with the separate `_pyrite` toolkit; `src/waft/core/empirica.py` (1,001 lines) sits beside the `empirica` package; `src/waft/fogsift/` sits beside the FogSift system.

**First step.** rename or document each boundary; avoid two different things called pyrite.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading F4.
