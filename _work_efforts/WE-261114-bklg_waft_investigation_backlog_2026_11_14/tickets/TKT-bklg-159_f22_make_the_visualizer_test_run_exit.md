---
id: TKT-bklg-159
title: "F22 Make the visualizer test run exit"
status: pending
created: 2026-11-14T16:06:03.535Z
labels: ['pyrite']
---

# F22 Make the visualizer test run exit

## Description

Evidence and first step are in the Notes below and in INVESTIGATION_BACKLOG.md.

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** in a scratch copy of `visualizer/`, `npm test` ran 3 test files (34 tests, all passing: 1, 17 and 16) but the `vitest run` process did not exit within 9 minutes and I killed it. The build printed 20 warnings, among them A11y warnings in `routes/projects/+page.svelte` and `routes/mission-control/+page.svelte` and a missing `.svelte-kit/tsconfig.json` base config (`svelte-kit sync` has not run).

**First step.** find the open handle (an interval, a server or a watcher started by the experiment runner test) and close it; fix the warnings.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading F22.
