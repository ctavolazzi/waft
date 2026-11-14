---
id: TKT-dirn-001
title: "P0.1 Stabilize: land backlog A1 to A3, A6 and A18 so the suite and ruff F821 are clean"
status: completed
created: 2026-11-14T16:24:51.041Z
parent: WE-261114-dirn
labels: ['direction', 'waft']
---

# P0.1 Stabilize: land backlog A1 to A3, A6 and A18 so the suite and ruff F821 are clean

Part of [[WE-261114-dirn_index|WE-261114-dirn]]

## Status

- [x] Completed

## Notes

**How.** Backlog A1, A2, A3, A6, A18.

**Done when** the full suite has no tracing or collection errors and `ruff check src --select F821` reports 0.

Full context: [DIRECTION_AND_REUSE.md](../DIRECTION_AND_REUSE.md).

**2026-11-14 (build pass).** Done. Suite: 850 passed, none failing. ruff F821 over src: clean.
