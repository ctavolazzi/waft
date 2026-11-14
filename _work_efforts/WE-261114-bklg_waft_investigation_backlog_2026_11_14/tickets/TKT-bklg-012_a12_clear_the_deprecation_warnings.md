---
id: TKT-bklg-012
title: "A12 Clear the deprecation warnings"
status: in_progress
created: 2026-11-14T15:43:40.223Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# A12 Clear the deprecation warnings

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] In progress

## Notes

Tags: `M` `agent` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** 151 warnings in the baseline run and 185 after the import patch. `datetime.utcnow()` appears 140 times in `src` (for example `tracer.py:32` and `storage.py:45`); Pydantic v2 `max_items` and class-based `Config` in `api/schemas/work_efforts.py` (lines 10, 16, 29, 35, 48, 54, 60, 89) and `api/schemas/projects.py`; `api/responses.py:10`.

**First step.** use timezone-aware datetimes, `max_length` and `ConfigDict`, then run with `-W error::DeprecationWarning` in CI.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading A12.

**2026-11-14 (build pass).** The two utcnow() calls in the tracing module are replaced. The other 138 and the Pydantic warnings remain (129 warnings in a full run).
