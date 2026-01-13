---
id: TKT-z88r-001
parent: WE-260112-z88r
title: "Create evolve-another-template command"
status: completed
created: 2026-01-13T03:25:21.341Z
created_by: ctavolazzi
assigned_to: null
completed: 2026-01-12T19:30:00.000Z
---

# TKT-z88r-001: Create evolve-another-template command

## Metadata
- **Created**: Monday, January 12, 2026 at 7:25:21 PM PST
- **Completed**: Monday, January 12, 2026 at 7:30:00 PM PST
- **Parent Work Effort**: WE-260112-z88r
- **Author**: ctavolazzi

## Description
Create the `/evolve-another-template` command that allows users to generate evolution reports using alternative template formats instead of the default format.

## Acceptance Criteria
- [x] Command file created at `.cursor/commands/evolve-another-template.md`
- [x] Implementation script created at `scripts/evolve_another_template.py`
- [x] CLI command registered in `src/waft/main.py`
- [x] Command can load evolution data from most recent `/evolve` run
- [x] Command supports template selection
- [x] Command generates PDFs using selected template

## Files Changed
- `.cursor/commands/evolve-another-template.md` - Command documentation
- `scripts/evolve_another_template.py` - Implementation script
- `src/waft/main.py` - CLI command registration

## Implementation Notes
- Command loads the most recent Being evolution data automatically
- Supports `--template`, `--list`, and `--all` options
- PDFs are saved to Desktop and opened automatically
- Work effort reference added to command and script

## Commits
- Initial implementation complete
