# TheCampfire System

**Created**: 2026-01-12  
**Status**: ✅ Complete  
**Purpose**: Gather around the campfire to tell stories using TheOracle, Storyteller, and TavernKeeper

---

## Overview

TheCampfire is a storytelling orchestration system that brings together:
- **TheOracle** - Provides epistemic insights about stories
- **Storyteller** - Converts input into narrative prose and PDFs
- **TavernKeeper/Narrator** - Adds narrative elements and logs to adventure journal

All stories are saved and displayed via a full-stack FastAPI + SvelteKit application.

---

## Architecture

### Backend (Python/FastAPI)

**TheCampfire Class** (`src/waft/core/campfire.py`):
- Orchestrates all three components
- Manages story storage in `_pyrite/campfire/`
- Creates story metadata and indexes
- Generates PDFs with Oracle insights

**API Routes** (`src/waft/api/routes/campfire.py`):
- `POST /api/campfire/stories` - Create a new story
- `GET /api/campfire/stories` - List all stories
- `GET /api/campfire/stories/{story_id}` - Get specific story
- `GET /api/campfire/stories/{story_id}/content` - Get story content

### Frontend (SvelteKit)

**Campfire Page** (`visualizer/src/routes/campfire/+page.svelte`):
- Beautiful campfire-themed UI
- Story creation form
- Story gallery with cards
- PDF viewing
- Oracle insights display

---

## Usage

### CLI Command

```bash
waft tell-story "Your story text here" --title "My Story"
```

This command now uses TheCampfire internally to:
1. Gather around the campfire
2. Consult TheOracle for insights
3. Generate narrative PDF
4. Save story to campfire
5. Open PDF automatically

### Web Interface

1. Start the FastAPI server:
   ```bash
   waft serve
   ```

2. Start the SvelteKit dev server (in `visualizer/`):
   ```bash
   cd visualizer
   npm run dev
   ```

3. Navigate to: `http://localhost:5173/campfire`

4. Tell your story using the form!

### API Usage

```python
from waft.core.campfire import TheCampfire
from pathlib import Path

campfire = TheCampfire(Path('.'))

result = campfire.gather_around_the_campfire(
    story_input="Once upon a time...",
    title="My Story",
    style="premium",
    include_oracle=True
)

print(f"Story ID: {result['story']['id']}")
print(f"PDF: {result['pdf_path']}")
```

---

## Story Storage

Stories are stored in `_pyrite/campfire/`:

```
_pyrite/campfire/
├── stories_index.json      # Metadata index
├── story_20260112_120000.pdf
├── story_20260112_120000.md
├── story_20260112_130000.pdf
└── story_20260112_130000.md
```

**Story Metadata** includes:
- ID, title, creation timestamp
- PDF and content paths
- Style and narrative settings
- Oracle insights (if available)
- Preview text and word count

---

## Features

### ✅ Complete Integration
- TheOracle provides epistemic insights
- Storyteller generates narrative PDFs
- TavernKeeper logs to adventure journal
- All components work together seamlessly

### ✅ Full-Stack Application
- FastAPI backend with REST API
- SvelteKit frontend with beautiful UI
- Story storage and retrieval
- PDF generation and viewing

### ✅ Graceful Degradation
- Works without Empirica (Oracle optional)
- Continues if Oracle unavailable
- Saves stories even if PDF generation fails

### ✅ Beautiful UI
- Campfire-themed design
- Story cards with previews
- Oracle insights badges
- PDF viewing integration

---

## Components

### TheCampfire Class

**Main Method**: `gather_around_the_campfire()`

**Workflow**:
1. Consult TheOracle (if available)
2. Enhance story with Oracle insights
3. Create Storyteller with TavernKeeper's Narrator
4. Generate narrative PDF
5. Save story metadata and content
6. Log to TavernKeeper adventure journal

**Storage Methods**:
- `get_stories()` - List all stories
- `get_story()` - Get specific story
- `get_story_content()` - Get story markdown

---

## Integration Points

### With /tell-story Command

The CLI command now uses TheCampfire:
```python
campfire = TheCampfire(project_path)
result = campfire.gather_around_the_campfire(...)
```

### With FastAPI

API routes use TheCampfire for all operations:
- Story creation
- Story listing
- Story retrieval
- Content access

### With SvelteKit

Frontend calls API endpoints to:
- Display stories
- Create new stories
- View PDFs
- Show Oracle insights

---

## Future Enhancements

Potential additions:
- Story editing
- Story sharing/export
- Story search and filtering
- Story tags and categories
- Story comments/annotations
- Story versioning
- Collaborative storytelling

---

## Technical Details

### Dependencies
- FastAPI (already in project)
- SvelteKit (already in project)
- TheOracle (requires Empirica, optional)
- Storyteller (requires PDFGenerator)
- TavernKeeper (requires TinyDB, optional)

### File Structure
```
src/waft/
├── core/
│   └── campfire.py          # TheCampfire class
└── api/
    └── routes/
        └── campfire.py      # API routes

visualizer/src/routes/
└── campfire/
    ├── +page.svelte         # Campfire UI
    └── +page.ts             # Page config
```

---

**TheCampfire brings together TheOracle, Storyteller, and TavernKeeper to create a beautiful storytelling experience around the digital campfire.**
