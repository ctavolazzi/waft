---
id: TKT-dirn-006
title: "P1.1 Honest loop: move src/gym/rpg into the package as waft.gym"
status: completed
created: 2026-11-14T16:24:51.041Z
parent: WE-261114-dirn
labels: ['direction', 'waft']
---

# P1.1 Honest loop: move src/gym/rpg into the package as waft.gym

Part of [[WE-261114-dirn_index|WE-261114-dirn]]

## Status

- [x] Completed

## Notes

**How.** Move `src/gym/rpg` to `src/waft/gym` (the top-level name `gym` collides with the PyPI package). Keep its 5 tests.

**Done when** `from waft.gym import GameMaster` works from an installed wheel and the gym tests pass.

Full context: [DIRECTION_AND_REUSE.md](../DIRECTION_AND_REUSE.md).

**2026-11-14 (build pass).** Done. `waft.gym`, with `gym.rpg` kept as an alias. While porting, the gym's judge turned out not to check weights at all; it does now (tests/test_gym_judge.py).
