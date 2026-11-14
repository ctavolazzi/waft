---
id: TKT-bklg-073
title: "F10 Measure type-check errors"
status: pending
created: 2026-11-14T15:43:40.226Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# F10 Measure type-check errors

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `Q` `agent` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** no mypy or pyright configuration exists.

**First step.** run pyright on `src/waft/core` and `src/waft/api`; set a ratchet so the count never rises.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading F10.
