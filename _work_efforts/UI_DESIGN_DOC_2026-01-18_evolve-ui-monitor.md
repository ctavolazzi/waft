# Evolve UI Monitor - Design Document

**Date**: 2026-01-18 07:27:00 PST
**Status**: Design Phase (Pre-Implementation)

---

## What Was Observed

### User Request
"I want a UI to exist where we can monitor runs of the evolve the UI command"

### Current State
- `/evolve-a-ui` command exists and creates UIs
- Outputs saved to `_genetics/ui_evolution/`
- Creates files: `{timestamp}_evolved_ui.html`, `{timestamp}_context_analysis.md`
- Screenshots saved to `_work_efforts/` (e.g., `{timestamp}_wireframe.png`)
- Case files created in `_work_efforts/proof_cases/`
- Design docs and requirements in `_work_efforts/`
- Process is methodical with multiple phases

### Existing Artifacts
- Found 10+ evolved UI files in `_genetics/ui_evolution/`
- Multiple context analysis files
- Screenshots and case files scattered in work efforts

---

## The Problem This UI Solves

**Problem**: There's no way to:
- **See** when `/evolve-a-ui` was run
- **Track** what it produced (HTML files, screenshots, case files)
- **Monitor** the evolution process progress
- **Review** all generated artifacts in one place
- **Understand** the relationship between runs (which screenshots belong to which run)
- **Navigate** to generated UIs easily

**Current State**: Artifacts scattered across multiple directories, no central view

**Desired State**: Central dashboard showing all evolve-a-ui runs and their artifacts

---

## Purpose of This UI

**Primary Purpose**: 
**Monitor and track all `/evolve-a-ui` command executions** - Show when it ran, what it produced, and provide easy access to all generated artifacts.

**Secondary Purposes**:
- **Track Process**: Show which phase each run is in
- **Display Artifacts**: List all generated files (HTML, screenshots, case files, docs)
- **Show Progress**: Visual timeline of evolution process
- **Link Evidence**: Connect screenshots to runs, case files to decisions
- **Navigate Easily**: Quick access to generated UIs

---

## What This UI Should Accomplish

1. **List All Runs**
   - Show all `/evolve-a-ui` executions
   - Timestamp, chat context, status
   - Current phase (Analysis, Requirements, Wireframe, Development, Complete)

2. **Display Generated Artifacts**
   - HTML files created
   - Screenshots taken (with thumbnails)
   - Case files generated
   - Design documents
   - Requirements documents

3. **Show Process Progress**
   - Which phase the run is in
   - Steps completed
   - Screenshots showing progress
   - Timeline of development

4. **Link Related Files**
   - Connect screenshots to runs
   - Link case files to decisions
   - Show design doc → requirements → wireframe → HTML flow

5. **Provide Navigation**
   - Quick links to view generated UIs
   - Download/view screenshots
   - Open case files
   - View design docs

---

## Key Features Needed

1. **Runs List**: Table/list of all evolve-a-ui executions
2. **Run Details**: Expandable view showing artifacts for each run
3. **Artifact Gallery**: Visual display of screenshots, HTML previews
4. **Process Timeline**: Show progress through phases
5. **File Browser**: Navigate to generated files
6. **Search/Filter**: Find runs by date, context, phase

---

## Data Sources

1. **`_genetics/ui_evolution/`**: HTML files, context analysis
2. **`_work_efforts/`**: Design docs, requirements, screenshots
3. **`_work_efforts/proof_cases/`**: Case files
4. **File timestamps**: Determine run times
5. **File naming patterns**: Extract run IDs, phases

---

## What Makes This Different

This is a **meta-monitoring UI** - it monitors the UI creation process itself. It shows:
- **Process visibility**: See the methodical evolution happening
- **Artifact organization**: All related files in one place
- **Progress tracking**: Visual timeline of development
- **Evidence linking**: Connect proof to decisions

---

## Success Criteria

The UI succeeds when:
- ✅ User can see all evolve-a-ui runs
- ✅ User can access all generated artifacts
- ✅ User understands process progress
- ✅ User can navigate to generated UIs easily
- ✅ User can see relationships between files

---

## User Persona

**Primary User**: Developer using WAFT framework
- Wants to track UI evolution runs
- Needs to find generated UIs
- Wants to review evolution process
- Interested in seeing progress and artifacts

---

## Use Cases

1. **After running `/evolve-a-ui`**: See the run appear in monitor
2. **Finding a UI**: Search for a specific evolved UI
3. **Reviewing process**: See how a UI was developed (screenshots, phases)
4. **Checking progress**: See which phase a run is in
5. **Accessing artifacts**: Quick links to HTML files, screenshots, case files

---

## Interaction Model

**Primary Mode**: **View-Only Dashboard**
- Display runs list
- Show artifacts
- Display progress
- Provide navigation links

**Future Interactions** (Phase 2):
- Filter runs by date/phase
- Search runs by context
- Delete old runs
- Re-run evolution

---

**This UI makes the UI evolution process visible and trackable.**
