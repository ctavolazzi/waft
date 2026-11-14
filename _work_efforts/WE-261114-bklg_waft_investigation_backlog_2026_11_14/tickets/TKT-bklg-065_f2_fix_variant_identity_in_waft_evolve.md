---
id: TKT-bklg-065
title: "F2 Fix variant identity in waft evolve"
status: pending
created: 2026-11-14T15:43:40.226Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# F2 Fix variant identity in waft evolve

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P1`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `waft evolve --generations 2 --variants 3` printed one id three times (`being_20261114_153322_37e1e692`), then `fitness=100.00, scints=0` for each, "Fitness improvement: +0.00" and a total time of 0.01 s. Cause (read): `src/waft/being.py:1836` builds the id from `datetime.now().strftime('%Y%m%d_%H%M%S')` (one-second resolution) plus the first 8 hex digits of `sha256(reality_id + parent_being_id)`, so variants spawned in the same second share an id; skill mutations (`being.py:1846`) are derived from a hash of that id and the skill name, so they are identical too. `core/evolution_engine.py:318` and `:319` add unseeded `random.uniform` changes to `will_to_live` and `luck`. FogSift gap #44 records the same id defect.

**First step.** add the variant index or a random suffix to the id; derive mutations from (id, generation, index); seed the random generator from a run seed; add a test that N variants have N ids and N distinct genomes.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading F2.
