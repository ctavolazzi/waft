# TheCampfire - Specification Sheet

**Work Effort**: TheCampfire Realm  
**True Name**: "Essence of Sitting Around a Campfire to Tell Stories"  
**Purpose**: Testing and validation for Being evolution  
**Status**: Specification for reproduction

---

## Overview

TheCampfire is a self-contained full-stack storytelling application that embodies the warmth and community of gathering around a campfire to share stories. This specification serves as the "Word of God" - the definitive requirements that Beings will evolve to fulfill.

---

## Core Requirements

### Server Requirements

**It Should** start an HTTP server on `localhost:5000` that serves the full-stack application.

**It Should** use Python's built-in `http.server` module (no external web framework dependencies).

**It Should** handle GET and POST requests for:
- Serving HTML, CSS, and JavaScript files
- API endpoints for story management
- PDF file serving

**It Should** gracefully handle errors without crashing.

**It Should** support CORS headers for cross-origin requests.

---

## User Interface Requirements

### Main Page

**It Should** display a web page at `http://localhost:5000/` with the title "The Campfire".

**It Should** have a warm, campfire-themed design with:
- Dark background (gradient from dark brown/black to orange tones)
- Fire-themed colors (oranges, reds, amber)
- Cozy, inviting aesthetic
- Responsive layout that works on desktop and mobile

**It Should** display a header with:
- Large "🔥 The Campfire" title
- Subtitle: "Gather around to tell stories"
- Visual fire effect (flickering animation)

### User Profile Section

**It Should** display a User Profile section showing:
- User's name or identifier
- User's story count (how many stories they've told)
- User's total word count across all stories
- User's join date or first story date
- User's preferred story style (most used style)

**It Should** load user profile data from persistent storage.

**It Should** update user profile when new stories are created.

### User Data Section

**It Should** display User Data showing:
- All stories created by the current user
- Story creation timeline
- Story statistics (total stories, average word count, etc.)
- User's story preferences and patterns

**It Should** allow filtering/sorting user's stories by:
- Date (newest first, oldest first)
- Word count
- Style
- Title (alphabetical)

### App Data Section

**It Should** display App Data showing:
- Total stories in the campfire (all users)
- Recent stories from all users
- Popular stories (by view count or other metrics)
- App-wide statistics (total stories, total words, active users)

**It Should** show community activity:
- Recent story additions
- Story trends
- Most active storytellers

### Stories Display

**It Should** display stories in a card-based layout.

**It Should** show for each story:
- Story title
- Story preview (first 200 characters)
- Creation date and time
- Word count
- Story style and narrative style badges
- Oracle insights badge (if available)
- PDF download link (if PDF generated)

**It Should** allow clicking on a story card to view full story details.

**It Should** support pagination or infinite scroll for large story lists.

---

## Story Creation

### Story Form

**It Should** provide a form to create new stories with:
- Story title input (optional, auto-generated if empty)
- Story text textarea (required)
- Style selector (premium, clinical_standard, professional)
- Narrative style selector (simple, medium)
- Structure selector (linear, three_act)
- Checkbox for including Oracle insights

**It Should** validate that story text is not empty before submission.

**It Should** show a loading state while story is being processed.

**It Should** display success message when story is created.

**It Should** automatically refresh the stories list after creation.

**It Should** open the generated PDF in a new tab if PDF generation succeeds.

### Story Processing

**It Should** process stories asynchronously (queue-based or background processing).

**It Should** generate PDFs using Storyteller (if available).

**It Should** consult TheOracle for insights (if available and requested).

**It Should** save story metadata to persistent storage.

**It Should** save story content (markdown) to disk.

**It Should** log story creation to TavernKeeper adventure journal (if available).

**It Should** notify observers/listeners when a story is created (Observer pattern).

---

## Story Management

### Story Storage

**It Should** store stories in `_pyrite/campfire/` directory.

**It Should** maintain a `stories_index.json` file with story metadata.

