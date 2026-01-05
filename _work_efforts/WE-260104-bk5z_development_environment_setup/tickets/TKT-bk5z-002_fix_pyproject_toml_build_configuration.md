---
id: TKT-bk5z-002
parent: WE-260104-bk5z
title: "Fix pyproject.toml build configuration"
status: completed
created: 2026-01-05T07:55:51.696Z
created_by: ctavolazzi
assigned_to: null
---

# TKT-bk5z-002: Fix pyproject.toml build configuration

## Metadata
- **Created**: Sunday, January 4, 2026 at 11:55:51 PM PST
- **Parent Work Effort**: WE-260104-bk5z
- **Author**: ctavolazzi

## Description
(describe what needs to be done)

## Acceptance Criteria
- [ ] (define acceptance criteria)

## Files Changed
- `pyproject.toml`

## Implementation Notes
- 1/4/2026: Fixed three build configuration issues: 1) Updated license format from `{text = "MIT"}` to `"MIT"` (deprecated format), 2) Removed deprecated license classifier, 3) Added `package-dir = {"" = "src"}` to point setuptools to correct package location. All fixes required for successful build.
- (decisions, blockers, context)

## Commits
- (populated as work progresses)
