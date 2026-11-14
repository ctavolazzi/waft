---
id: TKT-bklg-078
title: "F15 Centralize configuration"
status: pending
created: 2026-11-14T15:43:40.226Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# F15 Centralize configuration

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `R` `agent` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** ports and paths are spread through the code: 5050 (dashboard), 2077 (observatory), 8000 (Docker), 8080 (README `waft serve`).

**First step.** one settings module with env overrides; document it in the README.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading F15.
