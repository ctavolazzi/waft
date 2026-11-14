---
id: TKT-bklg-081
title: "G1 Make one index for the 3,680 Markdown files"
status: pending
created: 2026-11-14T15:43:40.227Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# G1 Make one index for the 3,680 Markdown files

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `git ls-files '*.md'` minus `node_modules` gives 3,680 files. Nothing says which are current. `docs/` is 3.8 MB and `_work_efforts` is 276 MB on disk.

**First step.** write `docs/INDEX.md` (current, historical, generated); archive the rest with a README, as `_archive/root-2026-11-09/` does.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading G1.
