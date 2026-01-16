---
id: TKT-298w-004
parent: WE-260116-298w
title: "Create CLI Commands for Project Management"
status: pending
created: 2026-01-16T19:28:41.000Z
created_by: ctavolazzi
assigned_to: null
---

# TKT-298w-004: Create CLI Commands for Project Management

## Description

Implement CLI commands for project management, integrated into the main `waft` CLI.

## Acceptance Criteria

- [ ] `project create` command implemented
- [ ] `project list` command implemented
- [ ] `project show` command implemented
- [ ] `project update` command implemented
- [ ] Commands integrated into main `waft` CLI
- [ ] Help text and documentation added
- [ ] Error handling and validation
- [ ] Integration tests created and passing

## Files

- `src/waft/cli/project_commands.py` - CLI commands
- `src/waft/main.py` - Updated to include project app

## Notes

Follow existing CLI patterns (Typer, rich console output, error handling).
