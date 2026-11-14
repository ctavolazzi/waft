---
id: TKT-bklg-007
title: "A7 Decide the fate of the three test files that fail at collection"
status: pending
created: 2026-11-14T15:43:40.222Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# A7 Decide the fate of the three test files that fail at collection

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `R` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** AGENTS.md says `test_foundation.py`, `test_full_system.py` and `test_the_absolute_begeesus.py` have module-level code that fails and must be passed to `--ignore`. I did not run them.

**First step.** for each: fix it, turn it into a script under `scripts/`, or move it to `_to_delete/` for CT's approval.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading A7.
