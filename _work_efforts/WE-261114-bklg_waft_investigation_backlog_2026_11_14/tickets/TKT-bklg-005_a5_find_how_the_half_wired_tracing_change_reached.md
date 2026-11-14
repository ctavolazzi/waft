---
id: TKT-bklg-005
title: "A5 Find how the half-wired tracing change reached main"
status: pending
created: 2026-11-14T15:43:40.222Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# A5 Find how the half-wired tracing change reached main

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `Q` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** branch `claude/add-data-tracing-kB8Nr` exists on GitHub. CI runs only `tests/api` (C1), which may be why a broken `core` change passed. The PR or commit that added the calls was not read.

**First step.** `git log -S"get_tracer" -- src/waft/core`, read the PR, note whether any test ran. Feed the answer to C1.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading A5.
