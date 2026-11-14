---
id: TKT-dirn-013
title: "P2.4 Real agents: add a recorded fake model so tests never touch the network"
status: completed
created: 2026-11-14T16:24:51.042Z
parent: WE-261114-dirn
labels: ['direction', 'waft']
---

# P2.4 Real agents: add a recorded fake model so tests never touch the network

Part of [[WE-261114-dirn_index|WE-261114-dirn]]

## Status

- [x] Completed

## Notes

**How.** Port tavern-keeper-bot's scripted fake server (about 35 lines) as a pytest fixture on port 0, replies chosen by prompt pattern; block non-loopback sockets in `conftest.py` (its end-to-end harness pattern).

**Done when** the whole suite passes with the network blocked.

Full context: [DIRECTION_AND_REUSE.md](../DIRECTION_AND_REUSE.md).

**2026-11-14 (build pass).** Done. A scripted fake model behind the real client (in process and over a real socket); lab tests fail on any connection that is not to this machine.
