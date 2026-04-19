# Waft Framework Exploration Report

**Date**: 2026-04-19  
**Exploration Method**: Hands-on usage and system observation  
**Environment**: Python 3.12, uv 0.8.17  

---

## Executive Summary

Waft is a sophisticated **evolutionary code framework** that treats agents as self-modifying organisms with DNA (code), fitness testing, and game-theoretic dynamics overlaid on Python project management. Through hands-on exploration, we observed:

1. **Complete initialization pipeline** - Projects scaffold with memory, epistemics, and gamification
2. **Dual-layer architecture** - Practical CLI/API tools + narrative/gamification overlay
3. **Memory-centric design** - Persistent state through JSON-based memory structures
4. **Document generation as first-class feature** - 25+ professional templates with recursive self-documentation
5. **Emergent narrative system** - TavernKeeper overlays game-theory on all operations

---

## Phase 1: Installation & Verification

### Findings

**Installation Success:**
- `uv sync --python 3.12` successfully installed all 150+ dependencies
- `uv tool install --editable .` installed the CLI
- `waft` command immediately available after installation

**Key Dependencies Installed:**
- Typer (CLI framework)
- Pydantic 2.0+ (data validation)
- FastAPI + Uvicorn (REST API)
- Empirica 1.2.3+ (epistemic tracking)
- TinyDB 4.8.0 (local document database)
- Rich 13.0+ (terminal rendering)
- WeasyPrint 68.0+ (PDF generation)
- CrewAI (optional, for agent coordination)

**Verification Command Output:**
```
waft verify
→ Gate-based validation system (TavernKeeper narrative)
→ Card games determine "success" with probability mechanics
→ XP awarded, achievements unlocked
```

**Key Insight**: Verification isn't just a dry check—it's gamified through card-based decision making (like a roguelike game). Every action runs through a dice check system.

---

## Phase 2: Test Laboratory Creation

### Project Structure

Running `waft new test_lab --path /tmp/waft_exploration` created:

```
test_lab/
├── .git/                    # Git initialized automatically
├── .github/
├── .python-version          # Specifies Python 3.12+
├── pyproject.toml           # uv project config
├── Justfile                 # Task runner templates
├── README.md                # Auto-generated docs
├── main.py                  # Entry point template
├── src/
│   └── agents.py           # Agent scaffold
└── _pyrite/                # Memory structure
    ├── .waft/              # Hidden system memory
    │   ├── gamification.json    # Game state
    │   └── chronicles.json      # Adventure journal
    ├── active/             # Current work items
    ├── backlog/            # Future work
    └── standards/          # Project standards
```

### Memory Files Analysis

**gamification.json** - Game state tracking:
```json
{
  "integrity": 100.0,
  "insight": 50.0,
  "level": 1,
  "achievements": ["perfect_integrity", "first_build"],
  "history": [
    {
      "timestamp": "2026-04-19T09:09:04.605317",
      "type": "insight_award",
      "amount": 50.0,
      "reason": "Created new project"
    }
  ]
}
```

**chronicles.json** - D&D 5e character + adventure log:
```json
{
  "character": {
    "name": "test_lab",
    "level": 2,
    "integrity": 100.0,
    "insight": 105.0,
    "ability_scores": {
      "strength": 8, "dexterity": 8, "constitution": 8,
      "intelligence": 8, "wisdom": 8, "charisma": 8
    },
    "max_hp": 10, "current_hp": 10
  },
  "adventure_journal": [
    {
      "event": "new",
      "narrative": "Sector Delta-12 optimized. Logic-Lattice integrity at 102%%.",
      "dice_roll": "1d20+-1",
      "result": 10,
      "outcome": "success",
      "rewards": {"insight": 55, "credits": 10, "integrity": 2.0}
    }
  ]
}
```

**Key Insight**: Waft uses a **persistent, typed state system** where:
- Integrity = code quality metric (0-100%)
- Insight = XP/knowledge points
- Credits = in-game currency for work/decisions
- D&D stats = ability modifiers for checks

