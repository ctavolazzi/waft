---
id: TKT-bklg-141
title: "A19 Add a smoke test for every CLI command"
status: pending
created: 2026-11-14T16:04:24.835Z
labels: ['pyrite']
---

# A19 Add a smoke test for every CLI command

## Description

Evidence and first step are in the Notes below and in INVESTIGATION_BACKLOG.md.

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `src/waft/main.py` has 2,400 statements at 0 percent coverage (A15) and registers 82 commands; the one test module for the CLI, `tests/test_commands.py`, does not load (A6). No test runs `waft <command> --help` for each command.

**First step.** after A6, add one parametrized test that runs `--help` for every command and expects exit code 0; run it against an installed wheel too, which would have caught B2.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading A19.
