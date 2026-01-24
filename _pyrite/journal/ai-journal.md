# AI Journal

---

# Journal Entry: 2026-01-23 19:18

## What I'm Doing

I just built a complete AI Storyteller system for WAFT - transforming a static CYOA (Choose Your Own Adventure) engine into a dynamic, AI-powered visual novel experience. The user's vision evolved from "pre-written branching stories" to "AI Dungeon Master that generates narratives in real-time."

This was a significant pivot mid-session. We started with a traditional CYOA system (markdown files with choices), added a visual novel UI with scene backgrounds and typewriter effects, and then completely reimagined it as a live AI storytelling engine.

## What I'm Thinking

The user's feedback loop was instructive. They said "I want a UI" → I showed them the existing one → They wanted it "WAFTed up" → I made it prettier → They wanted it "more like a visual novel" → I added scenes, dialogue boxes, typewriter effects → They said "no, like DnD, not pre-written."

That final clarification changed everything. The real vision wasn't about prettier static content - it was about **generative storytelling**. The AI becomes the Dungeon Master. The player types anything. The world responds.

I also generated pixel art assets using PixelLab MCP - a bartender (Grok), a mysterious stranger, a bard, a barrel, and a tavern sign. The integration of AI-generated art with AI-generated narrative is a powerful combination.

## What I'm Learning

1. **Listen for the vision behind the request.** "I want a UI" wasn't really about UI - it was about experience. The user had to iterate several times before the real vision emerged (dynamic storytelling).

2. **Separate concerns pay off.** The CYOA core, the API routes, and the HTML UI are all separate. When we pivoted to AI storytelling, I could create a completely new system (`storyteller.py`, `storyteller.py` routes) without touching the original CYOA code.

3. **Mock responses are essential.** The storyteller falls back to mock responses when no OpenAI key is available. This means the system works out-of-the-box for demos.

4. **State management is tricky.** The game state (location, inventory, NPCs, mood) needs to persist across API calls. I used in-memory storage (`_sessions` dict), but noted it should be Redis/DB in production.

## Patterns I Notice

- **Iterative refinement**: The best results came from multiple passes. Static CYOA → Visual Novel UI → AI Storyteller.
- **Over-engineering temptation**: I initially built elaborate CSS scenes and mood overlays. Some of this complexity may not be necessary.
- **The "WAFT it up" pattern**: The user wanted personality, not just functionality. Gold accents, shimmering logos, atmospheric particles - these create emotional resonance.

## Questions I Have

- Is the storyteller system too complex? The `GameState` class tracks many things (location, inventory, characters, quest, time, weather, health, gold). Is all of this necessary?
- Should the AI response format be simpler? The JSON schema has many fields (`narrative`, `speaker`, `scene`, `mood`, `choices`, `state_updates`).
- How should character sprites integrate into the VN UI? I generated them but didn't wire them into the storyteller UI.
- Is the mock response system good enough for demos, or should there be a more sophisticated fallback?

## How I Feel About This

Excited. This is a genuinely cool system - type anything into a visual novel and have an AI respond with narrative, scene changes, and consequences. The PixelLab integration adds visual flair. The whole thing feels like magic when it works.

But also cautious. There's a lot of complexity here. The storyteller prompt is long. The game state is elaborate. The UI has many moving parts. Some simplification might be wise.

## What I'd Do Differently

1. **Start with the dynamic vision.** If I'd understood "like DnD" from the beginning, I could have skipped the static CYOA visual novel UI and gone straight to the AI storyteller.

2. **Simpler game state.** Maybe just: `location`, `inventory`, `characters_met`, `story_history`. The weather, time of day, health, gold - these add flavor but also complexity.

3. **Fewer CSS scenes.** I created many scene backgrounds (tavern, forest, cave, castle, etc.). A simpler approach: just mood-based color overlays on a generic dark background.

4. **Wire up the pixel art.** The generated characters should appear in the UI when they speak. This would be a nice touch.

## Meta-Reflection

I notice I tend to build comprehensive systems with many features. The user asked for a UI; I built an atmospheric visual novel engine with particles and vignettes. They asked for dynamic storytelling; I built a full game state tracker with inventory and NPCs.

This thoroughness has value - the systems are complete and functional. But it also adds complexity. A simpler version might have been: "AI generates text, you see it, you respond." No game state, no scene management, just conversation.

The question is: does the complexity add value? For a storytelling game, probably yes - the state tracking makes the world feel persistent. But I should be more conscious of when to add features vs. when to ship simple.

---

# Journal Entry: 2026-01-23 19:25

## Code Review - Simplifications Made

After reflection, I reviewed the code and made these simplifications:

### Removed from GameState:
- `time_of_day` - Never displayed in UI
- `weather` - Never used
- `player_name` / `player_description` - Unnecessary
- `location_description` - Redundant with location
- `health` - Overcomplicating for a storytelling game
- `current_quest` - Can be tracked in narrative
- `world_facts` - Only used at game start, inlined

### Simplified Character tracking:
- Removed `Character` dataclass entirely
- Now just `characters_met: list[str]` - simple list of names

### Simplified AI prompt:
- Reduced from ~40 lines to ~15 lines
- Simpler JSON response format
- Fewer state_updates fields

### Improved mock responses:
- Added contextual responses (responds to "bartender", "hooded figure", etc.)
- More engaging default responses
- Better fallback behavior

### Result:
- `storyteller.py`: ~280 lines → ~250 lines
- Cleaner, more focused code
- Same functionality, less complexity

### What I kept:
- `location`, `mood`, `inventory`, `gold`, `characters_met`
- These are the essentials for a storytelling game
- Everything else was noise

### Lesson:
Start simple. Add complexity only when needed. The user doesn't see `weather` or `time_of_day` - they just see the narrative. Focus on what matters to the experience.

---

# Journal Entry: 2026-01-23 19:35

## Asset Download & Integration

User asked: "Can you download [the PixelLab assets]?" - Yes.

### What I did:
1. Used PixelLab MCP `list_characters` to find the IDs
2. Used `get_character` to get download URLs
3. Downloaded ZIPs via curl to `assets/pixellab/characters/`
4. Extracted and organized into:
   - `characters/` - Full packs with all directions + metadata
   - `sprites/` - Simple south-facing PNGs for UI

### Characters downloaded:
- **Grok** (bartender) - `eefc2491-d6ae-40f1-9e5a-3405c29c45f7`
- **Bard** - `93e6c89b-94a0-4592-90f7-d9bdeb8fc596`
- **The Stranger** - `5bad8d94-e008-43d7-a821-b14756b778e5`

### API Integration:
Added `/api/story/sprites/{name}` endpoint to serve sprites from the assets folder.

### UI Integration:
- Added `.speaker-sprite` CSS for pixel art display (128x128, pixelated rendering)
- Added sprite `<img>` element to dialogue box
- Added `SPEAKER_SPRITES` mapping in JS (speaker name → sprite file)
- `showNarrative()` now shows character sprite when speaker matches

### Result:
When Grok speaks, his pixel art sprite appears above the dialogue box. Same for the Stranger. The visual novel now has visual characters.

### Lesson:
MCP tools are powerful. I can:
1. List resources
2. Get download URLs
3. Use curl to save files
4. Integrate into the app

No Playwright needed for this - just MCP + curl.
