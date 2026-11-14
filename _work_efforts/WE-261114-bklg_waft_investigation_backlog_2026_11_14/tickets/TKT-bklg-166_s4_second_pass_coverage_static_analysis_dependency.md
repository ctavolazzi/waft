---
id: TKT-bklg-166
title: "S4 Second pass: coverage, static analysis, dependency audit, API probes, ledger mining"
status: completed
created: 2026-11-14T16:06:05.238Z
labels: ['pyrite']
---

# S4 Second pass: coverage, static analysis, dependency audit, API probes, ledger mining

## Description

Evidence and first step are in the Notes below and in INVESTIGATION_BACKLOG.md.

## Status

- [x] Completed

## Notes

Done 2026-11-14, after the request to explore further. Installed analysis tools in a scratch venv; ran coverage, bandit, vulture, radon, deptry, pip-audit and detect-secrets; compiled every tracked Python file; checked Markdown links; ran `waft serve` on a scratch project and probed its write routes; built and tested `visualizer/` in a scratch copy; read the evolution and auth code; mined the 135 existing work efforts. Numbers are in the Baseline table of INVESTIGATION_BACKLOG.md.

Full context: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md).
