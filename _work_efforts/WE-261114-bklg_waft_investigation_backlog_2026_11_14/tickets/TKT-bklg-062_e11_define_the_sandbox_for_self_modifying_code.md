---
id: TKT-bklg-062
title: "E11 Define the sandbox for self-modifying code"
status: pending
created: 2026-11-14T15:43:40.226Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# E11 Define the sandbox for self-modifying code

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `Q` `research` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** WAFT is described as self-modifying. Where generated code runs, with what rights, and what limits file and network access is not documented in anything read.

**First step.** document the execution model; add a test that a mutation cannot write outside its working directory. See R3.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading E11.
