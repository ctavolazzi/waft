---
id: TKT-bklg-047
title: "D8 Move runtime data out of git"
status: pending
created: 2026-11-14T15:43:40.225Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# D8 Move runtime data out of git

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** 4 tracked database files: `.empirica/sessions/sessions.db` (51 tables; 133 sessions, 56 reflexes; its `-wal` and `-shm` files are tracked too), `_pyrite/analytics/sessions.db`, `waft_memory.db` and `waft_pdf_library/backend/data/library.db` (2,125 PDF records); plus 162 tracked `.jsonl` files. During my runs, opening the Empirica database changed the tracked `.empirica/sessions/sessions.db-shm`; I restored it with `git checkout`.

**First step.** inspect for personal paths; split fixtures from runtime data; ignore the runtime paths (A10).

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading D8.
