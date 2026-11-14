---
id: TKT-bklg-058
title: "E7 Audit dependencies for known vulnerabilities"
status: pending
created: 2026-11-14T15:43:40.225Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# E7 Audit dependencies for known vulnerabilities

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `Q` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** no audit has run. The Python side is pinned by `uv.lock`; the JavaScript side has lockfiles inside tracked `node_modules` trees.

**First step.** `pip-audit` on the lock; `npm audit` in `waft_desktop/electron`, `waft_desktop/frontend`, `typst-webapp/frontend` and `visualizer`; record the Electron version.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading E7.
