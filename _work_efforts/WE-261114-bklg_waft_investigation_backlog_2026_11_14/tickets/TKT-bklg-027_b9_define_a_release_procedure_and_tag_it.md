---
id: TKT-bklg-027
title: "B9 Define a release procedure and tag it"
status: pending
created: 2026-11-14T15:43:40.224Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# B9 Define a release procedure and tag it

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `git tag` lists 0 tags. `pyproject.toml` says 0.10.0; `CHANGELOG.md` has an `[Unreleased]` section (the staging workflow warns about it); `src/waft/version/` exists and was not read.

**First step.** write the steps (bump, changelog, tag, build, publish or release asset); check the three version sources agree; tag at the right commit.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading B9.
