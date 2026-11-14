---
id: TKT-bklg-045
title: "D6 Design the target layout for the repo root"
status: pending
created: 2026-11-14T15:43:40.224Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# D6 Design the target layout for the repo root

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `R` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** the root held 350 files before the 2026-11-09 archive and 197 after (commit 6419b7c0); `ls` still shows PDFs, zips, scripts, `Bubbles`, `Campaigns`, `NARRATIVE-WAFT`, `PITCH_DECK` and `Obsidian_Archive`.

**First step.** classify each root entry (code, docs, data, art, archive), propose `src/ docs/ examples/ assets/ archive/`, move with `git mv`.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading D6.
