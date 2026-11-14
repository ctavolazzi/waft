---
id: TKT-bklg-037
title: "C8 Pin tool and runner versions in workflows"
status: pending
created: 2026-11-14T15:43:40.224Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# C8 Pin tool and runner versions in workflows

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `R` `agent` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `astral-sh/setup-uv@v4` with `version: "latest"` and `runs-on: ubuntu-latest`. The sibling book repo's CI broke when `ubuntu-latest` moved to 26.04 (`_workbench/sessions/LOG.md`, 2026-11-10).

**First step.** pin the runner image and the uv version.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading C8.
