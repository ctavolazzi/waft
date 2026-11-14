---
id: TKT-bklg-156
title: "F19 Resolve project paths from the project, not from __file__"
status: in_progress
created: 2026-11-14T16:06:02.739Z
labels: ['pyrite']
---

# F19 Resolve project paths from the project, not from __file__

## Description

Evidence and first step are in the Notes below and in INVESTIGATION_BACKLOG.md.

## Status

- [ ] In progress

## Notes

Tags: `M` `agent` `P1`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** 27 files in `src` derive a root with `Path(__file__)` and three or more `.parent` calls, among them `api/routes/pet.py:14` and the `being`, `protocel`, `storyteller` and `gym` routes. Measured: with `waft serve` running from a scratch directory, an unauthenticated `POST /api/pet/feed` created `_realms/waft_pet/pets/being_20261114_155231_796fa38d.json` inside this checkout (I moved the file out). In a wheel install the same code would write into site-packages. 20 `sys.path.insert` or `append` calls in 19 files add `src` to the path the same way. This is the likely cause of F14.

**First step.** use `app.state.project_path` (it exists in `api/main.py`) or the CLI's `--path`; delete the `sys.path` edits; add a test that runs the API in a temp project and asserts the checkout stays clean.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading F19.

**2026-11-14 (build pass).** The lab writes only where it is told. The API routes that derive paths from __file__ are unchanged.