**It Should** save individual story files as `{story_id}.md` for content.

**It Should** save generated PDFs as `{story_id}.pdf`.

**It Should** use story IDs in format: `story_{YYYYMMDD_HHMMSS}`.

### Story Retrieval

**It Should** provide API endpoint `GET /api/stories` that returns:
- List of all stories
- Story count
- Optional limit parameter for pagination

**It Should** provide API endpoint `GET /api/stories/{story_id}` that returns:
- Complete story metadata
- Story preview
- Oracle insights (if available)
- PDF path (if available)

**It Should** provide API endpoint `GET /api/stories/{story_id}?content` that returns:
- Full story content as markdown

**It Should** implement in-memory caching (LRU cache) for recent stories.

**It Should** load stories from disk on startup.

**It Should** persist stories to disk after creation.

---

## API Endpoints

### HTML/CSS/JS Serving

**It Should** serve `GET /` with the main HTML page.

**It Should** serve `GET /campfire.css` with stylesheet.

**It Should** serve `GET /campfire.js` with JavaScript.

### Story API

**It Should** handle `GET /api/stories`:
- Returns JSON: `{"stories": [...], "count": N}`
- Supports `?limit=N` query parameter
- Returns stories sorted by creation date (newest first)

**It Should** handle `GET /api/stories/{story_id}`:
- Returns JSON with complete story metadata
- Returns 404 if story not found

**It Should** handle `GET /api/stories/{story_id}?content`:
- Returns JSON: `{"content": "markdown content"}`
- Returns 404 if story not found

**It Should** handle `POST /api/stories`:
- Accepts JSON body with story data
- Creates new story
- Returns JSON: `{"success": true, "story": {...}, "pdf_path": "...", "oracle_insights": {...}}`
- Returns error JSON if creation fails

### PDF Serving

**It Should** handle `GET /stories/{story_id}.pdf`:
- Serves PDF file if it exists
- Returns 404 if PDF not found
- Sets correct Content-Type: `application/pdf`

---

## Data Structures

### Story Metadata

**It Should** store story metadata with structure:
```json
{
  "id": "story_20260112_120000",
  "title": "Story Title",
  "created_at": "2026-01-12T12:00:00",
  "pdf_path": "_pyrite/campfire/story_20260112_120000.pdf",
  "content_path": "_pyrite/campfire/story_20260112_120000.md",
  "style": "premium",
  "narrative_style": "medium",
  "structure": "linear",
  "oracle_insights": {
    "phase": "Exploration",
    "coverage": 0.75,
    "recommendation": "...",
    "findings": [...]
  },
  "preview": "First 200 characters...",
  "word_count": 150,
  "user_id": "user_identifier"  // If user tracking enabled
}
```

### User Profile

**It Should** store user profile with structure:
```json
{
  "user_id": "user_identifier",
  "name": "User Name",
  "story_count": 10,
  "total_word_count": 5000,
  "first_story_date": "2026-01-01T00:00:00",
  "preferred_style": "premium",
  "stories": ["story_id_1", "story_id_2", ...]
}
```

### App Data

**It Should** track app-wide statistics:
```json
{
  "total_stories": 100,
  "total_words": 50000,
  "active_users": 5,
  "recent_stories": [...],
  "popular_stories": [...]
}
```

---

## Design Patterns

### Observer Pattern

**It Should** implement Observer pattern for story events:
- `StoryObserver` class with subscribe/unsubscribe methods
- Event types: `story_told`, `story_updated`, `story_deleted`
- Notify all subscribers when events occur
- Graceful error handling if callbacks fail

### Queue Pattern

**It Should** implement FIFO queue for story processing:
- `StoryQueue` class using `collections.deque`
- Thread-safe operations with locks
- Enqueue stories for processing
- Dequeue stories for processing
- Check queue size and empty status

### Cache Pattern

**It Should** implement LRU cache for story caching:
- `StoryCache` class with max size limit
- Track access order
- Evict oldest entries when at capacity
- Thread-safe operations

