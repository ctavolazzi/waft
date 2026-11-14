---
id: TKT-bklg-008
title: "A8 Explain the setup error in tests/real_proof_test.py"
status: pending
created: 2026-11-14T15:43:40.222Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# A8 Explain the setup error in tests/real_proof_test.py

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `uv run pytest tests/real_proof_test.py` ends with 1 passed and 1 error (`test_real_performance_after_fix`). The error text was not read in full.

**First step.** read it; decide whether this "real proof" still means anything once the tracing is fixed.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading A8.
