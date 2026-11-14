---
id: TKT-bklg-160
title: "F23 Fix helper scripts that abort or leave processes behind"
status: pending
created: 2026-11-14T16:06:03.790Z
labels: ['pyrite']
---

# F23 Fix helper scripts that abort or leave processes behind

## Description

Evidence and first step are in the Notes below and in INVESTIGATION_BACKLOG.md.

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** checked by me: `scripts/sync-cursor-commands.sh` runs under `set -e` (line 8) and increments counters with `((SKIPPED++))` and `((SYNCED++))` (lines 50, 54, 59); in bash `set -e; X=0; ((X++))` exits with status 1, so the script stops after the first file, and its `cp` overwrites commands in `~/.cursor/commands` with no backup. `waft_desktop/START_DEV.sh` starts `npm run dev &` (line 63) and `npm start` (73) but registers its cleanup trap only at line 77, after `set -e` (line 4) can already have exited. Helper agent, not checked by me: `START_EVOLVE_UI.sh` runs `cd visualizer` relative to the caller's directory; several start scripts write fixed `/tmp/*.log` names and leave servers running.

**First step.** initialise counters with `X=$((X+1))`; move the trap above the first background process; use `mktemp` and `trap`; run `shellcheck` over the 36 tracked shell scripts and add it to CI.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading F23.
