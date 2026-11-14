---
id: TKT-bklg-048
title: "D9 Remove hardcoded /Users/ctavolazzi paths"
status: pending
created: 2026-11-14T15:43:40.225Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# D9 Remove hardcoded /Users/ctavolazzi paths

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `git grep -I -l '/Users/ctavolazzi'` outside `node_modules` finds 433 files; `src` has 30 lines in 6 Python files (for example `web.py:28` writes a debug log there).

**First step.** replace with config or `Path(__file__)`-relative paths in `src`; leave historical docs.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading D9.
