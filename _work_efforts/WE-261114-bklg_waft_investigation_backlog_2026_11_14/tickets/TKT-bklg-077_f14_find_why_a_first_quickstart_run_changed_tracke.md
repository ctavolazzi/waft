---
id: TKT-bklg-077
title: "F14 Find why a first quickstart run changed tracked files in the checkout"
status: completed
created: 2026-11-14T15:43:40.226Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# F14 Find why a first quickstart run changed tracked files in the checkout

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [x] Completed

## Notes

Tags: `M` `agent` `P1`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** my first run of `waft new demo`, `waft verify` and `waft evolve --generations 2 --variants 3` (cwd a scratch directory, started with `uv run --project /home/user/waft`) left four tracked files modified in `/home/user/waft`: `_pantheon/the_dealer/memory.jsonl`, `state.json`, `truth/keys.json` and `seals/gate_02_the_marker.pdf`. Two reruns did not reproduce it. `verify` rolls dice ("CON Check ... failure"), so the outcome may depend on a random roll. Relative paths `Path("_pantheon/the_dealer")` appear at `main.py:1064` and `core/dealer_journal.py:16`. I reverted the files. F19 found the same class of bug in the API: state written relative to the code, not the project.

**First step.** run each command 20 times with a fixed seed while watching `git status` in the source checkout; find the write.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading F14.

**2026-11-14 (build pass).** Cause found: the Dealer (main.py) writes _pantheon/the_dealer relative to the working directory when he appears, and the tests ran commands from the repo root. WAFT_DEALER=off switches him off; the tests set it. Whether he should write into any folder at all is ticket E19.
