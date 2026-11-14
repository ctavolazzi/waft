---
id: TKT-bklg-031
title: "C2 Find out whether the staging gate can ever run"
status: pending
created: 2026-11-14T15:43:40.224Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# C2 Find out whether the staging gate can ever run

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `R` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `staging-promotion.yml` has a `head:` key under `pull_request` (not a documented filter) and an `if` on `github.head_ref == 'staging'`. The one PR run recorded (run 70, 2026-07-26) concluded `skipped`. The first page of the branch list (50 names) has no `staging` branch; later pages were not read.

**First step.** list all branches; if there is no staging branch, delete the workflow or create the branch; test with a dummy PR.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading C2.
