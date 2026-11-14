---
id: TKT-bklg-112
title: "J2 List the system programs each command needs"
status: pending
created: 2026-11-14T15:43:40.228Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# J2 List the system programs each command needs

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `Q` `agent` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** Typst, a LaTeX distribution, poppler, cairo and pango are needed by different commands; no check exists.

**First step.** add a `waft doctor`-style check that prints missing programs and which commands need them.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading J2.
