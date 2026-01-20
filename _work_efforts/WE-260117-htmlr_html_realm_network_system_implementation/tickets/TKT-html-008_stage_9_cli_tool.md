---
id: TKT-html-008
parent: WE-260117-html
title: "Stage 9: CLI Tool"
status: pending
created: 2026-01-17T17:15:26.989Z
created_by: ctavolazzi
assigned_to: null
---

# TKT-html-008: Stage 9: CLI Tool

## Metadata
- **Created**: Saturday, January 17, 2026 at 9:15:26 AM PST
- **Parent Work Effort**: WE-260117-html
- **Author**: ctavolazzi

## Description
Create CLI tool for network operations (build, update, show, visualize, stats).

**Status**: Blocked on Stage 8 (User Interface)

**Tasks**:
1. Create `scripts/html_realm_network_builder.py` with commands:
   - `build` - Build network from scratch
   - `update` - Update existing network
   - `show --realm <name>` - Show realm network
   - `visualize --realm <name>` - Visualize network
   - `stats` - Show network statistics

2. Error Handling:
   - Clear error messages
   - Progress indicators
   - Graceful failure handling

## Acceptance Criteria
- [ ] Can build network from CLI
- [ ] Can query network
- [ ] Can visualize network
- [ ] Error messages helpful
- [ ] All commands working

## Files Changed
- (populated when complete)

## Implementation Notes
- (decisions, blockers, context)

## Commits
- (populated as work progresses)
