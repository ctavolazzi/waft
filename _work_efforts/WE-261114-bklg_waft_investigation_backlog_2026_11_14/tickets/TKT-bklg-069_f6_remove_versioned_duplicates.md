---
id: TKT-bklg-069
title: "F6 Remove versioned duplicates"
status: pending
created: 2026-11-14T15:43:40.226Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# F6 Remove versioned duplicates

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `foundation.py` and `foundation_v2.py`; `karma.py`, `karma_system.py`, `karma_market.py`, `karma_collector.py`; two `generate_lightcone_docs` variants.

**First step.** build an import graph; delete or archive what nothing imports (with CT's approval).

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading F6.
