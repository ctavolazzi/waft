---
id: TKT-html-008
parent: WE-260117-html
title: "Stage 8: Network Query & Pathfinding"
status: pending
created: 2026-01-17T17:15:26.987Z
created_by: ctavolazzi
assigned_to: null
---

# TKT-html-008: Stage 8: Network Query & Pathfinding

## Metadata
- **Created**: Saturday, January 17, 2026 at 9:15:26 AM PST
- **Parent Work Effort**: WE-260117-html
- **Author**: ctavolazzi

## Description
Implement network query functions and verify "ALL POINTS CONNECT TO THE ONE" through pathfinding.

**Status**: Blocked on Stage 7

**Tasks**:
1. Query Functions:
   - `get_the_core() -> CoreNode`
   - `get_realm_network(realm_name: str) -> Dict`
   - `find_path_to_core(from_page: str) -> List[str]` (Path: Page → Realm Core → The Core)
   - `find_path_between_pages(from_page: str, to_page: str) -> List[str]` (multi-dimensional pathfinding)

2. Pathfinding Enhancement:
   - Enhance `find_path()` from TendrilNetwork to prioritize Core paths:
     - to_core tendrils (weight: 1.0)
     - to_realm_core tendrils (weight: 0.9)
     - hyperlink tendrils (weight: 0.7)
     - content_similarity tendrils (weight: 0.5)
     - filesystem tendrils (weight: 0.4)

3. Verification:
   - Verify all pages can reach The Core
   - Test pathfinding between arbitrary pages
   - Generate network statistics

## Acceptance Criteria
- [ ] Can query The Core and Realm Cores
- [ ] Can find paths to The Core from any page
- [ ] Can find paths between any two pages
- [ ] Network statistics accurate
- [ ] ALL POINTS CONNECT TO THE ONE verified

## Files Changed
- (populated when complete)

## Implementation Notes
- (decisions, blockers, context)

## Commits
- (populated as work progresses)
