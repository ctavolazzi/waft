---
id: TKT-bklg-079
title: "F16 Pin down the API error contract"
status: pending
created: 2026-11-14T15:43:40.226Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# F16 Pin down the API error contract

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `tests/test_api.py::test_analyze_endpoint_missing_scores` expects HTTP 400 with the text "Missing score" under the `message` key; the app returns 500 today (cause: A1 to A3).

**First step.** after A1 to A3 confirm 400; export the OpenAPI schema and add a snapshot test.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading F16.
