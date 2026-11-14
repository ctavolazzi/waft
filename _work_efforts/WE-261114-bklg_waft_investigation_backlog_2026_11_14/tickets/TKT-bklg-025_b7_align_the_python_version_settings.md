---
id: TKT-bklg-025
title: "B7 Align the Python version settings"
status: pending
created: 2026-11-14T15:43:40.223Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# B7 Align the Python version settings

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `.python-version` says 3.14.3; CI uses 3.12; `requires-python` is `>=3.12`; classifiers list only 3.12; ruff `target-version` is `py310`; `__pycache__` folders from Python 3.14 sit in the tree.

**First step.** choose a supported range, set all five to it, test both ends (A17).

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading B7.
