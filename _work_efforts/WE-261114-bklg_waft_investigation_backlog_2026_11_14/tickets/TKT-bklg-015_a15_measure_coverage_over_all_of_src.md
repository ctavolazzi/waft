---
id: TKT-bklg-015
title: "A15 Measure coverage over all of src"
status: pending
created: 2026-11-14T15:43:40.223Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# A15 Measure coverage over all of src

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `Q` `agent` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** the only coverage command in the repo is in the staging workflow and, because only `tests/api` runs there, covers little. `src/waft` has 516 Python files and about 174,000 lines.

**First step.** `uv run pytest --cov=src --cov-report=term-missing` on the fixed baseline; list modules at 0 percent; they are dead-code candidates (F7).

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading A15.
