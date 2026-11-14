---
id: TKT-bklg-047
title: "D8 Move runtime data out of git"
status: pending
created: 2026-11-14T15:43:40.225Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# D8 Move runtime data out of git

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** 4 tracked `.db` or `.sqlite` files (for example `_pyrite/analytics/sessions.db`) and 162 tracked `.jsonl` files (traces, journals).

**First step.** inspect for personal paths; split fixtures from runtime data; ignore the runtime paths (A10).

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading D8.
