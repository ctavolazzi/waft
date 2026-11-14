---
id: TKT-bklg-055
title: "E4 Audit shell and subprocess calls"
status: pending
created: 2026-11-14T15:43:40.225Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# E4 Audit shell and subprocess calls

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P1`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `src` has 241 `subprocess.` references, 14 `shell=True` and 4 `os.system`. No `eval(`, `exec(`, `pickle.load` or `yaml.load(` hits. Where the arguments come from was not read.

**First step.** list the 18 sites; for each: argument source (CLI, API, document text); replace with list arguments or `shlex.quote`.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading E4.
