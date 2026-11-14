---
id: TKT-bklg-123
title: "L2 Fix the stop-hook conflict"
status: completed
created: 2026-11-14T15:43:40.229Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# L2 Fix the stop-hook conflict

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [x] Completed

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** this session's stop hook asked to commit untracked files, so a generated trace file went into commit 4ad0eee1.

**First step.** either make the hook ignore generated paths, or fix A10 so the file never lands in the repo.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading L2.

**2026-11-14 (build pass).** Fixed at the source: tests no longer create files in the tracked tree, so the hook has nothing to commit.
