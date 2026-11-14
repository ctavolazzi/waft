---
id: TKT-bklg-017
title: "A17 Run the suite on Python 3.12 and 3.13"
status: in_progress
created: 2026-11-14T15:43:40.223Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# A17 Run the suite on Python 3.12 and 3.13

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] In progress

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** everything here ran on Python 3.14.3 because uv honours `.python-version`. CI uses 3.12 and `requires-python` is `>=3.12`.

**First step.** `uv run --python 3.12 pytest ...` and 3.13; fix the failures or narrow the supported range.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading A17.

**2026-11-14 (build pass).** Python 3.12.3: 735 passed before the lab tests were added, and a 3.12 wheel install passes the lab doctor with the same digest. 3.13 not run.
