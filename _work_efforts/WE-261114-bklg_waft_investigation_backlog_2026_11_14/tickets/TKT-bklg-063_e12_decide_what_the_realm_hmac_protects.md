---
id: TKT-bklg-063
title: "E12 Decide what the realm HMAC protects"
status: pending
created: 2026-11-14T15:43:40.226Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# E12 Decide what the realm HMAC protects

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `R` `CT` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** now that `.hmac_key` is out of git it is generated per machine (commit dd1992fd message), so crystallized realm state made on one machine will not verify on another.

**First step.** state the intended trust model: one machine, shared, or signed by an owner key.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading E12.
