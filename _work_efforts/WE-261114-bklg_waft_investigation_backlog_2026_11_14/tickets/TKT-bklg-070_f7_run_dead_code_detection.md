---
id: TKT-bklg-070
title: "F7 Run dead-code detection"
status: pending
created: 2026-11-14T15:43:40.226Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# F7 Run dead-code detection

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** vulture on `src`: 33 findings at 80 percent confidence or higher (for example unused variables at `cli/banner.py:378` and `core/alignment.py:46`) and 1,433 at 60 percent or higher; many of the second group will be CLI and API entry points that vulture cannot see.

**First step.** triage the 33; intersect the 60 percent list with the 0 percent coverage modules (A15); archive what both agree on, with CT's approval.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading F7.
