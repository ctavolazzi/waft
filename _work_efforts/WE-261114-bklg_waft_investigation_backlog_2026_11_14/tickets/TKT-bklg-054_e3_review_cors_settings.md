---
id: TKT-bklg-054
title: "E3 Review CORS settings"
status: pending
created: 2026-11-14T15:43:40.225Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# E3 Review CORS settings

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `src/waft/api/main.py:120` sets `allow_origins`; `tests/test_cors.py::test_actual_post_request_with_cors` returns 500 (A1 does not fix it).

**First step.** read the origin list; confirm no wildcard with credentials; fix the 500.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading E3.
