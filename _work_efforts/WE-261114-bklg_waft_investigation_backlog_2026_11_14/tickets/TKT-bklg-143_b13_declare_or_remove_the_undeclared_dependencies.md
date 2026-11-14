---
id: TKT-bklg-143
title: "B13 Declare or remove the undeclared dependencies"
status: in_progress
created: 2026-11-14T16:05:59.472Z
labels: ['pyrite']
---

# B13 Declare or remove the undeclared dependencies

## Description

Evidence and first step are in the Notes below and in INVESTIGATION_BACKLOG.md.

## Status

- [ ] In progress

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `deptry src --known-first-party waft` reports 83 modules imported but not declared, 21 transitive packages used directly and 4 declared but unused. Undeclared third-party names include `reportlab` (8 imports), `fitz` (PyMuPDF, 4), `plotly` (4) and `sklearn` (2). Used directly but only transitive: `yaml` (6), `requests` (3), `PIL` (3), `pandas` (2), `google` (2), `cryptography` (2), `numpy` and `dotenv` (1 each). Several first-party-looking names (`src`, `foundation`, `demo_api`, `scripts`, `rag_chatbot`, `tmcg`, `patterns`, `scientific_method_tool`) point at broken imports or path hacks. Declared but unused: the `crewai` extra and the dev tools `pytest`, `pytest-cov` and `ruff` (the last three are expected).

**First step.** decide per package: declare it in an extra, make the import lazy with a clear error, or delete the code; add deptry to CI with this count as the starting budget (C11).

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading B13.

**2026-11-14 (build pass).** pillow, pyyaml, requests and cryptography are declared. reportlab, fitz, plotly, sklearn and the rest are not.
