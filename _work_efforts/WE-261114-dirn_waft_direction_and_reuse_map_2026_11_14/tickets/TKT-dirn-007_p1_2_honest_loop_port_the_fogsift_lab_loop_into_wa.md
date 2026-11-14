---
id: TKT-dirn-007
title: "P1.2 Honest loop: port the FogSift lab loop into waft.lab and make waft evolve use it"
status: completed
created: 2026-11-14T16:24:51.041Z
parent: WE-261114-dirn
labels: ['direction', 'waft']
---

# P1.2 Honest loop: port the FogSift lab loop into waft.lab and make waft evolve use it

Part of [[WE-261114-dirn_index|WE-261114-dirn]]

## Status

- [x] Completed

## Notes

**How.** Port `_workbench/fogsift-system/checks/waft_lab.py` (308 lines): genome, content-hash ids, per-call RNG from sha256, mutation, elitist selection, death below 0.5. Add fail-closed scoring (snowy-bridge `check-cameras.js` rule: NaN, missing or empty never wins). `waft evolve` becomes an alias.

**Done when** `waft lab run --seed 7` reproduces today's lab numbers (best 0.88 at generation 0, 0.95 at generation 5 with population 8 and 6 trials) or the difference is explained.

Full context: [DIRECTION_AND_REUSE.md](../DIRECTION_AND_REUSE.md).

**2026-11-14 (build pass).** Done as `waft.lab.engine`. `waft evolve` was kept and now says it runs no task, instead of being aliased. Numbers differ from FogSift's (0.88 to 0.95) on purpose: failed encounters score 0 here, and the judge now rejects bad weights.
