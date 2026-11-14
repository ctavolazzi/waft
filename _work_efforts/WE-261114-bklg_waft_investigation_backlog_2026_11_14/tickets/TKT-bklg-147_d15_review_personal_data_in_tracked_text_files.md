---
id: TKT-bklg-147
title: "D15 Review personal data in tracked text files"
status: pending
created: 2026-11-14T16:06:00.394Z
labels: ['pyrite']
---

# D15 Review personal data in tracked text files

## Description

Evidence and first step are in the Notes below and in INVESTIGATION_BACKLOG.md.

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** a scan of 7,215 tracked text files (no `node_modules`, no binaries) found 68 distinct email addresses and 16 files with phone-number-like text. Most look like placeholders (`viewer@email.com`, `waft@example.com`), but `christopher@fogsift.com` and `porchroot@gmail.com` each appear in 12 files, and the phone-like text is in invoices and business cards under `_work_efforts/WE-260119-ejtx...`. Whether any belong to real people was not checked.

**First step.** list the real ones; replace with placeholders or remove; add a personal-data check to pre-commit (L3).

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading D15.
