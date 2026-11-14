---
id: TKT-dirn-004
title: "P0.4 Stabilize: stop the handshake handing out the token and require auth on writes (E16, E2)"
status: pending
created: 2026-11-14T16:24:51.041Z
parent: WE-261114-dirn
labels: ['direction', 'waft']
---

# P0.4 Stabilize: stop the handshake handing out the token and require auth on writes (E16, E2)

Part of [[WE-261114-dirn_index|WE-261114-dirn]]

## Status

- [ ] Not started

## Notes

**How.** Backlog E16, E2, E17.

**Done when** the handshake answers only loopback clients, and a test that walks the OpenAPI schema gets 401 on every write route without a token.

Full context: [DIRECTION_AND_REUSE.md](../DIRECTION_AND_REUSE.md).

