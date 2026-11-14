---
id: TKT-bklg-024
title: "B6 Split heavy dependencies into extras"
status: pending
created: 2026-11-14T15:43:40.223Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# B6 Split heavy dependencies into extras

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `R` `agent` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** core dependencies include `streamlit`, `weasyprint` (needs cairo and pango), `fpdf2`, `pypdf`, `playingcards.py`, `d20`, `tinydb`, `markdown` and `beautifulsoup4`. A user who only wants `waft new` installs all of them.

**First step.** measure install size and time; define extras `pdf`, `ui`, `games`; make the imports lazy.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading B6.
