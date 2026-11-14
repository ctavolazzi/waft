---
id: TKT-bklg-080
title: "F17 Pick one observability story"
status: pending
created: 2026-11-14T15:43:40.227Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# F17 Pick one observability story

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `R` `research` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** separate mechanisms exist: `logging.py`, tracing (`_pyrite/analytics/traces`), the flight recorder (`_pyrite/flight_recorder`), journals, and the debug file in E5.

**First step.** choose one path for logs and one for traces; remove the rest.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading F17.
