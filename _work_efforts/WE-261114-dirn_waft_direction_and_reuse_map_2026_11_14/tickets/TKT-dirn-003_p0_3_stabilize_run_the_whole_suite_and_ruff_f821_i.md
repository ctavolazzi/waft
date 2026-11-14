---
id: TKT-dirn-003
title: "P0.3 Stabilize: run the whole suite and ruff F821 in CI (C1, C10)"
status: in_progress
created: 2026-11-14T16:24:51.041Z
parent: WE-261114-dirn
labels: ['direction', 'waft']
---

# P0.3 Stabilize: run the whole suite and ruff F821 in CI (C1, C10)

Part of [[WE-261114-dirn_index|WE-261114-dirn]]

## Status

- [ ] In progress

## Notes

**How.** Backlog C1, C10, C6. Patterns: survivingthesingularity `build-guard.yml` (test the committed tree, write what it proves), johnnyautoseed gitleaks job, tavern-keeper-bot consistency tests, a ratchet baseline for known breaks.

**Done when** CI runs all of `tests/`, ruff F821 and a secret scan on every push.

Full context: [DIRECTION_AND_REUSE.md](../DIRECTION_AND_REUSE.md).

**2026-11-14 (build pass).** CI runs the whole suite, an undefined-names pass, the lab doctor and a wheel install. No secret scan yet.
