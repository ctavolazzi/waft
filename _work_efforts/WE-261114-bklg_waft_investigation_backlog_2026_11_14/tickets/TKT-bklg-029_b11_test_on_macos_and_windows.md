---
id: TKT-bklg-029
title: "B11 Test on macOS and Windows"
status: pending
created: 2026-11-14T15:43:40.224Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# B11 Test on macOS and Windows

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `Q` `research` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** scripts use bash (`START_EVOLVE_UI.sh`, `scripts/dev-reinstall.sh`), 433 tracked files hold `/Users/ctavolazzi`, and the FogSift reports say nothing has run on macOS. Only Linux was tested here.

**First step.** add a macOS job to CI; list the failures.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading B11.
