---
id: TKT-bklg-018
title: "A18 Fix the 31 undefined names that ruff finds"
status: pending
created: 2026-11-14T15:43:40.223Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# A18 Fix the 31 undefined names that ruff finds

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P1`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `ruff check src --isolated --select F821` reports 31 undefined names. Besides the five tracing hits (A1, A3): `main.py` lines 3101 to 3128 use `project_path` six times; `pdf.py:861` and `:891` use `os`; `web.py:498` and `:528` call `_notify_clients`; `being.py:1028` uses `dnd_stats`; `cli/pyrite_cli.py:121` and `:194` call `get_pyrite_instance`; `ui/streamlit/being_integration.py:197` uses `project_path`; and `Being`, `Mission`, `ArrowOfIntent`, `BaseAgent`, `StoryState`, `Event` appear in 12 more places (some may be annotation-only).

**First step.** read each site and separate real NameErrors from annotations; fix; then turn the rule on in CI (C10).

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading A18.
