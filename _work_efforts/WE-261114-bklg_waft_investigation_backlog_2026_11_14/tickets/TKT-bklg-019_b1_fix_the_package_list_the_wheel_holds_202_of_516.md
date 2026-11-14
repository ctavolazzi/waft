---
id: TKT-bklg-019
title: "B1 Fix the package list: the wheel holds 202 of 516 Python files"
status: pending
created: 2026-11-14T15:43:40.223Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# B1 Fix the package list: the wheel holds 202 of 516 Python files

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P1`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `[tool.setuptools] packages` is a hand-written list of six names (`waft`, `waft.core`, `waft.cli`, `waft.templates`, `waft.ui`, `waft.api`). `uv build --wheel` made a wheel with 202 `.py` files; `find src/waft -name '*.py'` finds 516. Missing: 13 top-level subpackages (`ai_town`, `campaign`, `config`, `dealer`, `evolution`, `fogsift`, `pantheon`, `pet`, `prime_directive`, `rag`, `reports`, `scripts`, `version`) and nested ones inside the listed packages, for example `core/tracing`, `core/agent`, `core/science`, `api/routes` and `ui/streamlit` (each checked absent from the wheel).

**First step.** switch to `[tool.setuptools.packages.find] where = ["src"]`, rebuild, compare file counts, rerun B2.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading B1.
