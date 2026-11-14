---
id: TKT-dirn-005
title: "P0.5 Stabilize: upgrade the fixable vulnerable dependencies (E7)"
status: completed
created: 2026-11-14T16:24:51.041Z
parent: WE-261114-dirn
labels: ['direction', 'waft']
---

# P0.5 Stabilize: upgrade the fixable vulnerable dependencies (E7)

Part of [[WE-261114-dirn_index|WE-261114-dirn]]

## Status

- [x] Completed

## Notes

**How.** Backlog E7. Copy johnnyautoseed's `dependabot.yml` for pip and Actions.

**Done when** pip-audit reports only advisories with no fixed version, each noted with a reason.

Full context: [DIRECTION_AND_REUSE.md](../DIRECTION_AND_REUSE.md).

**2026-11-14 (build pass).** Done. pip-audit on the dev lock: no known vulnerabilities.
