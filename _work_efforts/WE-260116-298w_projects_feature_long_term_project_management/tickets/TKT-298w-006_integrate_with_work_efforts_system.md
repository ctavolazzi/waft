---
id: TKT-298w-006
parent: WE-260116-298w
title: "Integrate with Work Efforts System"
status: pending
created: 2026-01-16T19:28:41.000Z
created_by: ctavolazzi
assigned_to: null
---

# TKT-298w-006: Integrate with Work Efforts System

## Description

Integrate projects with the existing work efforts system (Johnny Decimal), allowing projects to link to work efforts and track their completion.

## Acceptance Criteria

- [ ] Projects can link to work efforts via `related_work_efforts` field
- [ ] Progress entries can reference work effort IDs
- [ ] Work effort completion can update project progress
- [ ] Integration tests created and passing
- [ ] Documentation updated

## Files

- `src/waft/core/projects.py` - Work effort integration methods

## Notes

This connects Projects to the existing work effort tracking system, enabling comprehensive project management.
