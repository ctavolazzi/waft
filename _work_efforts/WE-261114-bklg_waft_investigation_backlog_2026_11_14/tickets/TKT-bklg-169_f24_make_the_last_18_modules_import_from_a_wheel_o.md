---
id: TKT-bklg-169
title: "F24 Make the last 18 modules import from a wheel, or move them out"
status: pending
created: 2026-11-14T19:38:38.028Z
labels: ['pyrite']
---

# F24 Make the last 18 modules import from a wheel, or move them out

## Description

Found during the build pass of 2026-11-14.

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P3`

**Evidence.** After the packaging fix, a script that imports every module of the installed wheel reports 506 of 524 importing. The 18 that do not: 13 demos that import each other by bare name (`demo_api`, `foundation`, `advanced`, `benchmark`), 3 that import `KeyValueBlock` from `waft.foundation` (it is gone), 2 that need `scientific_method_tool` from a checkout, `core.hub.display` (needs pygame) and `waft.rag` (its submodule is not initialised).

**First step.** Move the demos to `examples/` (backlog F5), delete or fix the three stale ones with CT's approval, and make the optional ones fail with a clear message.

Found during the build pass; see `BUILD_LOG_2026-11-14.md` in WE-261114-dirn.
