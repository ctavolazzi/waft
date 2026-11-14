---
id: TKT-dirn-011
title: "P2.2 Real agents: add a local model provider over HTTP behind Door Guy"
status: in_progress
created: 2026-11-14T16:24:51.042Z
parent: WE-261114-dirn
labels: ['direction', 'waft']
---

# P2.2 Real agents: add a local model provider over HTTP behind Door Guy

Part of [[WE-261114-dirn_index|WE-261114-dirn]]

## Status

- [ ] In progress

## Notes

**How.** Port tavern-keeper-bot `llm.js` (195 lines, 25 passing tests) to httpx with an injectable clock and transport; llama.cpp and Ollama are OpenAI-compatible base URLs. Route every call through `door_guy.py`.

**Done when** the same lab run works with the mock and with a local model, and every model call is a Logbook record.

Full context: [DIRECTION_AND_REUSE.md](../DIRECTION_AND_REUSE.md).

**2026-11-14 (build pass).** The model path is tested over real HTTP against the scripted server, and provider addresses pass the Door Guy. It has not been run against a real local model (none is reachable from the container this was built in). Model calls are tallied in the record, not stored one by one.
