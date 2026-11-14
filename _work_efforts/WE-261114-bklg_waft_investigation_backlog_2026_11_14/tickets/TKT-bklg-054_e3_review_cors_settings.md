---
id: TKT-bklg-054
title: "E3 Review CORS settings"
status: in_progress
created: 2026-11-14T15:43:40.225Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# E3 Review CORS settings

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] In progress

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `src/waft/api/main.py:120` sets `allow_origins` to four localhost URLs (ports 5173, 3000 and 8781 on localhost and 127.0.0.1) with `allow_credentials=True` and `*` for methods and headers; there is no wildcard origin. `tests/test_cors.py::test_actual_post_request_with_cors` returns 500 and A1 alone does not fix it.

**First step.** decide how a hosted deployment sets its origins (an environment variable); fix the 500 (A4).

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading E3.

**2026-11-14 (build pass).** The 500 was the tracing bug and is gone. The allowed origins are still a fixed list.
