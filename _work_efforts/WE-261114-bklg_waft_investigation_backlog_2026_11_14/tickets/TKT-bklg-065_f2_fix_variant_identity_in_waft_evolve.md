---
id: TKT-bklg-065
title: "F2 Fix variant identity in waft evolve"
status: pending
created: 2026-11-14T15:43:40.226Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# F2 Fix variant identity in waft evolve

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P1`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `waft evolve --generations 2 --variants 3` printed one id three times (`being_20261114_153322_37e1e692`), then `fitness=100.00, scints=0` for each, "Fitness improvement: +0.00" and a total time of 0.01 s. With identical variants and a saturated score, selection chooses between copies. FogSift gap #44 records the same id defect.

**First step.** read the spawn code in `core/evolution_engine.py`; make ids unique; add a test that N variants have N ids; see F3.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading F2.
