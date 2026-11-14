---
id: TKT-dirn-009
title: "P1.4 Honest loop: test that the same seed gives the same head hash and ids are unique"
status: pending
created: 2026-11-14T16:24:51.041Z
parent: WE-261114-dirn
labels: ['direction', 'waft']
---

# P1.4 Honest loop: test that the same seed gives the same head hash and ids are unique

Part of [[WE-261114-dirn_index|WE-261114-dirn]]

## Status

- [ ] Not started

## Notes

**How.** Patterns: snowy-bridge determinism check (in order, shuffled, repeated, fresh process), its forbidden-pattern scan as an `ast` check, pyrite's negative controls.

**Done when** same seed gives the same head hash, a different seed a different one, N variants have N ids, a no-op agent scores 0 and a known-bad agent scores below the mock.

Full context: [DIRECTION_AND_REUSE.md](../DIRECTION_AND_REUSE.md).

