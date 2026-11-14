---
id: TKT-bklg-068
title: "F5 Move demos and generators out of the package root"
status: pending
created: 2026-11-14T15:43:40.226Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# F5 Move demos and generators out of the package root

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** about 40 modules sit directly in `src/waft/`, including `demo_api.py`, `demo_confidence.py`, `demo_stochastic.py`, `demo_anti_dogfooding.py`, `final_demo.py`, `generate_artifacts.py`, `generate_lightcone_docs.py` and `generate_lightcone_docs_weasyprint.py`.

**First step.** move to `examples/` and `scripts/`; fix imports.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading F5.
