---
id: TKT-bklg-124
title: "L3 Add pre-commit checks"
status: pending
created: 2026-11-14T15:43:40.229Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# L3 Add pre-commit checks

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `R` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** no `.pre-commit-config.yaml` at the root.

**First step.** ruff, a 5 MiB file guard, gitleaks, a ban on `/Users/` paths, and a ban on em and en dashes in Markdown.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading L3.
