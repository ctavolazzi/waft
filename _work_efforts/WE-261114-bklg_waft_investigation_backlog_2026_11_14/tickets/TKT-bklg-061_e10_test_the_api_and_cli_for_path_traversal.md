---
id: TKT-bklg-061
title: "E10 Test the API and CLI for path traversal"
status: pending
created: 2026-11-14T15:43:40.225Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# E10 Test the API and CLI for path traversal

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `Q` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** routes in `work_efforts` and `projects`, and the CLI, accept a project path and write files. `../` and absolute paths outside the project were not tried.

**First step.** add tests that send such paths and expect 400 or 403.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading E10.
