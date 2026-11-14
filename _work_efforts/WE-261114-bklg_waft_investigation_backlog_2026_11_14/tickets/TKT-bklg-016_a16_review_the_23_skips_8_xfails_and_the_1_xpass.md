---
id: TKT-bklg-016
title: "A16 Review the 23 skips, 8 xfails and the 1 xpass"
status: pending
created: 2026-11-14T15:43:40.223Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# A16 Review the 23 skips, 8 xfails and the 1 xpass

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** the baseline run ends with `23 skipped, 8 xfailed, 1 xpassed`. The reasons were not read.

**First step.** `pytest -rsx` to print each reason; remove the xfail marker on the xpass; turn long-term skips into tickets.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading A16.
