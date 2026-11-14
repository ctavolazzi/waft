---
id: TKT-bklg-051
title: "D12 Decide whether to rewrite history"
status: pending
created: 2026-11-14T15:43:40.225Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# D12 Decide whether to rewrite history

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `R` `CT` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** old commits still hold the Pexels and Pixabay keys and the API token (rotated 2026-11-09 per commit 67ce2ed8) and the two crypto keys (E1). `_workbench` ticket 8.4 says leave history. A rewrite would also shrink the 687 MiB pack but breaks every clone and open branch.

**First step.** CT decides; if yes, plan `git filter-repo` with a backup and a branch freeze.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading D12.
