---
id: TKT-bklg-066
title: "F3 Find out what \"evolution\" operates on"
status: pending
created: 2026-11-14T15:43:40.226Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# F3 Find out what "evolution" operates on

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `R` `research` `P1`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `core/evolution_engine.py` imports `hashlib`, `random` and `json`; model-provider names appear in few files (anthropic 2, openai 3, ollama 5, gemini 3 files). The fitness measure is "Scint detection". Nothing read shows a model being called by `evolve`.

**First step.** write one page: genome fields, mutation operators, fitness function, what a Being does. If no model runs, say so in the README.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading F3.
