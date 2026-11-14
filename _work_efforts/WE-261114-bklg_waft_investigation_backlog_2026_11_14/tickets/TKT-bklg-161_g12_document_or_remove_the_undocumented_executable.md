---
id: TKT-bklg-161
title: "G12 Document or remove the undocumented executable scripts"
status: pending
created: 2026-11-14T16:06:04.056Z
labels: ['pyrite']
---

# G12 Document or remove the undocumented executable scripts

## Description

Evidence and first step are in the Notes below and in INVESTIGATION_BACKLOG.md.

## Status

- [ ] Not started

## Notes

Tags: `R` `agent` `P3`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** 36 tracked `.sh` files outside `node_modules` (34 mode 755, 2 mode 644 despite shebangs; modes checked, names of the two not). A helper agent found six executables named in no doc, code or CI file: `_science_textbook/compile.sh`, `examples/START_PROJECTS_DASHBOARD.sh`, `install_latex.sh`, `open_small_iterm.sh`, `verify_latex.sh` and `recap_review_app/backend/docker-entrypoint.sh`. It also reports that `install_latex.sh` is the only script using `sudo` (macOS, `brew` and `tlmgr`, no confirmation) and that 12 Python files and several scripts carry hardcoded `/Users/...` or `/Volumes/...` paths (D9).

**First step.** list every script with one line on what it does and whether it is current; delete or archive the rest with CT's approval; keep `install_latex.sh` manual.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading G12.
