---
id: TKT-bklg-149
title: "E13 Triage the high and medium bandit findings"
status: pending
created: 2026-11-14T16:06:00.860Z
labels: ['pyrite']
---

# E13 Triage the high and medium bandit findings

## Description

Evidence and first step are in the Notes below and in INVESTIGATION_BACKLOG.md.

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `bandit -r src` reports 717 issues over 135,988 lines: 7 high, 9 medium, 701 low. High: `core/status_persistence.py:73` and `:108` (B324, weak hash), `dealer/pdf_generator.py:221` and `main.py:4078` (B602), `fogsift/simulation.py:17`, `pet/fogsift_cli.py:52` and `pet/fogsift_device.py:321` (B605). Medium: `core/pocketbase_scout.py:135` (B103, file permissions), `main.py:853` and `core/realms/pocketbase_downloader.py:87` (B310, urlopen), `document_builder.py:962`, `templates/typst/compiler.py:107` and `:108` (B108, fixed /tmp path), and three B104 bind-all hits covered in E14. The 701 low findings were not read.

**First step.** read each of the 16, fix it or mark it with a reason; add bandit to CI with this list as the baseline (C11).

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading E13.
