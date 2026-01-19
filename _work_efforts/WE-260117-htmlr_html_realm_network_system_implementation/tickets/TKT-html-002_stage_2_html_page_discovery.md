---
id: TKT-html-002
parent: WE-260117-html
title: "Stage 2: HTML Page Discovery"
status: pending
created: 2026-01-17T17:14:56.591Z
created_by: ctavolazzi
assigned_to: null
---

# TKT-html-002: Stage 2: HTML Page Discovery

## Metadata
- **Created**: Saturday, January 17, 2026 at 9:14:56 AM PST
- **Parent Work Effort**: WE-260117-html
- **Author**: ctavolazzi

## Description
Discover all HTML files in the project, safely parse metadata, and associate them with realms. This stage uses the security functions from Stage 1.

**Status**: Ready to start (blocked on Stage 1 - now unblocked)

**Tasks**:
1. Implement `discover_html_pages(project_path: Path) -> List[HTMLPageNode]`
   - Recursively scan for `.html` files
   - Apply security exclusions from Stage 1
   - Validate all paths before processing
   - Skip sensitive files (log warning)
   - Handle permission errors gracefully

2. For each valid HTML file:
   - Parse safely using `parse_html_safely()` from Stage 1
   - Extract metadata using `extract_html_metadata()`
   - Create `HTMLPageNode` dataclass instance
   - Associate with realm based on path:
     - `_realms/{realm_name}/` → that realm
     - `scripts/` → "scripts" realm
     - `_work_efforts/` → "work_efforts" realm
     - Root level → "root" realm

3. Create `HTMLPageNode` dataclass:
   - `html_title: str`
   - `html_path: Path`
   - `realm_name: str`
   - `realm_core_id: str` (set in Stage 4)
   - `extracted_links: List[str]`
   - `content_themes: List[str]`
   - `link_count: int`

## Acceptance Criteria
- [ ] All non-sensitive HTML files discovered
- [ ] Metadata extracted safely for all pages
- [ ] Realm association correct for all pages
- [ ] No security violations
- [ ] HTMLPageNode dataclass created
- [ ] discover_html_pages() function implemented

## Files Changed
- (populated when complete)

## Implementation Notes
- (decisions, blockers, context)

## Commits
- (populated as work progresses)
