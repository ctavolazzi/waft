---
id: TKT-bklg-142
title: "B12 Remove the experiment folders from the uv workspace"
status: pending
created: 2026-11-14T16:05:59.234Z
labels: ['pyrite']
---

# B12 Remove the experiment folders from the uv workspace

## Description

Evidence and first step are in the Notes below and in INVESTIGATION_BACKLOG.md.

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `pyproject.toml` has a `[tool.uv.workspace]` with five members: `_experiments/test_project_001`, `_experiments/existing_project`, `_experiments/test_project_002`, `_experiments/test_project_001/nested_project` and `narcissus_lab/internal_monologue`. Every uv command prints a deprecation warning about `tool.uv.dev-dependencies` in `narcissus_lab/internal_monologue/pyproject.toml`. The members' dependencies resolve into the root `uv.lock`, a likely cause of A11.

**First step.** drop the experiment members, fix or move the deprecated field, re-lock, and check that `uv.lock` stays stable (A11).

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading B12.