---

## Phase 3: Core Commands Exploration

### Command Architecture

**50+ Commands** discovered, organized in functional families:

```
Project Management:
  new, verify, sync, add, init, info

Epistemic Tracking:
  assess, dashboard, hud, check

Gamification:
  stats, character, achievements, chronicle, level, roll, quests

Narrative:
  observe, note, journal-search, journal-stats, phase1, analyze, resume

Decision Making:
  decide, next-cmd, oracle-cycle, pantheon-command

Media Generation:
  meme, case-render, encapsulated-environments-pdf

API/Server:
  serve, dashboard-5050, runtime-demo
```

### Observed Behaviors

**`waft info` output:**
```
Project Path: /tmp/waft_exploration/test_lab
Project Name: test-lab
Version: 0.1.0
_pyrite Structure: Valid
uv.lock: Missing (needs uv sync)
Empirica: Not initialized (git needed)

[WIS Check: 6 + -1 = 5 (DC 8) - failure]
[+2 Insight gained]
```

**Key Insight**: Every command result includes:
- Dice check (1d20 + modifier based on relevant stat)
- Difficulty Class (DC) target
- Success/failure outcome
- Contextual rewards (Insight, Credits)

**`waft stats` output:**
```
💎 Integrity: 100%
🧠 Insight: 50
⭐ Level: 1
🏆 Achievements: 2
```

**`waft chronicle` output:**
Shows adventure journal entries as formatted table with:
- Timestamps
- Event types (achievement, insight_award, new, etc.)
- Dice roll results
- Narrative descriptions
- Reward amounts

---

## Phase 4: Memory & Telemetry Systems

### Data Persistence Architecture

**Storage Layers:**

