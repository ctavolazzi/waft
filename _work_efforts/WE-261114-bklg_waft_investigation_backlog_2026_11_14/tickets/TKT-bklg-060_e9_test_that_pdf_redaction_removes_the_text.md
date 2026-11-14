---
id: TKT-bklg-060
title: "E9 Test that PDF redaction removes the text"
status: pending
created: 2026-11-14T15:43:40.225Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# E9 Test that PDF redaction removes the text

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `Q` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `src/waft/redactor.py` and `src/waft/pdf_redactor.py` exist. Whether redacted text can still be extracted was not tested.

**First step.** redact a sample PDF, extract text with two tools, fail the test if the text survives.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading E9.
