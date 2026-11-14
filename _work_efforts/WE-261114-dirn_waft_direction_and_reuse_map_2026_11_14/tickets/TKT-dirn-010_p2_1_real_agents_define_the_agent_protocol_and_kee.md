---
id: TKT-dirn-010
title: "P2.1 Real agents: define the agent protocol and keep the deterministic mock"
status: pending
created: 2026-11-14T16:24:51.041Z
parent: WE-261114-dirn
labels: ['direction', 'waft']
---

# P2.1 Real agents: define the agent protocol and keep the deterministic mock

Part of [[WE-261114-dirn_index|WE-261114-dirn]]

## Status

- [ ] Not started

## Notes

**How.** `Agent = Callable[[str], str]` plus metadata (name, model, cost). Keep the deterministic mock from the lab loop. Port tavern-keeper-bot's loose JSON parser (about 20 lines).

**Done when** the gym runs unchanged with the protocol and the mock.

Full context: [DIRECTION_AND_REUSE.md](../DIRECTION_AND_REUSE.md).

