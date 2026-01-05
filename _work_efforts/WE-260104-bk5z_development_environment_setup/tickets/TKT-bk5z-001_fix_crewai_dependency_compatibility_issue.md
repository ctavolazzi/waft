---
id: TKT-bk5z-001
parent: WE-260104-bk5z
title: "Fix crewai dependency compatibility issue"
status: completed
created: 2026-01-05T07:55:51.694Z
created_by: ctavolazzi
assigned_to: null
---

# TKT-bk5z-001: Fix crewai dependency compatibility issue

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
- 1/4/2026: Made crewai an optional dependency since it requires macOS 13.0+ (onnxruntime dependency) but system is on macOS 12.7.6. Moved crewai from dependencies to optional-dependencies.crewai. Projects that need CrewAI can install it separately with `uv sync --extra crewai`.
- (decisions, blockers, context)

## Commits
- (populated as work progresses)
