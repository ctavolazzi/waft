---
id: TKT-bklg-146
title: "D14 Remove duplicate files from the working tree"
status: pending
created: 2026-11-14T16:06:00.161Z
labels: ['pyrite']
---

# D14 Remove duplicate files from the working tree

## Description

Evidence and first step are in the Notes below and in INVESTIGATION_BACKLOG.md.

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** 2,969 file contents are tracked under more than one path: 5,336 extra copies, about 382 MiB in the working tree (git stores each content once, so the pack grows less). Largest: an esbuild binary in `typst-webapp/frontend/node_modules` (29.4 MiB, 4 copies) and the `_archive/daily/2026-01-13/WAFT_GAME_RULES_*.pdf` files (5.9 MiB, 5 copies each).

**First step.** after D1 most copies disappear; then dedupe what is left or keep one and link.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading D14.
