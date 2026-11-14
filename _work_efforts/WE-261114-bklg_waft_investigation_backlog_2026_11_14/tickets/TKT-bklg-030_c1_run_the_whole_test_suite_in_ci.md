---
id: TKT-bklg-030
title: "C1 Run the whole test suite in CI"
status: pending
created: 2026-11-14T15:43:40.224Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# C1 Run the whole test suite in CI

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `R` `agent` `P1`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `.github/workflows/branch-protection.yml` runs `uv run pytest tests/api` and a lint job. `tests/api` holds about 41 test functions (static count of `def test_`) against 573 outcomes in the baseline run, so CI exercises roughly 7 percent of the suite. The last four runs on `main` (runs 181 to 184, 2026-11-09) are green while 25 tests fail locally.

**First step.** run `pytest tests/` with the known-bad files deselected by name; shrink the list as A1 to A9 land.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading C1.
