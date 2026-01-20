---
id: TKT-l7tt-006
parent: WE-260112-l7tt
title: "Add User Profile, User Data, and App Data sections"
status: completed
created: 2026-01-12T19:26:59.880Z
created_by: ctavolazzi
assigned_to: null
completed: 2026-01-18T23:45:00.000Z
---

# TKT-l7tt-006: Add User Profile, User Data, and App Data sections

## Metadata
- **Created**: Monday, January 12, 2026 at 11:26:59 AM PST
- **Completed**: Sunday, January 18, 2026 at 11:45:00 PM PST
- **Parent Work Effort**: WE-260112-l7tt
- **Author**: ctavolazzi

## Description
Add User Profile, User Data, and App Data sections to the UI with corresponding API endpoints.

## Acceptance Criteria
- [x] User Profile section showing: name, story count, total word count, first story date, preferred style
- [x] User Data section showing: user's stories, timeline, statistics
- [x] App Data section showing: total stories, recent stories, app-wide statistics
- [x] API endpoints: /api/profile, /api/user-data, /api/app-data
- [x] Data updates when new stories are created

## Files Changed
- `src/waft/core/campfire.py` - get_user_profile(), get_user_data(), get_app_data() methods and UI sections

## Implementation Notes
- User Profile: Calculates stats from all stories (single-user mode for now)
- User Data: Returns user's stories with timeline and statistics
- App Data: Returns app-wide stats including total stories, words, recent stories, popular styles
- All sections load via API on page load
- Data automatically refreshes after story creation
- Single-user mode: All stories treated as "user" stories (multi-user support can be added later)

## Commits
- Implementation completed in prior work (2026-01-12)
- Verified and tested (2026-01-18)
