---
id: TKT-bklg-158
title: "F21 Replace print, silent excepts and other smells"
status: pending
created: 2026-11-14T16:06:03.288Z
labels: ['pyrite']
---

# F21 Replace print, silent excepts and other smells

## Description

Evidence and first step are in the Notes below and in INVESTIGATION_BACKLOG.md.

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** counts in `src` (grep): 1,575 `print(` calls, 69 `except Exception` blocks that only `pass`, 21 bare `except:`, 229 `open(` calls with no encoding (rough pattern), 140 `datetime.utcnow()` uses (A12), 15 TODO, FIXME, HACK or XXX markers and 1 `raise NotImplementedError`.

**First step.** route output through `logging` or Rich consistently; replace silent excepts with a logged handler; set `encoding="utf-8"` on text opens; ratchet each count.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading F21.
