---
id: TKT-bklg-066
title: "F3 Find out what \"evolution\" operates on"
status: in_progress
created: 2026-11-14T15:43:40.226Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# F3 Find out what "evolution" operates on

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] In progress

## Notes

Tags: `M` `research` `P1`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `core/evolution_engine.py` lines 63 to 131: `evaluate_fitness` never runs the trial tasks (a code comment says "For now, simple heuristic based on being's attributes"); for each task string it runs the same three detectors on the same being (logic fractures, knowledge gaps, safety violations), so a scint is counted once per task. Fitness is 100 minus 10 per scint plus 5 per skill above 80, clamped to 0 to 100. A freshly spawned being has none of the impossible states the detectors look for, so every variant scores 100. Mutation changes numbers (skill levels by up to 5 percent, `will_to_live`, `luck`); in this path no code is generated or rewritten. Provider names appear in few files (anthropic 2, openai 3, ollama 5, gemini 3 files) and `evolve` calls no model.

**First step.** write the one-page spec: genome fields, mutation operators, fitness function; say plainly in the README what `evolve` does today; decide what a real trial (an executed task with a measurable result) would be (R2).

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading F3.

**2026-11-14 (build pass).** `waft evolve` now says, in its help and its output, that it runs no task. The loop that does is `waft lab run` (docs/LAB.md). The one-page genome spec is not written.
