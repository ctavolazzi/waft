---
id: TKT-html-004
parent: WE-260117-html
title: "Stage 4: Realm Core Creation"
status: pending
created: 2026-01-17T17:15:08.409Z
created_by: ctavolazzi
assigned_to: null
---

# TKT-html-004: Stage 4: Realm Core Creation

## Metadata
- **Created**: Saturday, January 17, 2026 at 9:15:08 AM PST
- **Parent Work Effort**: WE-260117-html
- **Author**: ctavolazzi

## Description
Discover all realms, create Core.html for each realm, and connect Realm Cores to The Core.

**Status**: Blocked on Stages 2, 3

**Tasks**:
1. Implement `discover_realms(project_path: Path) -> Dict[str, Path]`
   - Scan `_realms/` directory
   - Check `_pantheon/external_drive_realm/` for realm registries
   - Support custom realm mappings
   - Return `{realm_name: realm_path}`

2. Implement `create_realm_cores(project_path: Path, realms: Dict[str, Path], the_core: CoreNode) -> Dict[str, RealmCoreNode]`
   - For each realm: locate/create `Core.html`
   - Set permissions using `set_secure_permissions()` from Stage 1
   - Create `RealmCoreNode`
   - Connect to The Core (to_core tendril, strength 1.0)
   - Calculate statistics

3. Create `RealmCoreNode` dataclass:
   - `realm_core_id: str`
   - `realm_name: str`
   - `core_html_path: Path`
   - `connected_page_ids: List[str]` (populated in Stage 6)
   - `connected_to_core_id: str = "the_core"`

4. Create Core Connections:
   - Create `to_core` tendrils from each Realm Core to The Core
   - Strength: 1.0 (maximum, permanent)
   - Connection type: "to_core"

## Acceptance Criteria
- [ ] Each realm has Core.html
- [ ] All Realm Cores connect to The Core
- [ ] to_core tendrils with max strength (1.0)
- [ ] Realm statistics calculated
- [ ] RealmCoreNode dataclass created

## Files Changed
- (populated when complete)

## Implementation Notes
- (decisions, blockers, context)

## Commits
- (populated as work progresses)
