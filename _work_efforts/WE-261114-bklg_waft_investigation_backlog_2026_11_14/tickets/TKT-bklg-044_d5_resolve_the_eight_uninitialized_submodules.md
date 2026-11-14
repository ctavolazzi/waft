---
id: TKT-bklg-044
title: "D5 Resolve the eight uninitialized submodules"
status: pending
created: 2026-11-14T15:43:40.224Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# D5 Resolve the eight uninitialized submodules

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `.gitmodules` lists 8; `git submodule status` shows all 8 with a leading `-` (not checked out). Commit 2836a19b removed 29 orphan submodules earlier.

**First step.** for each: is anything imported or read at runtime? Then init, vendor with a licence note, or remove from `.gitmodules`.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading D5.
