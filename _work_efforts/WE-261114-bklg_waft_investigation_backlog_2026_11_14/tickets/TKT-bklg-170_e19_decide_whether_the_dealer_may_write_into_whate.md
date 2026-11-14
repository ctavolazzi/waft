---
id: TKT-bklg-170
title: "E19 Decide whether the Dealer may write into whatever folder a command runs in"
status: pending
created: 2026-11-14T19:38:38.180Z
labels: ['pyrite']
---

# E19 Decide whether the Dealer may write into whatever folder a command runs in

## Description

Found during the build pass of 2026-11-14.

## Status

- [ ] Not started

## Notes

Tags: `M` `CT` `P3`

**Evidence.** `_check_dealer_appearance` in `src/waft/main.py` runs on every command except `cards` and `lab`. In any folder that holds `_pyrite` or `pyproject.toml` it creates `_pantheon/the_dealer`, and when he appears he rewrites `state.json`, `memory.jsonl`, `truth/keys.json` and a PDF there. In this repository those files are tracked, so running a waft command from the root can dirty the checkout. `WAFT_DEALER=off` now switches him off.

**First step.** CT decides: keep as is, make him opt-in, or keep his state in the user's home folder.

Found during the build pass; see `BUILD_LOG_2026-11-14.md` in WE-261114-dirn.
