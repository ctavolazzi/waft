---
id: TKT-bklg-076
title: "F13 Choose which front ends to keep"
status: pending
created: 2026-11-14T15:43:40.226Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# F13 Choose which front ends to keep

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `CT` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** seven exist: the FastAPI app (`waft serve`), the `dashboard` and `dashboard-5050` commands, the observatory (`core/observatory/server.py`, 1,390 lines), Streamlit (`ui/streamlit`), the SvelteKit `visualizer/`, the Electron `waft_desktop/`, and `typst-webapp/`.

**First step.** for each: last used, who uses it, build status; keep one or two.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading F13.
