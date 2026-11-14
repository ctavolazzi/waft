---
id: TKT-bklg-111
title: "J1 Choose the default PDF engine"
status: pending
created: 2026-11-14T15:43:40.228Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# J1 Choose the default PDF engine

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `R` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** Typst (318 tracked `.typ` files, `typst-webapp`, `typst-demos`), LaTeX (templates, `Latex Source Code`), WeasyPrint and fpdf2 (both core dependencies) and pypdf are all present.

**First step.** render one sample document with each; compare quality, speed and dependencies; pick one default.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading J1.
