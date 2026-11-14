---
id: TKT-dirn-012
title: "P2.3 Real agents: add hosted providers behind a flag with a fallback chain and a budget"
status: completed
created: 2026-11-14T16:24:51.042Z
parent: WE-261114-dirn
labels: ['direction', 'waft']
---

# P2.3 Real agents: add hosted providers behind a flag with a fallback chain and a budget

Part of [[WE-261114-dirn_index|WE-261114-dirn]]

## Status

- [x] Completed

## Notes

**How.** Same client: ordered providers, cooldowns, Retry-After, failover on empty replies; add tavern-keeper-bot's rate limiter (about 17 lines) as a call budget. Hosted providers only behind an explicit flag and a key.

**Done when** a run stops cleanly when its budget is spent and records the spend.

Full context: [DIRECTION_AND_REUSE.md](../DIRECTION_AND_REUSE.md).

**2026-11-14 (build pass).** Done. Up to five providers in order, cooldowns, Retry-After, failover on empty replies, a call budget. A spent budget ends the run at its last full generation and the record says so.
