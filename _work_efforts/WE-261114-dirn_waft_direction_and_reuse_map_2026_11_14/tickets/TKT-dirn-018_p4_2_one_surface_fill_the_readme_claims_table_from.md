---
id: TKT-dirn-018
title: "P4.2 One surface: fill the README claims table from real runs"
status: pending
created: 2026-11-14T16:24:51.042Z
parent: WE-261114-dirn
labels: ['direction', 'waft']
---

# P4.2 One surface: fill the README claims table from real runs

Part of [[WE-261114-dirn_index|WE-261114-dirn]]

## Status

- [ ] Not started

## Notes

**How.** Backlog G2, G3, G10. Patterns: a generated `docs/CLI.md` with a `--check` mode (thecoffeejesus `gen_sitemap.py`), a Python port of johnnyautoseed's copy-rule engine with WAFT's own rules, `voice_audit.py`, survivingthesingularity's verdict words for the claims table, pyrite's obsidian linter for wikilinks.

**Done when** CI fails when a doc names a missing command, and the README claims table says which claims a Logbook run backs.

Full context: [DIRECTION_AND_REUSE.md](../DIRECTION_AND_REUSE.md).

