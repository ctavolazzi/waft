---
id: TKT-bklg-157
title: "F20 Refactor the most complex functions"
status: pending
created: 2026-11-14T16:06:03.000Z
labels: ['pyrite']
---

# F20 Refactor the most complex functions

## Description

Evidence and first step are in the Notes below and in INVESTIGATION_BACKLOG.md.

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `radon cc src`: 79 functions rank D or worse and 18 blocks rank F (complexity over 40). Worst: `generate_typst_from_parsed_data` in `cli/case_render.py` (100), `Visualizer.analyze` in `core/visualizer.py` (78), `CritiqueResponseManager._generate_response_report` in `core/critique_response.py` (58), `render_town_view` in `ui/streamlit/town_view.py` (56), `GameMaster.start_encounter` in `src/gym/rpg/game_master.py` (54), `parse_markdown_case_file` in `cli/case_render.py` (50) and `oracle` in `main.py` (45).

**First step.** pick the ten worst; add characterization tests first; then split.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading F20.
