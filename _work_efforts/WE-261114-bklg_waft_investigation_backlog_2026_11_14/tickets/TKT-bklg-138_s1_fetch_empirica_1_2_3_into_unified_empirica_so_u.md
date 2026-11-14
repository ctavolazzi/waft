---
id: TKT-bklg-138
title: "S1 Fetch empirica 1.2.3 into _unified/empirica so uv sync can resolve it"
status: completed
created: 2026-11-14T15:43:40.230Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# S1 Fetch empirica 1.2.3 into _unified/empirica so uv sync can resolve it

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [x] Completed

## Notes

Done 2026-11-14. Followed AGENTS.md: `pip3 download empirica==1.2.3 --no-binary :all: --no-deps`, extracted the sdist, copied it to `_unified/empirica` (gitignored). The recipe's `/workspace` path does not exist here, so the copy used this checkout's path. See B4.

Full context: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md).
