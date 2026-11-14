---
id: TKT-bklg-011
title: "A11 Find why uv rewrites uv.lock on every run"
status: completed
created: 2026-11-14T15:43:40.223Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# A11 Find why uv rewrites uv.lock on every run

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [x] Completed

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** after `uv sync` and after several `uv run` calls, `git status` showed `M uv.lock` each time; I reverted it each time. Suspects: the local `empirica` path source (B4) or a lock that is out of date. The diff was not read.

**First step.** `git diff uv.lock` after one run; commit a lock that stays stable.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading A11.

**2026-11-14 (build pass).** Cause: the lock was written by an older uv, and a newer uv simplifies the markers on every run. Re-locked with uv 0.11.32; uv run no longer changes it, and CI pins that uv version.
