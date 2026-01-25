# Teleport Massive Writer

> A sophisticated storytelling and worldbuilding module for the Teleport Massive universe.
> Designed for Terry Pratchett-style narrative creation with rigorous tracking of characters, timelines, and Scinted realities.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                        TELEPORT MASSIVE WRITER                               ║
║                                                                              ║
║  "The manuscript you hold is both key and lock.                             ║
║   Turn it carefully."                                                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Architecture

This module implements a **DM-style orchestration system** that simultaneously tracks:

- **Characters** (internal thoughts + external behavior)
- **Timelines** (reality branches and Scinted divergences)
- **World State** (locations, factions, artifacts, lore)
- **Scenes** (narrative beats with wiki-linked elements)
- **The Orchestrator's Journal** (meta-narrative tracking)

## Directory Structure

```
teleport_massive_writer/
├── world/                    # Worldbuilding elements
│   ├── locations/           # Places (physical and conceptual)
│   ├── factions/            # Organizations and groups
│   ├── artifacts/           # Important objects
│   ├── concepts/            # Key ideas, technologies, phenomena
│   └── _world_index.md      # Master index of all world elements
│
├── characters/              # Character profiles
│   ├── protagonists/        # Main characters
│   ├── antagonists/         # Opposition forces
│   ├── supporting/          # Supporting cast
│   └── _character_index.md  # Master character list
│
├── timelines/               # Reality tracking
│   ├── prime/               # Prime timeline events
│   ├── scinted/             # Branched/fractured realities
│   └── _timeline_index.md   # Timeline navigation
│
├── scenes/                  # Story content
│   ├── chapters/            # Chapter scenes
│   ├── interludes/          # Between-chapter content
│   └── _scene_index.md      # Scene navigation
│
├── journals/                # Character journals
│   ├── internal/            # True thoughts/motivations
│   └── external/            # Observable behavior logs
│
├── orchestration/           # DM-level tracking
│   ├── story_state.md       # Current narrative state
│   ├── character_states.md  # All character current states
│   ├── open_threads.md      # Unresolved plot threads
│   ├── secrets.md           # Hidden information (who knows what)
│   └── dm_notes.md          # Orchestrator's working notes
│
└── templates/               # Markdown templates
    ├── character.md         # Character profile template
    ├── location.md          # Location template
    ├── scene.md             # Scene template
    ├── timeline_event.md    # Timeline event template
    └── journal_entry.md     # Journal entry template
```

## Wiki Linking Convention (Obsidian-Flavored)

All documents use `[[wiki-style links]]` for cross-referencing:

```markdown
[[Characters/Aziah Calderon]]           # Link to character
[[Locations/Teleport Massive HQ]]       # Link to location
[[Timelines/Prime/2087-03-15]]          # Link to timeline event
[[Concepts/Scinting]]                   # Link to concept
[[Artifacts/SWAB]]                      # Link to artifact
```

### Link Types

| Syntax | Purpose |
|--------|---------|
| `[[Name]]` | Simple link (auto-resolves) |
| `[[Folder/Name]]` | Explicit path link |
| `[[Name\|Display Text]]` | Link with custom display |
| `[[Name#Section]]` | Link to specific section |
| `[[Name^block-id]]` | Link to specific block |

## Character Tracking System

Each character has two parallel records:

### Internal Journal (True Self)
- Actual thoughts and motivations
- Hidden knowledge and secrets
- Internal conflicts and desires
- What they *really* think about others

### External Record (Observable Self)
- Actions taken (observable by others)
- Dialogue spoken
- Physical behaviors
- How others perceive them

This dual-track system enables:
- Dramatic irony (reader knows what characters don't)
- Unreliable narration
- Complex character motivation tracking
- "Who knows what" management

## Timeline & Reality Tracking

The Teleport Massive universe features **Scinted realities** - points where reality fractures and diverges.

```
PRIME TIMELINE
     │
     ├──● Event A
     │
     ├──◆ SCINT POINT [SP-001]
     │   │
     │   ├── Reality A (Prime continues)
     │   │
     │   └── Reality B (Divergent)
     │         │
     │         └──◆ SCINT POINT [SP-002]
     │              ├── Reality B1
     │              └── Reality B2
     │
     └──● Event B (Prime)
```

Each Scint Point is documented with:
- Triggering conditions
- Divergence description
- Which characters/elements exist in which branch
- Cross-reality effects (if any)

## Orchestration Layer

The DM/Orchestrator maintains god-level awareness:

1. **Story State**: Where are we in the narrative?
2. **Character States**: What does each character know/believe/want right now?
3. **Open Threads**: What plot elements are unresolved?
4. **Secrets Registry**: Who knows what? What's still hidden?
5. **Consistency Checks**: Does everything make sense across timelines?

## Usage

### Creating a New Character

```bash
# Copy template and fill in
cp templates/character.md characters/protagonists/New_Character.md
```

### Logging a Scene

```bash
# Create new scene from template
cp templates/scene.md scenes/chapters/CH01_SC01_The_Arrival.md
```

### Recording a Timeline Event

```bash
# Add to appropriate timeline
cp templates/timeline_event.md timelines/prime/2087-03-15_First_Teleport.md
```

## Integration with WAFT

This module integrates with WAFT's existing systems:

- **PDF Generation**: Export manuscripts, character sheets, world guides
- **Storyteller Engine**: AI-assisted narrative generation
- **Scint Gym**: Reality consistency validation
- **Document Builder**: Professional document output

## The Pratchett Principle

> "The intelligence of the creature known as a crowd is the square root of the number of people in it."

This system encourages:
- Footnotes and asides
- Fourth-wall awareness (the manuscript IS the artifact)
- Layered meaning
- Wit in darkness
- Truth wrapped in absurdity

---

*Remember: not everything is what it seems.*
