---
id: TKT-bklg-122
title: "L1 Choose the branch policy"
status: pending
created: 2026-11-14T15:43:40.229Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# L1 Choose the branch policy

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `R` `CT` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** branches `main` and `dev` (and maybe `staging`); recent history shows direct pushes to `main` with green CI. CT's `_workbench` rule: commits go on branches that then get merged.

**First step.** write the policy; enable branch protection on `main`.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading L1.
