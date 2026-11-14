---
id: TKT-bklg-165
title: "L9 Unshallow the clone before any history work"
status: pending
created: 2026-11-14T16:06:04.998Z
labels: ['pyrite']
---

# L9 Unshallow the clone before any history work

## Description

Evidence and first step are in the Notes below and in INVESTIGATION_BACKLOG.md.

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `git rev-parse --is-shallow-repository` is `true` here: 86 commits are reachable, from 2026-01-25 to 2026-11-14, while the first work effort is dated 2026-01-04 and GitHub shows 254 workflow runs. History statements in this document (A5, D3, D12, E6, H8) rest on a partial clone.

**First step.** `git fetch --unshallow`, then recheck pack size, commit count and authors, and rerun the history scans.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading L9.
