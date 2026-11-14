---
id: TKT-bklg-167
title: "A20 Quest files say rewards but the gym reads loot_table, so no XP is ever awarded"
status: pending
created: 2026-11-14T19:38:37.725Z
labels: ['pyrite']
---

# A20 Quest files say rewards but the gym reads loot_table, so no XP is ever awarded

## Description

Found during the build pass of 2026-11-14.

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P3`

**Evidence.** `src/waft/gym/dungeons/waft_temple.json` gives each quest a `rewards` key; `Quest` in `src/waft/gym/models.py` has `loot_table` (default `{"xp": 0}`) and `GameMaster` reads `quest.loot_table.get("xp", 0)`. Found while reading the gym for the lab.

**First step.** Rename the key in the JSON or accept both in the model; add a test that a won quest awards its XP.

Found during the build pass; see `BUILD_LOG_2026-11-14.md` in WE-261114-dirn.
