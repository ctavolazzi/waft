---
id: TKT-bklg-155
title: "F18 Fix or archive the four tracked Python files that do not compile"
status: pending
created: 2026-11-14T16:06:02.468Z
labels: ['pyrite']
---

# F18 Fix or archive the four tracked Python files that do not compile

## Description

Evidence and first step are in the Notes below and in INVESTIGATION_BACKLOG.md.

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** compiling the 1,109 tracked `.py` files outside `node_modules` found 4 syntax errors: `_temp/template_function.py:94` (f-string), `demo_output/scripts/script.py:3` and `demo_output/scripts/test.py:3` (leading zeros in a decimal literal) and `scripts/generate_tavern_game_with_skills.py:580` (invalid decimal literal).

**First step.** fix them or move them to `_to_delete/` for CT's approval; add a compile check for tracked Python to CI (C11).

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading F18.
