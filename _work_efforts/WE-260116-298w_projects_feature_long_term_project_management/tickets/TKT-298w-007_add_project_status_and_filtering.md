---
id: TKT-298w-007
parent: WE-260116-298w
title: "Add Project Status and Filtering"
status: pending
created: 2026-01-16T19:28:41.000Z
created_by: ctavolazzi
assigned_to: null
---

# TKT-298w-007: Add Project Status and Filtering

## Description

Add project status management and filtering capabilities (by status, tags, etc.).

## Acceptance Criteria

- [ ] Project status filtering in `project list` command
- [ ] Tag-based filtering
- [ ] Search functionality
- [ ] Status transitions validated
- [ ] Integration tests created and passing

## Files

- `src/waft/core/projects.py` - Filtering methods
- `src/waft/cli/project_commands.py` - Filtering CLI options

## Notes

Enables users to organize and find projects easily.
