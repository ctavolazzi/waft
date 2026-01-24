---
id: TKT-in0a-006
parent: WE-260120-in0a
title: "ODD research notes web app (FastAPI + SvelteKit)"
status: in_progress
created: 2026-01-21T05:38:29.279Z
created_by: ctavolazzi
assigned_to: null
---

# TKT-in0a-006: ODD research notes web app (FastAPI + SvelteKit)

## Metadata
- **Created**: Tuesday, January 20, 2026 at 9:38:29 PM PST
- **Parent Work Effort**: WE-260120-in0a
- **Author**: ctavolazzi

## Description
Create a new ODD research notes web page linked to existing ODD page, backed by FastAPI storage, and update /bananote to open the site + keep bananote notes.

## Acceptance Criteria
- [ ] New SvelteKit ODD research page exists and links to existing ODD page
- [ ] Existing ODD page links to new research page
- [ ] FastAPI endpoints for ODD research notes (read + write)
- [ ] /bananote command updated to open browser on the new page
- [ ] Bananote notes updated with science references and design notes

## Files Changed
- `.cursor/commands/bananote.md`
- `_realms/odd_realm/index.html`
- `_realms/odd_realm/notes/odd_research_notes.json`
- `src/waft/api/routes/odd_notes.py`
- `visualizer/src/lib/components/layout/Navbar.svelte`
- `visualizer/src/routes/odd-notes/+page.svelte`
- `_work_efforts/WE-260120-in0a_odd_realm_creative_expansion/bananote_odd_research_notes_2026-01-20.typ`
- `_work_efforts/WE-260120-in0a_odd_realm_creative_expansion/bananote_odd_research_notes_2026-01-20.pdf`
- `_work_efforts/devlog.md`

## Implementation Notes
- 1/20/2026: Port for notes UI set to 5173 (SvelteKit default). Browser check failed because SvelteKit dev server is not running; FastAPI API expected at http://localhost:8000.
- 1/20/2026: Adjusted ODD notes URL to use SvelteKit default port 5173 to avoid conflict with the card game on 3000.
- 1/20/2026: Added ODD research notes API + seed JSON, created SvelteKit /odd-notes page with ODD styling, linked from ODD index to the notes UI, and updated /bananote to open the notes page. Bananote science notes compiled with scienceicons.
- (decisions, blockers, context)

## Commits
- (populated as work progresses)
