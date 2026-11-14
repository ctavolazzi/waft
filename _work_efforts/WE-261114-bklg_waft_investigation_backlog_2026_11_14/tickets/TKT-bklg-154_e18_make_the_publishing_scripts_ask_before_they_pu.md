---
id: TKT-bklg-154
title: "E18 Make the publishing scripts ask before they push"
status: pending
created: 2026-11-14T16:06:02.213Z
labels: ['pyrite']
---

# E18 Make the publishing scripts ask before they push

## Description

Evidence and first step are in the Notes below and in INVESTIGATION_BACKLOG.md.

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** checked by me: `push_to_github.sh` runs `git add .` (line 32), `git branch -M main` (49) and `git push -u origin main` (56) against a hardcoded remote with no prompt; `scripts/promote-staging-to-main.sh` sets `VERSION` only through `--version` (line 27) and tests `-n "$VERSION"` at line 129, so an inherited `VERSION` variable creates and pushes a release tag. Helper agent, not checked by me: `setup_github.sh` also does `git add .` and commits with a stale v0.1.0 message; `scripts/upload_wiki.sh` clones the wiki into `.wiki-temp` inside the repo (not ignored) and pushes with no prompt; both promote scripts run `git checkout` and `git pull` even under `--dry-run`, so "No changes were made" is false.

**First step.** initialise `VERSION` empty; add a confirmation prompt and a `--yes` flag; stop `git add .`; refuse to run from a non-main branch; make `--dry-run` change nothing.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading E18.
