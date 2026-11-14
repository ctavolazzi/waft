---
id: TKT-bklg-021
title: "B3 Ship template data files in the wheel"
status: completed
created: 2026-11-14T15:43:40.223Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# B3 Ship template data files in the wheel

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [x] Completed

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** the built wheel has 0 non-Python files under `waft/`; `src/waft/templates` has 14 non-Python files in the tree. `pyproject.toml` has no `package-data`, `include-package-data` or `MANIFEST.in`.

**First step.** declare the data, rebuild, and test `waft new` from the wheel.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading B3.

**2026-11-14 (build pass).** package-data ships json, typ, tex, html, css, js, mjs, md, toml, txt, otf and ttf files (44 data files in the wheel).
