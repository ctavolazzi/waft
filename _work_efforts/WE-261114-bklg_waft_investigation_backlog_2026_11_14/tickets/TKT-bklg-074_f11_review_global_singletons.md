---
id: TKT-bklg-074
title: "F11 Review global singletons"
status: pending
created: 2026-11-14T15:43:40.226Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# F11 Review global singletons

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `R` `agent` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `_global_tracer` in `core/tracing/__init__.py`; the `Pyrite` singleton in `pyrite.py`.

**First step.** check thread and async safety; let tests build their own instances.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading F11.
