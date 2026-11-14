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

**Evidence.** `git tag` lists 0 tags. Three version schemes disagree: `pyproject.toml` says 0.10.0; `CHANGELOG.md` has `[Unreleased]` above 0.9.4 (2026-01-19); `src/waft/version` implements an epoch-based scheme (`v{Years}.{Months}.{Days}.{Hour}.{Quarter}`, epoch 2026-01-04). `waft --version` is not an option ("No such option").

**First step.** choose one scheme; write the release steps (bump, changelog, tag, build, publish or release asset); tag the right commit; add `waft --version` and make it print the same version everywhere.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading B9.