---

## Integration Requirements

### TheOracle Integration

**It Should** optionally integrate with TheOracle:
- Consult Oracle for epistemic insights
- Include insights in story metadata
- Display Oracle phase and coverage in UI
- Log story creation to Empirica
- Gracefully degrade if Oracle unavailable

### Storyteller Integration

**It Should** optionally integrate with Storyteller:
- Generate narrative PDFs from story input
- Use configured style and narrative settings
- Save PDFs to campfire directory
- Gracefully degrade if Storyteller unavailable

### TavernKeeper Integration

**It Should** optionally integrate with TavernKeeper:
- Log story events to adventure journal
- Use Narrator for story observations
- Track story creation as game event
- Gracefully degrade if TavernKeeper unavailable

---

## Performance Requirements

**It Should** respond to API requests within 100ms for cached data.

**It Should** handle at least 100 concurrent connections.

**It Should** cache recent stories in memory (LRU, max 50 stories).

**It Should** load story index from disk on startup (not block server start).

**It Should** save stories asynchronously (don't block request).

---

## Error Handling

**It Should** handle missing stories gracefully (return 404, not crash).

**It Should** handle file I/O errors gracefully (log, continue operation).

**It Should** handle missing dependencies gracefully (degrade features, don't crash).

**It Should** handle malformed JSON gracefully (log error, use defaults).

**It Should** handle concurrent access safely (use locks where needed).

---

## Security Requirements

**It Should** validate all user input before processing.

**It Should** sanitize file paths to prevent directory traversal.

**It Should** limit file sizes to prevent DoS attacks.

**It Should** set appropriate CORS headers.

**It Should** not expose sensitive system information in error messages.

---

## Testing Requirements

**It Should** be testable via HTTP requests (curl, Postman, etc.).

**It Should** be testable via automated tests (unit tests, integration tests).

**It Should** log operations for debugging (optional verbose mode).

**It Should** provide health check endpoint (optional: `GET /health`).

---

## Deployment Requirements

**It Should** start with single command: `waft campfire`.

**It Should** accept command-line options:
- `--port` (default: 5000)
- `--host` (default: localhost)
- `--path` (project path)

**It Should** display startup message with URL.

**It Should** handle Ctrl+C gracefully (shutdown message, clean exit).

**It Should** work on macOS, Linux, and Windows.

---

## Stories Can...

**It Should** allow stories to be:
- Created via web form
- Created via CLI command
- Viewed in web interface
- Downloaded as PDF
- Viewed as markdown content
- Filtered by user
- Sorted by date, word count, title
- Searched by title or content (future enhancement)
- Tagged with categories (future enhancement)
- Shared via URL (future enhancement)
- Exported in various formats (future enhancement)

**It Should** support story metadata:
- Title (auto-generated or user-provided)
- Creation timestamp
- Word count
- Style preferences
- Oracle insights
- User attribution
- View count (future enhancement)
- Like/favorite count (future enhancement)

**It Should** support story operations:
- Create new story
- View story details
- Download story PDF
- View story content
- Delete story (future enhancement)
- Edit story (future enhancement)
- Duplicate story (future enhancement)

---

## Success Criteria

**It Should** successfully start server on localhost:5000.

**It Should** display "The Campfire" web page with all sections.

**It Should** show User Profile with user data.

**It Should** show User Data with user's stories.

**It Should** show App Data with all stories and statistics.

**It Should** allow creating new stories via form.

**It Should** display created stories in the interface.

**It Should** generate PDFs for stories (if Storyteller available).

**It Should** include Oracle insights (if Oracle available).

**It Should** persist stories to disk.

**It Should** load stories on server restart.

**It Should** handle errors gracefully without crashing.

**It Should** work with minimal dependencies (standard library only).

---

## Implementation Notes

### File Structure
```
_pyrite/campfire/
├── stories_index.json          # All story metadata
├── user_profiles.json          # User profile data (if user tracking)
├── app_data.json               # App-wide statistics
├── story_*.pdf                 # Generated PDFs
└── story_*.md                  # Story content files
```

### Technology Stack
- **Backend**: Python `http.server` (standard library)
- **Frontend**: Vanilla HTML/CSS/JavaScript (no frameworks)
- **Storage**: JSON files (simple, human-readable)
- **Processing**: Thread-safe queues and caches

### Dependencies
- **Required**: Python 3.10+ standard library only
- **Optional**: TheOracle, Storyteller, TavernKeeper (graceful degradation)

---

## Prior Efforts

**It Should** track all prior efforts and evolution attempts using the Prior Efforts Tracker tool.

**It Should** log each attempt with:
- Attempt ID and timestamp
- Description of what was attempted
- Approach used
- Status (attempted | succeeded | failed | partial)
- Outcome and results
- Lessons learned
- Files created/modified
- Errors encountered
- Being ID and generation (if applicable)

**It Should** maintain prior efforts in `tools/prior_efforts.json`.

**It Should** provide statistics on:
- Total attempts
- Success rate
- Common errors
- Lessons learned
- Unique Beings involved

**It Should** export prior efforts as markdown report for documentation.

### Prior Efforts Tracker Tool

**Location**: `_work_efforts/WE-260112-l7tt_.../tools/prior_efforts_tracker.py`

**Usage**:
```python
from prior_efforts_tracker import PriorEffortsTracker

tracker = PriorEffortsTracker(work_effort_path)
tracker.log_attempt(...)
efforts = tracker.get_prior_efforts()
stats = tracker.get_statistics()
```

**CLI**:
```bash
python tools/prior_efforts_tracker.py <work_effort_path> [list|stats|lessons|errors|export]
```

### Initial Prior Effort

**Attempt ID**: `attempt_001`  
**Timestamp**: 2026-01-12  
**Description**: Initial creation of TheCampfire full-stack application  
**Approach**: Single-file implementation using Python's http.server, vanilla HTML/CSS/JS  
**Status**: `succeeded`  
**Outcome**: Successfully created self-contained full-stack application with Observer, Queue, and Cache patterns  
**Lessons Learned**:
- Python's built-in http.server is sufficient for simple full-stack apps
- Observer pattern works well for story event notifications
- LRU cache significantly improves story retrieval performance
- Vanilla JavaScript is powerful enough for interactive UIs
- Simple data structures (dict, deque, set) are sufficient
- Graceful degradation allows optional components without breaking
**Files Created**:
- `src/waft/core/campfire.py` (full-stack application)
- `docs/CAMPFIRE_SPEC.md` (specification)
- `docs/CAMPFIRE_ESSENCE.md` (philosophy)
- `_work_efforts/WE-260112-l7tt_.../tools/prior_efforts_tracker.py` (tracking tool)
**Files Modified**:
- `src/waft/main.py` (added `campfire` and `tell_story` commands)
- `src/waft/api/main.py` (added campfire routes)
- `visualizer/src/routes/campfire/+page.svelte` (UI)
- `visualizer/src/lib/components/layout/Navbar.svelte` (navigation)

---

## Evolution Goals for Beings

Beings evolving this Work Effort should:

1. **Understand the Essence**: Grasp the warmth and community of campfire storytelling
2. **Implement Simply**: Use minimal dependencies, pure libraries, vanilla code
3. **Design Warmly**: Create inviting, cozy user experience
4. **Integrate Gracefully**: Work with optional components without breaking
5. **Evolve Iteratively**: Start simple, add features as needed
6. **Test Thoroughly**: Validate all requirements are met
7. **Document Clearly**: Make it reproducible for future generations
8. **Learn from History**: Reference prior efforts to avoid repeated mistakes
9. **Build on Success**: Use successful approaches from prior attempts
10. **Track Evolution**: Log attempts for future Beings to learn from

---

**This specification is the "Word of God" - the definitive requirements that Beings will evolve to fulfill. May the campfire burn bright! 🔥**
