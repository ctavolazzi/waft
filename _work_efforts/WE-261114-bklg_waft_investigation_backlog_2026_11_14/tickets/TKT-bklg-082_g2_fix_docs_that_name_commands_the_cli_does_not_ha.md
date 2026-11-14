---
id: TKT-bklg-082
title: "G2 Fix docs that name commands the CLI does not have"
status: pending
created: 2026-11-14T15:43:40.227Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# G2 Fix docs that name commands the CLI does not have

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P1`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `waft --help` lists 82 commands. A scan of `README.md` and `docs/*.md` for `waft <word>` found words with no command, among them `spawn`, `eval`, `lineage`, `select`, `import`, `scenario`, `personnel`, `agent`, `version`, `test`, `decision-compare`, `decision-export`, `decision-history`, `decision-show`, `oracle-personality` and `create`, in at least 18 docs (for example `docs/FAQ.md`, `GETTING_STARTED.md`, `SYSTEM_OVERVIEW.md`, `TROUBLESHOOTING.md` and four `FOGSIFT_WAFT_SEED_PROMPT*` files). A few hits are prose ("waft itself").

**First step.** commit the scan as `scripts/check_docs_commands.py`, fix or archive each doc, add it to CI. This is `_workbench` ticket 10.9, which is blocked.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading G2.
