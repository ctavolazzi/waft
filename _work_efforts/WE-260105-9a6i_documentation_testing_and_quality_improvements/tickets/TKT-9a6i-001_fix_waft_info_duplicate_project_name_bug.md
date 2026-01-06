---
id: TKT-9a6i-001
parent: WE-260105-9a6i
title: "Fix waft info duplicate Project Name bug"
status: completed
created: 2026-01-05T08:07:05.804Z
created_by: ctavolazzi
assigned_to: null
---

# TKT-9a6i-001: Fix waft info duplicate Project Name bug

## Metadata
- **Created**: Monday, January 5, 2026 at 12:07:05 AM PST
- **Parent Work Effort**: WE-260105-9a6i
- **Author**: ctavolazzi

## Description
(describe what needs to be done)

## Acceptance Criteria
- [ ] (define acceptance criteria)

## Files Changed
- `src/waft/main.py`

## Implementation Notes
- 1/6/2026: Fixed duplicate Project Name bug in waft info command. Updated logic in src/waft/main.py lines 402-418 to check pyproject.toml existence first, then parse. Ensures only one "Project Name" row is displayed regardless of parsing status.
- (decisions, blockers, context)

## Commits
- `cd30afb`
- (populated as work progresses)
