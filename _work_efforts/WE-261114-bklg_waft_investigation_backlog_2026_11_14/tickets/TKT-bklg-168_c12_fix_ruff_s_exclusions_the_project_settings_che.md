---
id: TKT-bklg-168
title: "C12 Fix ruff's exclusions: the project settings check 4 files"
status: pending
created: 2026-11-14T19:38:37.871Z
labels: ['pyrite']
---

# C12 Fix ruff's exclusions: the project settings check 4 files

## Description

Found during the build pass of 2026-11-14.

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P2`

**Evidence.** `ruff check . --show-files` with the project settings lists 4 files, all `pyproject.toml`. The `exclude` list in `pyproject.toml` names folders such as `api`, `cli`, `docs`, `templates`, `tools`, `web` and `lib`, and ruff matches those names anywhere in the tree, including inside `src/waft`. So the lint and format jobs in CI have been checking nothing. CI now also runs an isolated undefined-names pass, which does not depend on these settings.

**First step.** Anchor the exclusions to the repository root (`/api`, `/cli` and so on), run ruff over `src/waft`, and ratchet the 268 findings down.

Found during the build pass; see `BUILD_LOG_2026-11-14.md` in WE-261114-dirn.
