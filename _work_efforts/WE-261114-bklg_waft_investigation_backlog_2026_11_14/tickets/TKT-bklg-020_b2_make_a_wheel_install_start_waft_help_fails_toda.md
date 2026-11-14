---
id: TKT-bklg-020
title: "B2 Make a wheel install start: waft --help fails today"
status: pending
created: 2026-11-14T15:43:40.223Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# B2 Make a wheel install start: waft --help fails today

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P1`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** I built the wheel with `uv build --wheel`, installed it in a clean Python 3.14 venv, and ran `waft --help`. It stops with `ModuleNotFoundError: No module named 'waft.templates.typst'` (`main.py:37` imports `cli/case_render.py`, which imports `..templates.typst.compiler` at line 15). `waft new` and `waft evolve` fail the same way. The README tells users to install from GitHub, which builds a wheel the same way; I did not run that exact command.

**First step.** fix B1, reinstall in a clean venv, run `--help` for each of the 82 commands, and add that as a CI job (C7).

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading B2.
