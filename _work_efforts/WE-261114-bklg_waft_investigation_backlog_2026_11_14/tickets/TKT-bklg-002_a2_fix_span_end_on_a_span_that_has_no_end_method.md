---
id: TKT-bklg-002
title: "A2 Fix span.end() on a Span that has no end method"
status: pending
created: 2026-11-14T15:43:40.222Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# A2 Fix span.end() on a Span that has no end method

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P1`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `decision_matrix.py:132` calls `span.end(...)`. `Span` in `core/tracing/tracer.py` is a dataclass with no `end`; the tracer's method is `end_span(span, status, error=...)`. After A1 this raises AttributeError in `test_core.py::test_wsm_calculation`, `test_core.py::test_deterministic_tie_breaking` and `test_persistence.py::test_loaded_matrix_is_valid`.

**First step.** use `tracer.end_span` or add `Span.end`; decide which API is the intended one and make the callers agree.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading A2.
