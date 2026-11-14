---
id: TKT-dirn-002
title: "P0.2 Stabilize: fix the package list (B1 to B3) and prove a wheel install runs waft --help"
status: pending
created: 2026-11-14T16:24:51.041Z
parent: WE-261114-dirn
labels: ['direction', 'waft']
---

# P0.2 Stabilize: fix the package list (B1 to B3) and prove a wheel install runs waft --help

Part of [[WE-261114-dirn_index|WE-261114-dirn]]

## Status

- [ ] Not started

## Notes

**How.** Backlog B1, B2, B3. Use `[tool.setuptools.packages.find]`; switch the 31 files that import `src.waft` to `waft`. Pattern: pyrite's clean-install validation idea (install outside the checkout, run from a temp directory).

**Done when** a wheel built in CI installs in a clean venv and `waft --help` exits 0 from a temp directory.

Full context: [DIRECTION_AND_REUSE.md](../DIRECTION_AND_REUSE.md).

