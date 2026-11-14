---
id: TKT-bklg-056
title: "E5 Remove leftover agent logging blocks"
status: pending
created: 2026-11-14T15:43:40.225Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# E5 Remove leftover agent logging blocks

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** five Python files contain `# #region agent log` (`web.py`, `document_builder.py`, `one_pager.py`, `evolution/document_components.py`, `evolution/golden_triangle.py`); `web.py:26` onward appends to `/Users/ctavolazzi/Code/active/waft/.cursor/debug.log`. `waft_desktop/electron/main.js` has six more of the same kind: `fetch` calls to `http://127.0.0.1:7248/ingest/...` that send the process id, the absolute backend path, the port, error text and context-menu link URLs to whatever listens on that loopback port.

**First step.** delete the blocks; run the staging gate's grep locally.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading E5.
