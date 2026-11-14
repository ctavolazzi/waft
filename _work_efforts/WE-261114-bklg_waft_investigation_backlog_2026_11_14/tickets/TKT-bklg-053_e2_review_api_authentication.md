---
id: TKT-bklg-053
title: "E2 Review API authentication"
status: pending
created: 2026-11-14T15:43:40.225Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# E2 Review API authentication

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `R` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** the bearer token comes from `get_or_create_token()` in `src/waft/api/auth.py` and is stored in `.waft_api_token`. Comparison method, token scope, which routes require it and rotation were not reviewed.

**First step.** read `auth.py` and every router; list routes by auth requirement; add tests for 401 and 403.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading E2.
