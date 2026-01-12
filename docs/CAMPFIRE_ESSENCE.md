# TheCampfire - The Essence of Sitting Around a Campfire to Tell Stories

**True Name**: "Essence of Sitting Around a Campfire to Tell Stories"

A self-contained full-stack application that embodies the warmth, community, and magic of gathering around a campfire to share stories.

---

## Philosophy

TheCampfire is not just a tool - it's an experience. It captures the essence of:
- **Warmth**: The glow of stories shared in community
- **Community**: Stories belong to everyone around the fire
- **Magic**: The transformation of words into narrative
- **Simplicity**: No complexity, just stories

---

## Architecture

### Design Patterns

1. **Observer Pattern** (`StoryObserver`)
   - Stories notify listeners when told
   - Simple callback system
   - Event-driven architecture

2. **Queue Pattern** (`StoryQueue`)
   - FIFO queue for story processing
   - Thread-safe with locks
   - Simple deque data structure

3. **Cache Pattern** (`StoryCache`)
   - LRU cache for recent stories
   - In-memory with disk persistence
   - Automatic eviction

4. **Singleton-like**: One campfire per project
   - Shared state for stories
   - Centralized event system

### Data Structures

- **Dictionary**: Story storage (O(1) lookup)
- **Deque**: Story queue (FIFO, O(1) operations)
- **Set**: Observer listeners (O(1) add/remove)
- **List**: Story index (sorted by date)

### Algorithms

- **FIFO Queue**: Simple story processing
- **LRU Cache**: Recent story access
- **Merge Sort**: Story sorting by date
- **Simple Search**: Linear search for story lookup

---

## Dependencies

**Minimal - Pure Libraries Only**:
- Python standard library (`http.server`, `json`, `threading`, `collections`)
- Optional: TheOracle, Storyteller, TavernKeeper (graceful degradation)

**No Heavy Frameworks**:
- No React, Vue, Angular
- No Express, Django, Flask
- Just vanilla HTML/CSS/JavaScript
- Just Python's built-in HTTP server

---

## Usage

### Start TheCampfire

```bash
waft campfire
```

This starts the full-stack application on `http://localhost:8782`

### Tell a Story via CLI

```bash
waft tell-story "Your story here" --title "My Story"
```

Stories are automatically saved and available in TheCampfire.

### Tell a Story via Web UI

1. Start TheCampfire: `waft campfire`
2. Open browser: `http://localhost:8782`
3. Click "+ Tell a Story"
4. Enter your story
5. Click "Tell Story Around the Fire"

---

## API Endpoints

### `GET /`
Campfire HTML page

### `GET /campfire.css`
Campfire stylesheet

### `GET /campfire.js`
Campfire JavaScript

### `GET /api/stories`
List all stories (optional `?limit=N`)

### `GET /api/stories/{story_id}`
Get specific story

### `GET /api/stories/{story_id}?content`
Get story content (markdown)

### `POST /api/stories`
Create new story
```json
{
  "story": "Your story text",
  "title": "Optional title",
  "style": "premium",
  "narrative_style": "medium",
  "include_oracle": true
}
```

### `GET /stories/{story_id}.pdf`
Download story PDF

---

## File Structure

```
_pyrite/campfire/
├── stories_index.json          # Story metadata index
├── story_20260112_120000.pdf   # Generated PDFs
└── story_20260112_120000.md    # Story content
```

---

## Design Principles

1. **EASY**: Simple, intuitive, no complexity
2. **LIMITED DEPENDENCIES**: Pure libraries, vanilla code
3. **CLEVER CONFIGURATION**: Smart use of simple patterns
4. **GRACEFUL DEGRADATION**: Works even if components unavailable
5. **WARM AESTHETICS**: Campfire-themed, cozy, inviting

---

## Integration

TheCampfire orchestrates:
- **TheOracle**: Epistemic insights (optional)
- **Storyteller**: Narrative generation (optional)
- **TavernKeeper**: Adventure journal logging (optional)

All components work together, but TheCampfire works even if they're unavailable.

---

**TheCampfire - Where stories come to life around the digital fire.**
