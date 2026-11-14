---
id: TKT-dirn-008
title: "P1.3 Honest loop: record every lab run in a Logbook (waft.record)"
status: pending
created: 2026-11-14T16:24:51.041Z
parent: WE-261114-dirn
labels: ['direction', 'waft']
---

# P1.3 Honest loop: record every lab run in a Logbook (waft.record)

Part of [[WE-261114-dirn_index|WE-261114-dirn]]

## Status

- [ ] Not started

## Notes

**How.** Vendor or depend on `fogsift_api/custody.py` and `schemas.py` (see D1). One run is one chain; print the head. Resolve the project directory by env var, then flag, then git root, never `__file__` (backlog F19; spec in `_workbench` WE-261025-eo0i).

**Done when** `waft lab verify RUN --expect-head HASH` passes, flipping one stored byte makes it fail, and the checkout is unchanged after a run.

Full context: [DIRECTION_AND_REUSE.md](../DIRECTION_AND_REUSE.md).

