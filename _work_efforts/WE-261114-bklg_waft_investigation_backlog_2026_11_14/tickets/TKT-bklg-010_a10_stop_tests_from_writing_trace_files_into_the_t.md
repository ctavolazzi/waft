---
id: TKT-bklg-010
title: "A10 Stop tests from writing trace files into the tracked tree"
status: completed
created: 2026-11-14T15:43:40.223Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# A10 Stop tests from writing trace files into the tracked tree

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [x] Completed

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `TraceStorage` defaults to `Path.cwd() / "_pyrite" / "analytics" / "traces"` (`core/tracing/storage.py:25`). Each test run created or changed `_pyrite/analytics/traces/2026-11-14.jsonl`, a tracked path. Commit 4ad0eee1 on this branch contains that file because a stop hook asked for untracked files to be committed.

**First step.** point storage at a tmp dir in `tests/conftest.py`, offer an env var for the trace dir, and untrack the file (D8).

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading A10.

**2026-11-14 (build pass).** WAFT_TRACE_DIR and WAFT_TRACING control where spans go; tests/conftest.py sends them to a temp folder. A full run leaves git status empty. The trace file committed earlier is still tracked (D8).
