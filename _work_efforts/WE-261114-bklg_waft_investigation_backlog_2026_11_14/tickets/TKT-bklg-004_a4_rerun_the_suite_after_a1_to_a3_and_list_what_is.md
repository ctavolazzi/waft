---
id: TKT-bklg-004
title: "A4 Rerun the suite after A1 to A3 and list what is still red"
status: completed
created: 2026-11-14T15:43:40.222Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# A4 Rerun the suite after A1 to A3 and list what is still red

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [x] Completed

## Notes

Tags: `M` `agent` `P1`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** after A1 alone, `test_cors.py::test_actual_post_request_with_cors` still returns 500 and the six PDF tests still fail. The three `test_api.py` analyze tests were red before A1; their state after A1 was not read one by one.

**First step.** fix A1 to A3, rerun the command in AGENTS.md, write the new baseline into this ticket.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading A4.

**2026-11-14 (build pass).** Rerun on the fixed tree: 850 passed, 23 skipped, 8 xfailed, 1 xpassed, none failing (Python 3.14.3).
