---
id: TKT-bklg-022
title: "B4 Make the empirica dependency installable with one command"
status: completed
created: 2026-11-14T15:43:40.223Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# B4 Make the empirica dependency installable with one command

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [x] Completed

## Notes

Tags: `R` `agent` `P1`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `pyproject.toml` points `empirica` at the gitignored path `_unified/empirica` (editable), so a fresh `uv sync` cannot find it. AGENTS.md's recipe hardcodes `/workspace/_unified/empirica`. Here I fetched empirica 1.2.3 with `pip3 download --no-binary :all: --no-deps`, extracted it, and copied it to `_unified/empirica`. The sibling `_pyrite` repo has the same trap (`../empirica` and `../NovaSystem-Codex`); its `uv sync` failed here.

**First step.** add `scripts/setup-empirica.sh`, or drop the source override so uv resolves PyPI. Apply the same fix in `_pyrite`.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading B4.

**2026-11-14 (build pass).** The premise was wrong. pyproject.toml has no [tool.uv.sources]; empirica 1.7.1 comes from PyPI through uv.lock and `uv sync --extra dev` works as is. AGENTS.md said otherwise and this backlog repeated it without checking. AGENTS.md is corrected. (_pyrite does have that problem; it is a different repo.)
