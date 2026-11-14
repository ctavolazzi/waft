---
id: TKT-bklg-139
title: "S2 Run uv sync --extra dev and confirm the waft CLI starts from the checkout"
status: completed
created: 2026-11-14T15:43:40.230Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# S2 Run uv sync --extra dev and confirm the waft CLI starts from the checkout

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [x] Completed

## Notes

Done 2026-11-14. `uv sync --extra dev` succeeded on Python 3.14.3 (uv follows `.python-version`). `uv run waft --help` lists 82 commands. `uv sync` and `uv run` rewrote `uv.lock` each time; it was restored with `git checkout` (A11).

Full context: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md).
