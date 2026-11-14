---
id: TKT-bklg-050
title: "D11 Set a size budget"
status: pending
created: 2026-11-14T15:43:40.225Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# D11 Set a size budget

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** the working tree is 2.9 GB with `.venv`; biggest directories on disk: `waft_pdf_library` 307 MB, `_work_efforts` 276 MB, `waft_desktop` 226 MB, `templates` 143 MB, `examples` 106 MB.

**First step.** a CI check on total tracked size and on any new file over 5 MiB.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading D11.