1. **_pyrite/.waft/** (Hidden system memory)
   - gamification.json - Game state
   - chronicles.json - Adventure logs
   - Indexed by timestamp + event type

2. **_pyrite/active/** - Current work in progress
3. **_pyrite/backlog/** - Planned work
4. **_pyrite/standards/** - Project standards/docs

### Flight Recorder (Telemetry)

Each event recorded includes:
- **Timestamp** (ISO 8601)
- **Event Type** (insight_award, achievement_unlocked, new, etc.)
- **Payload** (context-dependent)
- **State Before/After** (integrity, insight, level)
- **Rewards** (insight, credits, integrity changes)
- **Classification** (success/failure, outcome quality)

### Empirica Integration

**Epistemic Tracking** (requires git):
```
waft session bootstrap  # Load context and session
waft session status     # Show current session
```

Creates persistent epistemic state for:
- Knowledge gaps (unknowns)
- Findings (discoveries)
- Safety gates (go/no-go decisions)

---

## Phase 5: Document Generation

### Template System (25+ templates)

**Professional Templates:**
```
Academic:
  - academic_paper.py
  - simple_scientific.py
  - scientific_research_paper

Business:
  - invoice_contract.py
  - one_pager.py
  - brief.py

Technical:
  - code_documentation.py
  - lab_notes.py
  - field_guide.py

Creative:
  - eldritch_journal.py
  - screenplay.py
  - heartfelt_letter.py

Narrative:
  - storybook.py
  - newspaper.py
  - worldbuild.py

Gaming:
  - dnd5e_latex.py
  - dnd_scenario.py
```

### Meme Generation System

**15 Meme Templates** available:

```
Mainstream:
  drake, distracted_boyfriend, expanding_brain, two_buttons,
  change_my_mind, woman_yelling_cat, gru_plan, one_does_not_simply,
  success_kid, ancient_aliens, left_exit_12_off_ramp

WAFT-native:
  waft_oracle (prophecy cards)
  containment_alert (incident reports)
  chef_waft_special (cooking logs)
```

**Usage**: `waft meme generate --template drake --text "..."` generates image memes.

### Binder System

Assembles multiple documents into cohesive PDF collections:
- Cover pages (4 styles)
- Automatic table of contents
- Section dividers
- Multi-document merging

---

## Phase 6: API & Dashboard Architecture

### FastAPI Routes

**Route Groups:**
```
/api/auth/           - Token-based authentication
/api/projects/       - Project CRUD operations
/api/work-efforts/   - Work effort management
/api/health/         - Health checks
/api/beings/         - Agent/being management
/api/biome/          - Environment state
/api/gym/            - Scint Gym (fitness testing)
/api/oracle/         - Oracle decision system
/api/empirica/       - Epistemic state
/api/git/            - Git operations
/api/meme-lab/       - Meme generation
/api/storyteller/    - Narrative generation
/api/dashboard/      - Dashboard data
/api/evolve-monitor/ - Evolution tracking
/api/quests/         - Quest system
/api/state/          - System state snapshots
```

### Server Options

**`waft serve`** - Development web server
**`waft dashboard-5050`** - Integrated dashboard + API on port 5050
**`waft runtime-demo`** - CLI-guided API demo

### Authentication

Write operations (POST, PUT, PATCH, DELETE) require Bearer token from `/api/auth/handshake`.
Read operations are publicly accessible.

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      WAFT Framework                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐      ┌──────────────────┐             │
│  │   CLI Interface  │      │   REST API       │             │
│  │  (Typer-based)   │      │  (FastAPI)       │             │
│  │                  │      │                  │             │
│  │  50+ Commands    │──→───│  25+ Routes      │             │
│  └──────────────────┘      └──────────────────┘             │
│           │                         │                       │
│           ├─────────┬───────────────┤                       │
│           v         v               v                       │
│  ┌─────────────────────────────────────────┐               │
│  │  Core Orchestration Layer               │               │
│  │  - SubstrateManager (project init)      │               │
│  │  - MemoryManager (state persistence)    │               │
│  │  - EmpiricaManager (epistemic track)    │               │
│  │  - GamificationManager (D&D overlay)    │               │
│  │  - TavernKeeper (narrative system)      │               │
│  └─────────────────────────────────────────┘               │
│           │                                                  │
│           v                                                  │
│  ┌─────────────────────────────────────────┐               │
│  │  Storage & Memory Systems               │               │
│  │                                         │               │
│  │  _pyrite/                               │               │
│  │  ├── .waft/gamification.json            │               │
│  │  ├── .waft/chronicles.json              │               │
│  │  ├── active/ (TinyDB work efforts)      │               │
│  │  ├── backlog/ (planned work)            │               │
│  │  └── standards/ (project standards)     │               │
│  │                                         │               │
│  │  Plus: Empirica epistemic DB            │               │
│  └─────────────────────────────────────────┘               │
│           │                                                  │
│           v                                                  │
│  ┌─────────────────────────────────────────┐               │
│  │  Generation & Rendering Systems         │               │
│  │  - DocumentBuilder (25+ templates)      │               │
│  │  - Binder (PDF assembly)                │               │
│  │  - MemeGenerator (15 meme templates)    │               │
│  │  - Reflection (self-analysis)           │               │
│  └─────────────────────────────────────────┘               │
│                                                               │
│  ┌──────────────────┐      ┌──────────────────┐             │
│  │  Game Theory     │      │  Safety Gates    │             │
│  │  Overlay         │      │                  │             │
│  │                  │      │  - check()       │             │
│  │  - Integrity     │      │  - assess()      │             │
│  │  - Insight (XP)  │      │  - decide()      │             │
│  │  - D&D Stats     │      │  - oracle()      │             │
│  │  - Achievements  │      │                  │             │
│  │  - Quests        │      │  Returns:        │             │
│  │  - Narrative     │      │  PROCEED/HALT/   │             │
│  │                  │      │  BRANCH/REVISE   │             │
│  └──────────────────┘      └──────────────────┘             │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Design Patterns Observed

### 1. **State as First-Class Citizen**
Every operation mutates persistent state tracked in JSON files:
- Gamification (game mechanics)
- Chronicles (narrative/history)
- Empirica (epistemics)
- TinyDB (work efforts)

### 2. **Dual-Layer Architecture**
- **Practical layer**: File management, API, commands
- **Narrative layer**: D&D stats, quests, achievements, dice rolls

Every practical operation is dressed in narrative game mechanics.

### 3. **Event-Sourced Telemetry**
Complete history of all mutations recorded with:
- Timestamp
- Event type
- Before/after state
- Classification (success/failure/outcome)

### 4. **Probabilistic Decision-Making**
All checks use d20 mechanics:
- Roll dice (1d20)
- Add ability modifier (+WIS, +STR, etc.)
- Compare to DC (difficulty class)
- Award insight/credits on success

### 5. **Recursive Documentation**
Framework can document itself using its own document generation system—enabling self-improvement loops.

---

## Integration Points

### External Systems

1. **Git** - Automatic repo initialization, commit tracking
2. **Empirica** - Epistemic state and memory (requires git)
3. **CrewAI** - Optional agent coordination (optional dependency)
4. **FastAPI/Uvicorn** - REST API and web server
5. **TinyDB** - File-based document database for work efforts
6. **WeasyPrint/ReportLab** - PDF generation from templates

### Data Formats

- **JSON** - State persistence (gamification, chronicles)
- **YAML** - Work effort frontmatter
- **Markdown** - Documentation
- **HTML/CSS** - Web templates
- **Jinja2** - Template rendering
- **PDF** - Final document output

---

## Operational Workflows

### Typical Session Flow

```
1. waft new laboratory
   → Creates _pyrite structure
   → Awards "First Build" achievement
   → Sets integrity=100%, insight=50
   
2. waft info
   → Shows project metadata
   → Runs WIS check
   → Awards insight if successful
   
3. waft observe "Discovery X" --mood curious
   → Logs to episodic memory
   → Triggers narrative hooks
   
4. waft chronicle
   → Displays adventure journal
   → Shows historical progression
   
5. waft decide --goal "Choose framework"
   → Runs decision matrix analysis
   → Records outcome and rationale
   
6. waft session bootstrap
   → Loads Empirica context
   → Shows epistemic dashboard
   
7. waft serve --port 8000
   → Starts REST API
   → Serves web dashboard
```

---

## Gamification Deep-Dive

### Stats Tracked

| Stat | Range | Meaning |
|------|-------|---------|
| Integrity | 0-100% | Code quality/project health |
| Insight | 0-∞ | XP/knowledge points |
| Level | 1-∞ | Character progression |
| Credits | 0-∞ | In-game currency |
| D&D Ability Scores | 3-18 | Modifiers for checks |

### Achievement Categories

- `perfect_integrity` - 100% integrity maintained
- `first_build` - Initial project creation
- `oracle_consulted` - Used decision oracle
- `documented` - Documentation completed
- Custom achievements based on milestones

### Narrative System

Every action generates narrative via TavernKeeper:
```
"Sector Delta-12 optimized. Logic-Lattice integrity at 102%%."
"The Dealer presents three cards..."
"Success! Key Fragment earned: SEAL-02-BEF3AE39A48C014E"
```

---

## Memory Model

### Three-Tier Memory System

**Tier 1: Gamification (Recent Decisions)**
```json
{
  "type": "insight_award",
  "timestamp": "2026-04-19T09:09:04",
  "amount": 50,
  "reason": "Created new project"
}
```

**Tier 2: Chronicles (Adventure Log)**
```json
{
  "event": "new",
  "narrative": "...",
  "dice_roll": "1d20+-1",
  "rewards": {"insight": 55}
}
```

**Tier 3: Empirica (Epistemics)**
- Knowledge gaps (unknowns)
- Findings (discoveries)
- Safety gates
- Reasoning traces

---

## Observed Constraints & Limitations

1. **Git Dependency** - Empirica features require initialized Git repo
2. **Python 3.12+** - Requires fairly recent Python version
3. **150+ Dependencies** - Large dependency footprint
4. **Memory Files** - JSON-based storage (not suitable for massive scale)
5. **Narrative Overlay** - Optional but omnipresent (can be verbose)

---

## Key Innovations Observed

### 1. **Game Theory Applied to Development**
D&D mechanics applied to mundane operations creates engaging feedback loops.

### 2. **Persistent Event Log**
Every operation recorded with full context enables perfect replay and analysis.

### 3. **Self-Documenting Framework**
Framework can generate its own documentation using its own templates.

### 4. **Dual-Layer Architecture**
Separating practical operations from narrative overlay allows both rigor and creativity.

### 5. **Empirica Integration**
Epistemic tracking brings formalized knowledge management to AI agent development.

---

## Recommendations for Further Exploration

1. **Evolutionary Cycle**: Run `waft evolve` to observe agent mutation and fitness selection
2. **Scint Gym**: Test the error detection and correction system
3. **Oracle Cycle**: Use `waft oracle-cycle` to see decision-making in action
4. **Multi-Agent Coordination**: Explore CrewAI integration for agent swarms
5. **Custom Templates**: Create domain-specific document templates
6. **API Automation**: Build CLI tools that consume the REST API
7. **Dashboard Development**: Extend web dashboard with custom visualizations

---

## Conclusion

Waft is a **meta-framework for managing AI agent evolution** with sophisticated state management, narrative overlay, and document generation. It treats code as DNA and projects as living organisms with game-theoretic dynamics.

The framework reveals several design insights:
- **Memory is king**: Persistent, timestamped state enables perfect reconstruction
- **Narrative matters**: Game mechanics overlay creates engagement and meaning
- **Flexibility**: Dual-layer architecture allows both practical and creative operations
- **Composability**: Template system enables recursive documentation and self-improvement

**For AI research**: Waft provides the experimental infrastructure to observe emergent agent behavior over thousands of generations with complete telemetry.

**For practical Python projects**: Waft scaffolds, gamifies, and memorializes project development with integrated memory, decision support, and document generation.

---

## Appendix: File Inventory

### Core Modules

```
src/waft/
├── main.py                    # CLI entry point
├── core/
│   ├── agent/                # Agent implementation
│   ├── orchestrator.py        # System orchestration
│   ├── memory.py              # Memory management
│   ├── empirica.py            # Epistemic tracking
│   ├── gamification.py        # Game mechanics
│   ├── substrate.py           # Project initialization
│   └── tavern_keeper.py       # Narrative system
├── cli/
│   ├── project_commands.py    # new, verify, init, info
│   ├── hud.py                # Dashboard rendering
│   ├── meme_cli.py            # Meme generation
│   ├── epistemic_display.py  # Epistemic HUD
│   └── 25+ other command modules
├── api/
│   ├── main.py                # FastAPI app
│   ├── routes/                # 25+ route modules
│   ├── models.py              # Pydantic schemas
│   └── services/              # Business logic
└── templates/
    ├── academic_paper.py
    ├── field_guide.py
    ├── dnd_scenario.py
    ├── 22+ other templates
    └── latex/                # LaTeX templates
```

### Configuration

```
pyproject.toml                # Dependencies, metadata
src/waft/config/
├── abilities.py              # D&D ability definitions
└── theme.py                  # UI theming
```

### Examples

```
examples/
├── interactive_demo.py        # Self-observation demo
├── demonstrate_reflection.py  # Reflection system
├── simple_field_guide_example.py
├── generate_*_pdf.py         # 50+ PDF generation examples
└── (90 more example scripts)
```

---

*End of Exploration Report*

Generated by hands-on system exploration on 2026-04-19.
