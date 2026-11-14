---
id: TKT-bklg-015
title: "A15 Measure coverage over all of src"
status: pending
created: 2026-11-14T15:43:40.223Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# A15 Measure coverage over all of src

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** Measured with `uv run pytest tests/ --cov=src/waft` (same 25 failures, 99 s): total coverage is 16 percent (58,876 statements, 49,697 missed). 258 modules are at 0 percent (32,416 statements). `main.py` alone has 2,400 statements at 0 percent; next are `one_pager.py` 632, `foundation_v2.py` 485, `pyrite.py` 471, `cli/dungeon_cli.py` 404 and `core/pocketbase_scout.py` 380. The test module that would exercise the CLI (`tests/test_commands.py`) does not load (A6).

**First step.** fix A6 and add the smoke test in A19; set a coverage floor at today's 16 percent and ratchet it up; list the 0 percent modules next to the dead-code list (F7).

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading A15.
