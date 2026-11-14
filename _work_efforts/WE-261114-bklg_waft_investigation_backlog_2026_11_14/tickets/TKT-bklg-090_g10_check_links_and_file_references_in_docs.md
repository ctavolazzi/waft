---
id: TKT-bklg-090
title: "G10 Check links and file references in docs"
status: pending
created: 2026-11-14T15:43:40.227Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# G10 Check links and file references in docs

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** a link check over `README.md` and the 116 Markdown files under `docs/` found 273 relative links, 147 of them pointing at files that do not exist. `docs/DOCUMENTATION_INDEX.md` alone has 83 broken links, `docs/TYPST_TEMPLATES_BROWSER_REPORT.md` 25, `docs/api/API_INDEX.md` 19, `docs/GETTING_STARTED.md` 7 and `docs/FAQ.md` 5.

**First step.** commit the checker (`scripts/check_doc_links.py`); fix or delete the dead links, starting with the index; add it to CI with today's 147 as the budget.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading G10.
