---
id: TKT-bklg-023
title: "B5 Test WAFT against current Empirica"
status: pending
created: 2026-11-14T15:43:40.223Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# B5 Test WAFT against current Empirica

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `research` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** WAFT requires `empirica>=1.2.3` and ran here against 1.2.3 (local). A clean venv resolved `empirica` 1.16.3 from PyPI on 2026-11-14; FogSift FINDINGS recorded 1.14.14 on 2026-10-25 and a fork at 1.12.33. `src/waft/core/empirica.py` is 1,001 lines, and the `waft empirica`, `finding`, `unknown`, `goal` and `session` commands depend on it.

**First step.** in a throwaway venv with 1.16.3, run the `test_empirica_*.py` files and the Empirica commands; list API breaks; pin a tested range.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading B5.
