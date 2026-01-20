---
id: TKT-html-006
parent: WE-260117-html
title: "Stage 6: Page-to-Realm-Core Connections"
status: pending
created: 2026-01-17T17:15:16.616Z
created_by: ctavolazzi
assigned_to: null
---

# TKT-html-006: Stage 6: Page-to-Realm-Core Connections

## Metadata
- **Created**: Saturday, January 17, 2026 at 9:15:16 AM PST
- **Parent Work Effort**: WE-260117-html
- **Author**: ctavolazzi

## Description
Connect all HTML pages to their Realm Cores and create to_realm_core tendrils.

**Status**: Blocked on Stages 2, 4, 5

**Tasks**:
1. Implement `create_to_realm_core_tendrils(network: HTMLRealmNetwork, pages: List[HTMLPageNode], realm_cores: Dict[str, RealmCoreNode]) -> int`
   - For each HTML page: find Realm Core
   - Create `to_realm_core` tendril (strength 0.9)
   - Update page's `realm_core_id`
   - Update Realm Core's `connected_page_ids`

2. Connection Validation:
   - Verify all pages have realm_core_id set
   - Verify all Realm Cores have correct page lists
   - Verify tendrils created correctly

## Acceptance Criteria
- [ ] Every HTML page connects to its Realm Core
- [ ] to_realm_core tendrils have strength 0.9
- [ ] Path Page → Realm Core → The Core exists for all pages
- [ ] All connections validated

## Files Changed
- (populated when complete)

## Implementation Notes
- (decisions, blockers, context)

## Commits
- (populated as work progresses)
