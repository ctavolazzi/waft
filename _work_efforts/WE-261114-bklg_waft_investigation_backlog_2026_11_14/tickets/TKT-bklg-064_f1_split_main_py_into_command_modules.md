---
id: TKT-bklg-064
title: "F1 Split main.py into command modules"
status: pending
created: 2026-11-14T15:43:40.226Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# F1 Split main.py into command modules

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `src/waft/main.py` is 4,918 lines and registers 82 top-level commands (`waft --help`); `src/waft/cli/` already holds 16 modules. `src/waft` totals about 174,000 lines in 516 files.

**First step.** move command groups into `cli/`, keep `main.py` as wiring, do it behind the existing tests.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading F1.
