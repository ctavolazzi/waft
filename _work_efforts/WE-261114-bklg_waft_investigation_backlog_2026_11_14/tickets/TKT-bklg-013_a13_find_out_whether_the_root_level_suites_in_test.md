---
id: TKT-bklg-013
title: "A13 Find out whether the root-level suites in tests/ are run anywhere"
status: pending
created: 2026-11-14T15:43:40.223Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# A13 Find out whether the root-level suites in tests/ are run anywhere

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `R` `agent` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** pytest's default file pattern skips `mega_test_suite.py`, `hellfire_test_suite.py`, `insane_test_suite.py`, `torture_test_suite.py`, `scientific_test_suite.py`, `adversarial_red_team.py`, `quantitative_benchmarks.py` and the `self_*` files in `tests/`. Whether any script or workflow runs them was not checked.

**First step.** grep for each name in scripts and workflows; run each once; keep the ones that pass and mean something.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading A13.
