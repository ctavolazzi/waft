---
id: TKT-bklg-003
title: "A3 Import SpanStatus where input_transformer uses it"
status: pending
created: 2026-11-14T15:43:40.222Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# A3 Import SpanStatus where input_transformer uses it

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P1`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `input_transformer.py` lines 75, 78 and 81 pass `SpanStatus.ERROR` to `end_span`; the name is never imported (NameError at line 77 in `test_transformer.py::test_missing_keys` and `test_invalid_number_strings`).

**First step.** import it from `.tracing`; read the other exception branches of that function for the same slip.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading A3.
