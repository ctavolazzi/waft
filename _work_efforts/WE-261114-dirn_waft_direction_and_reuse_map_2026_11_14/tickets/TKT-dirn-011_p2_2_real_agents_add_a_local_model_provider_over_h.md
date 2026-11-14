---
id: TKT-dirn-011
title: "P2.2 Real agents: add a local model provider over HTTP behind Door Guy"
status: pending
created: 2026-11-14T16:24:51.042Z
parent: WE-261114-dirn
labels: ['direction', 'waft']
---

# P2.2 Real agents: add a local model provider over HTTP behind Door Guy

Part of [[WE-261114-dirn_index|WE-261114-dirn]]

## Status

- [ ] Not started

## Notes

**How.** Port tavern-keeper-bot `llm.js` (195 lines, 25 passing tests) to httpx with an injectable clock and transport; llama.cpp and Ollama are OpenAI-compatible base URLs. Route every call through `door_guy.py`.

**Done when** the same lab run works with the mock and with a local model, and every model call is a Logbook record.

Full context: [DIRECTION_AND_REUSE.md](../DIRECTION_AND_REUSE.md).

