---
id: TKT-bklg-046
title: "D7 Untrack tool state"
status: pending
created: 2026-11-14T15:43:40.224Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# D7 Untrack tool state

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** tracked: `.cursor` 171 files (1.4 MiB: 138 slash commands, 10 plans, 8 procedures, 4 continuation prompts, 1 skill), `.empirica` 12 files (1.6 MiB, including a SQLite database and its WAL and SHM files), `.empirica_reflex_logs` 12 (named in `.gitignore` but tracked earlier), `.playwright-mcp` 3 screenshots from 2026-01-26, `.obsidian` 5, `.waft/ollama_runtime.jsonl` (10 lines of prompts and responses). The sibling book repo had the same Empirica problem (FogSift FINDINGS item 2).

**First step.** read the contents for sensitive reasoning or paths; `git rm --cached`; extend `.gitignore`.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading D7.
