---
id: TKT-bklg-083
title: "G3 Build a claims table"
status: pending
created: 2026-11-14T15:43:40.227Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# G3 Build a claims table

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `R` `research` `P1`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** README and `PITCH_DECK` use phrases such as "Don't just build agents. Breed them." and "God-Head". README Core Pillar 1, "The Substrate", says "Agents that write their own Python source code (DNA)"; in the code, `core/substrate.py` is `SubstrateManager`, a wrapper around uv commands (init, sync, add), and no path I read makes an agent write its own source. FogSift FINDINGS (2026-10-25) says the "God-Head" term appears only in documentation and nothing in `src/` or `tests/` measures it.

**First step.** one table: claim, where it is made, the command or test that shows it, the measured result, status.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading G3.
