---
id: TKT-bklg-072
title: "F9 Shrink the ruff exclusion list"
status: pending
created: 2026-11-14T15:43:40.226Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# F9 Shrink the ruff exclusion list

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** ruff reports nothing with the project's config, which excludes `src/gym`, root `*.py` and many underscore folders. `ruff check src --isolated --line-length 100` (default rules) reports 268 findings, 128 auto-fixable: F401 unused import 99, F541 55, F821 undefined name 31, E722 bare except 21, E402 19, F841 14, E741 12, E701 11, F811 4, E731 2.

**First step.** remove one exclusion at a time, fix, commit; start with F821 (A18, C10).

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading F9.
