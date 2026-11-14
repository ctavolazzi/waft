---
id: TKT-bklg-001
title: "A1 Add the missing get_tracer imports in two core modules"
status: pending
created: 2026-11-14T15:43:40.222Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# A1 Add the missing get_tracer imports in two core modules

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P1`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `src/waft/core/input_transformer.py:41` and `src/waft/core/decision_matrix.py:112` call `get_tracer()` and import nothing for it. Adding `from .tracing import get_tracer` to both (temporary edit, reverted) took the suite from 25 failed and 516 passed to 15 failed and 526 passed.

**First step.** apply the import for real, with a test that imports both modules and calls each once.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading A1.
