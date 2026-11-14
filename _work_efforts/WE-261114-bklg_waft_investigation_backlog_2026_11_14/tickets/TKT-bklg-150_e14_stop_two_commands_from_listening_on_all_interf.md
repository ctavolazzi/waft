---
id: TKT-bklg-150
title: "E14 Stop two commands from listening on all interfaces by default"
status: pending
created: 2026-11-14T16:06:01.150Z
labels: ['pyrite']
---

# E14 Stop two commands from listening on all interfaces by default

## Description

Evidence and first step are in the Notes below and in INVESTIGATION_BACKLOG.md.

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P1`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `main.py:4576` (`waft rag ui`) and `main.py:4623` (`waft rag serve`) default `--host` to `0.0.0.0` on port 7860, so the Gradio app listens on every network interface. `core/door_guy.py:96` also contains `0.0.0.0`, but in a blocklist (a false positive). `waft serve` itself defaults to localhost.

**First step.** default to `127.0.0.1`, require an explicit `--host 0.0.0.0` with a printed warning; add a test of the defaults.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading E14.
