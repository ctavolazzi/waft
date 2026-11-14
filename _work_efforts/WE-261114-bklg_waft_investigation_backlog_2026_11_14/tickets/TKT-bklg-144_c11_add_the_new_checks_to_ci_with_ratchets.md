---
id: TKT-bklg-144
title: "C11 Add the new checks to CI with ratchets"
status: pending
created: 2026-11-14T16:05:59.694Z
labels: ['pyrite']
---

# C11 Add the new checks to CI with ratchets

## Description

Evidence and first step are in the Notes below and in INVESTIGATION_BACKLOG.md.

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** baselines measured today: coverage 16 percent; bandit 717 issues (7 high); pip-audit 21 vulnerable packages; deptry 83, 21 and 4; vulture 33 at 80 percent confidence; radon 79 functions rank D or worse; ruff F821 31; broken doc links 147 of 273; 4 files that do not compile; 28 write routes that never returned 401 (E2).

**First step.** add each as a job that records the number and fails only if it rises; lower the budget as items close; print the table in the weekly health run (L7).

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading C11.
