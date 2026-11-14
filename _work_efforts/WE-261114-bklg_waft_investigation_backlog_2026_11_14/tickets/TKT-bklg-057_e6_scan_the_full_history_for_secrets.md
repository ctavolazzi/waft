---
id: TKT-bklg-057
title: "E6 Scan the full history for secrets"
status: pending
created: 2026-11-14T15:43:40.225Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# E6 Scan the full history for secrets

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `Q` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** my scan of the current tree used five patterns (`sk-`, `ghp_`, `AKIA`, `AIza`, `xox`) and found nothing; that is a weak test. The history (687 MiB pack) and the vendored `node_modules` were not scanned.

**First step.** run gitleaks and trufflehog over all refs; classify hits as live, rotated or fixture.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading E6.
