---
id: TKT-bklg-039
title: "C10 Turn on ruff F821 for all of src in CI"
status: completed
created: 2026-11-14T15:43:40.224Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# C10 Turn on ruff F821 for all of src in CI

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [x] Completed

## Notes

Tags: `M` `agent` `P1`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** the project's ruff config excludes most legacy folders and passes cleanly, yet `--isolated --select F821` finds the missing `get_tracer` and `SpanStatus` names that broke tests, plus 26 more (A18). One cheap rule would have stopped the tracing break.

**First step.** add a CI step `ruff check src --select F821`; fix or baseline the hits.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading C10.

**2026-11-14 (build pass).** The test job runs `ruff check src/waft --isolated --select E9,F63,F7,F82`.
