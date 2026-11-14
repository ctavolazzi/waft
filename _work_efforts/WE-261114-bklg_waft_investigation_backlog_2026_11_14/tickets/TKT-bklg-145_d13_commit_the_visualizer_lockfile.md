---
id: TKT-bklg-145
title: "D13 Commit the visualizer lockfile"
status: pending
created: 2026-11-14T16:05:59.938Z
labels: ['pyrite']
---

# D13 Commit the visualizer lockfile

## Description

Evidence and first step are in the Notes below and in INVESTIGATION_BACKLOG.md.

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `.gitignore` lists `visualizer/package-lock.json`, so `npm ci` cannot be used and each install resolves fresh. A clean `npm install` in a scratch copy took 28 s for 374 packages and printed deprecation warnings (`inflight`, `rimraf` 2, `glob` 7). The build succeeded.

**First step.** remove the ignore line, commit the lockfile, switch docs and CI to `npm ci`.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading D13.
