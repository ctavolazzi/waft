---
id: TKT-bklg-006
title: "A6 Add the CliRunner import to tests/test_commands.py"
status: pending
created: 2026-11-14T15:43:40.222Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# A6 Add the CliRunner import to tests/test_commands.py

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** line 11 is `runner = CliRunner()`; the imports above it do not include `typer.testing.CliRunner`. The file fails at collection with NameError and stops a plain `pytest tests/` run.

**First step.** add the import, then see how many of that file's tests pass.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading A6.
