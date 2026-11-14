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

**Evidence.** the current tree was scanned two ways: five regexes (`sk-`, `ghp_`, `AKIA`, `AIza`, `xox`) found nothing, and detect-secrets over 7,215 tracked text files (no `node_modules`, no binaries) raised 2,807 raw hits in 417 files: 2,209 base64-entropy, 537 hex-entropy and 61 keyword hits in 27 files, mostly docs about secrets, plan files (D16) and scripts. None was verified. The history (this clone is shallow, L9) and the vendored `node_modules` were not scanned.

**First step.** unshallow (L9); run gitleaks and trufflehog over all refs; classify each hit as live, rotated or fixture; triage the 27 keyword files first.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading E6.
