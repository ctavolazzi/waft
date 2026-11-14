---
id: TKT-bklg-032
title: "C3 Remove the debug blocks the staging gate greps for"
status: pending
created: 2026-11-14T15:43:40.224Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# C3 Remove the debug blocks the staging gate greps for

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** the gate fails if `src/` contains `# #region agent log` or `debug.log`. Five Python files do: `web.py`, `document_builder.py`, `one_pager.py`, `evolution/document_components.py`, `evolution/golden_triangle.py`.

**First step.** delete the blocks (E5); keep the gate.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading C3.
