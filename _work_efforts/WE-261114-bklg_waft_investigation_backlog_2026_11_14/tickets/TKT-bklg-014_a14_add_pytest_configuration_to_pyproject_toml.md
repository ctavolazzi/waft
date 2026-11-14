---
id: TKT-bklg-014
title: "A14 Add pytest configuration to pyproject.toml"
status: pending
created: 2026-11-14T15:43:40.223Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# A14 Add pytest configuration to pyproject.toml

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** there is no `[tool.pytest.ini_options]`. AGENTS.md says a bare `pytest` collects broken files and can end in an INTERNALERROR (from `narcissus_lab/internal_monologue`). The full run takes about 80 s (78.9 s and 85.3 s measured).

**First step.** set `testpaths = ["tests"]`, register markers (`slow`, `needs_pdf_lib`, `network`), set a default timeout, and make `uv run pytest` safe with no arguments.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading A14.
