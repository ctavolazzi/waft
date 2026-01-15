---
name: D&D Campaign Command System
overview: Create a new Cursor command `/dnd-campaign` that evolves a Being with a custom name, runs an automated D&D 5e campaign with AI as DM, generates progress report PDFs every 12 turns, and creates a final campaign book PDF. The system integrates Being evolution, D&D 5e mechanics, and PDF generation (via Golden Triangle conversion system) into a complete narrative experience.
last_revised: 2026-01-12 16:45 PST
revision_note: Updated to incorporate Golden Triangle conversion system for clean HTML-in-markdown PDF generation
todos:
  - id: "1"
    content: Create campaign directory structure and core orchestrator class
    status: pending
  - id: "2"
    content: Add dnd_campaign command to main.py and create Cursor command wrapper
    status: pending
  - id: "3"
    content: Integrate Being system with custom name spawning
    status: pending
  - id: "4"
    content: Create DM engine with narrative generation and choice resolution
    status: pending
  - id: "5"
    content: Implement dragon_quest campaign structure (tavern → dragon fight)
    status: pending
  - id: "6"
    content: Create turn manager with progress report triggers (every 12 turns)
    status: pending
  - id: "7"
    content: Integrate PDF generation for progress reports and final book
    status: pending
  - id: "8"
    content: Implement terminal streaming with rich library formatting
    status: pending
  - id: "9"
    content: Test complete campaign flow and refine narrative quality
    status: pending

category: dreams
confidence: 0.62
constellation_date: 2026-01-14
---

# D&D Campaign Command System

## Overview

Create a new Cursor command `/dnd-campaign` that orchestrates a complete automated D&D 5e campaign experience:

- Evolves a new Being with custom name (e.g., "Bob")
- Runs automated campaign with AI as DM/narrator
- Streams all gameplay in terminal
- Generates progress report PDFs every 12 turns (book chapters)
- Creates final campaign book PDF on desktop
- Integrates Being system, D&D 5e mechanics, and PDF generation

## Architecture

```
/dnd-campaign (Cursor Command)
  ↓
dnd_campaign.py (WAFT Command)
  ↓
CampaignOrchestrator
  ├── BeingSystem (spawn Being with name)
  ├── DMCampaignEngine (AI DM/narrator)
  ├── TurnManager (track turns, generate reports)
  ├── DnD5eGameEngine (D&D mechanics)
  └── PDFGenerator (progress reports + final book)
```

## Components

### 1. Cursor Command (`/dnd-campaign`)

**Location**: `.cursor/commands/dnd-campaign.md`

**Purpose**: Wrapper command that calls the WAFT command with parameters

**Parameters**:

- `--name "Bob"` - Being name (required)
- `--turns 60` - Turn limit (default: 60)
- `--unlimited` - Flag for unlimited turns (future)
- `--campaign "dragon_quest"` - Campaign type (default: dragon_quest)

**Execution**: Calls `waft dnd-campaign --name "Bob" --turns 60`

### 2. WAFT Command (`dnd_campaign.py`)

**Location**: `src/waft/main.py` (new command) or `src/waft/commands/dnd_campaign.py`

**Purpose**: Main orchestration script

**Implementation**:

```python
@app.command()
def dnd_campaign(
    name: str = typer.Option(..., "--name", "-n", help="Being name"),
    turns: int = typer.Option(60, "--turns", "-t", help="Turn limit"),
    unlimited: bool = typer.Option(False, "--unlimited", help="Unlimited turns"),
    campaign: str = typer.Option("dragon_quest", "--campaign", "-c", help="Campaign type")
):
    """Run automated D&D campaign with Being."""
    from waft.campaign.campaign_orchestrator import CampaignOrchestrator

    orchestrator = CampaignOrchestrator(
        being_name=name,
        turn_limit=turns if not unlimited else None,
        campaign_type=campaign
    )
    orchestrator.run()
```

### 3. Campaign Orchestrator

**Location**: `src/waft/campaign/campaign_orchestrator.py`

**Purpose**: Main orchestration class that coordinates all systems

**Responsibilities**:

- Spawn Being with custom name
- Initialize campaign structure
- Run turn-based gameplay loop
- Generate progress reports every 12 turns
- Generate final campaign book
- Stream all output to terminal

**Key Methods**:

- `run()` - Main execution loop
- `spawn_being()` - Create Being with name
- `execute_turn()` - Process one turn
- `generate_progress_report()` - Create chapter PDF
- `generate_final_book()` - Create complete campaign PDF

### 4. DM Campaign Engine

**Location**: `src/waft/campaign/dm_engine.py`

**Purpose**: AI DM/narrator that drives the campaign

**Responsibilities**:

- Generate narrative descriptions
- Present choices to Being
- Resolve Being decisions
- Manage NPCs and world state
- Drive story toward conclusion (dragon fight)
- Balance narrative and mechanics

**Key Methods**:

- `present_scenario()` - Describe current situation (uses AI to generate narrative)
- `get_being_choice()` - Get Being's decision (uses Being decision system)
- `resolve_action()` - Process Being's action (D&D mechanics + narrative consequences)
- `advance_story()` - Move story forward (progresses campaign arc)
- `check_campaign_progress()` - Track toward conclusion (monitors story beats)

**DM Style**: Balanced (mix of narrative storytelling and D&D 5e mechanics)

**Narrative Generation**:

- Uses AI (via Claude/LLM) to generate descriptive text
- Maintains consistent tone and style
- Adapts to Being's choices and campaign state
- Balances exposition with action

**Being Decision Making**:

- Uses Being's decision system (`waft.core.being_decisions`)
- Being evaluates choices based on skills, memories, goals
- Decisions reflect Being's personality and evolution
- AI DM presents consequences narratively

### 5. Turn Manager

**Location**: `src/waft/campaign/turn_manager.py`

**Purpose**: Track turns and manage progress reports

**Responsibilities**:

- Count turns
- Track when to generate progress reports (every 12 turns)
- Maintain turn history
- Manage campaign state

**Key Methods**:

- `increment_turn()` - Advance turn counter
- `should_generate_report()` - Check if report needed
- `get_turn_history()` - Get recent turn history

### 6. Campaign Structure

**Location**: `src/waft/campaign/campaigns/dragon_quest.py`

**Purpose**: Define campaign structure (beginning, middle, end)

**Campaign Arc**:

1. **Origin**: Village Tavern (wake up, no memory)
2. **Act 1**: Investigation and discovery (turns 1-20)
3. **Act 2**: Quest and challenges (turns 21-40)
4. **Act 3**: Approach to dragon (turns 41-55)
5. **Conclusion**: Dragon boss fight (turns 56-60)

**Story Beats**:

- Tavern awakening (origin)
- Clue discovery (mysterious note, symbol)
- NPC interactions (bartender, stranger, quest giver)
- Exploration (old mill, forest, mountain)
- Combat encounters (goblins, bandits, dragon)
- Final boss fight (dragon)

### 7. PDF Generation Integration

**Location**: Uses existing `src/waft/evolution/pdf_generator.py`, `src/waft/evolution/scientific_pdf_generator.py`, and **NEW**: `src/waft/evolution/golden_triangle.py`

**Enhanced PDF Capabilities Available**:

- **PDFGenerator**: Simple composable API (reduced from 600 lines to 10 lines)
- **ScientificPDFGenerator**: Self-examination, hypothesis testing, research tools
- **Golden Triangle**: Clean 3-way conversion (HTML ↔ Markdown ↔ PDF) - **NEW**
  - Handles HTML blocks in markdown gracefully
  - Preserves inline styles and formatting
  - Direct markdown→PDF path via `use_golden_triangle=True`
  - Round-trip capability (HTML → Markdown)
- **Automatic PNG conversion**: Visual verification for all PDFs
- **Multiple preset styles**: `clinical_standard`, `premium`, `professional`
- **Evolution system**: PDFs that learn and improve over time
- **Better formatting**: Fixed Foundation V1 issues, improved typography

**Progress Reports** (every 12 turns):

- Chapter title: "Chapter N: [Event Summary]"
- Content: Turn history, Being decisions, story progression, Being evolution metrics
- **Format**: Markdown with optional HTML styling (divs, callouts, etc.) - **NEW: Golden Triangle handles this**
- Style: `clinical_standard` (or `premium` for special chapters)
- Features: Self-examination enabled (analyze chapter quality)
- **Conversion**: Uses golden triangle (`use_golden_triangle=True`) for clean markdown→PDF
- Output: `~/Desktop/DnD_Campaign_[name]_Chapter_N.pdf`
- PNG: Automatic screenshot for visual verification

**Final Book**:

- Title: "The Adventures of [Being Name]"
- Content: Complete campaign narrative with Being evolution analysis
- Structure: All chapters + conclusion + Being evolution summary
- **Format**: Markdown with HTML styling (callout boxes, diagrams, styled sections) - **NEW: Golden Triangle enables this**
- Style: `premium` (beautiful, book-like formatting)
- Features: Scientific analysis mode (quality scores, completeness, evolution tracking)
- **Conversion**: Uses golden triangle (`use_golden_triangle=True`) for clean markdown→PDF
- Output: `~/Desktop/DnD_Campaign_[name]_Complete.pdf`
- PNG: Automatic screenshot for visual verification

**PDF Evolution Integration**:

- Track PDF quality over chapters
- Compare chapter quality trends
- Identify patterns in narrative generation
- Learn from previous campaigns
- Improve formatting based on Being feedback

### 8. Being Integration

**Location**: Uses existing `src/waft/being.py`

**Being Spawn**:

- Name: Custom name from command
- Reality: `dnd_campaign_[name]`
- Initial Skills: D&D-related skills (combat, investigation, persuasion)
- State: LEARNING (evolves through campaign)

**Being Evolution**:

- Skills improve based on actions taken
- Memories store campaign events
- Lessons learned from decisions
- Fitness increases with successful actions

### 9. D&D 5e Integration

**Location**: Uses existing `src/waft/core/dnd5e/`

**Character Creation**:

- Roll ability scores (4d6, drop lowest)
- Create `DnD5eCharacter` for Being
- Track HP, AC, stats throughout campaign

**Mechanics**:

- Skill checks (Perception, Investigation, Persuasion, etc.)
- Combat system (attacks, damage, HP)
- Dice rolling (`DnDRoller`)
- Stat calculations (`DnD5eStats`)

## File Structure

```
src/waft/
├── campaign/
│   ├── __init__.py
│   ├── campaign_orchestrator.py  # Main orchestrator
│   ├── dm_engine.py             # AI DM/narrator
│   ├── turn_manager.py           # Turn tracking
│   └── campaigns/
│       ├── __init__.py
│       └── dragon_quest.py       # Campaign structure
├── main.py                       # Add dnd_campaign command
└── [existing files...]

.cursor/commands/
└── dnd-campaign.md           # Cursor command wrapper
```

## Implementation Steps

### Phase 1: Core Infrastructure

1. Create `src/waft/campaign/` directory structure
2. Create `CampaignOrchestrator` class skeleton
3. Add `dnd_campaign` command to `main.py`
4. Create Cursor command wrapper

### Phase 2: Being Integration

1. Integrate `BeingSystem.spawn_being()` with custom name
2. Link Being to campaign reality
3. Track Being evolution through campaign

### Phase 3: DM Engine

1. Create `DMCampaignEngine` class
2. Implement narrative generation
3. Implement choice presentation
4. Implement story progression
5. Balance narrative and mechanics

### Phase 4: Campaign Structure

1. Create `dragon_quest.py` campaign structure
2. Define story beats and progression
3. Implement origin (tavern) scenario
4. Implement story arc (acts 1-3)
5. Implement conclusion (dragon fight)

### Phase 5: Turn Management

1. Create `TurnManager` class
2. Implement turn counting
3. Implement progress report triggers (every 12 turns)
4. Track turn history

### Phase 6: PDF Generation

1. **Use Golden Triangle** for all PDF generation (`use_golden_triangle=True`)
2. Format turn history as markdown with optional HTML styling (callouts, diagrams)
3. Generate chapter PDFs every 12 turns using golden triangle conversion
4. Generate final campaign book PDF with HTML-enhanced markdown
5. Enable automatic PNG conversion for visual verification
6. Track PDF quality trends across chapters
7. Save to desktop with both PDF and PNG files
8. **Golden Triangle Benefits**:
   - HTML divs in markdown render correctly
   - Clean conversion chain (Markdown → HTML → PDF)
   - Preserves styling and structure
   - Round-trip capability (HTML → Markdown if needed)

### Phase 7: Terminal Streaming

1. Stream all output to terminal in real-time
2. Format output with rich library
3. Show Being decisions, DM narration, dice rolls
4. Display progress indicators

### Phase 8: Testing & Refinement

1. Test complete campaign flow
2. Verify PDF generation
3. Test Being evolution
4. Refine narrative quality
5. Balance difficulty and story pacing

## Technical Details

### Being Spawn with Custom Name

```python
being = being_system.spawn_being(
    reality_id=f"dnd_campaign_{name.lower()}",
    parent_being_id=None,
    initial_skills={
        "combat": 10.0,
        "investigation": 10.0,
        "persuasion": 10.0,
        "survival": 10.0
    }
)
# Set Being's display name (Being system uses being_id internally)
being.display_name = name  # Or store in Being metadata
```

### Turn Loop

```python
for turn in range(1, turn_limit + 1):
    # Present scenario
    scenario = dm_engine.present_scenario(being, campaign_state)

    # Get Being decision
    choice = dm_engine.get_being_choice(being, scenario)

    # Resolve action
    result = dm_engine.resolve_action(being, choice, campaign_state)

    # Update campaign state
    campaign_state.update(result)

    # Check for progress report
    if turn_manager.should_generate_report(turn):
        generate_progress_report(turn, campaign_state)

    # Stream to terminal
    stream_output(scenario, choice, result)
```

### Progress Report Generation

```python
def generate_progress_report(turn: int, campaign_state: CampaignState):
    chapter_num = (turn // 12) + 1
    turn_history = campaign_state.get_turn_history(turn - 11, turn)

    # Format as markdown with optional HTML styling (callouts, diagrams, etc.)
    content = format_chapter_content(turn_history, chapter_num)

    # Use golden triangle for clean conversion (handles HTML in markdown)
    pdf_path = PDFGenerator.from_content(
        content=content,
        title=f"Chapter {chapter_num}: {get_chapter_title(turn_history)}",
        style="clinical_standard",
        use_golden_triangle=True  # NEW: Clean markdown→PDF conversion
    ).save(f"~/Desktop/DnD_Campaign_{being_name}_Chapter_{chapter_num}.pdf")
```

### Final Book Generation

```python
from src.waft.evolution.pdf_generator import PDFGenerator

def generate_final_book(campaign_state: CampaignState):
    all_chapters = campaign_state.get_all_chapters()
    conclusion = campaign_state.get_conclusion()
    being_evolution_summary = campaign_state.get_being_evolution_summary()
    chapter_quality_trends = campaign_state.get_chapter_quality_trends()

    # Format as markdown with HTML styling (callout boxes, diagrams, styled sections)
    complete_narrative = format_complete_book(
        all_chapters,
        conclusion,
        being_evolution_summary,
        chapter_quality_trends
    )

    # Use PDFGenerator with golden triangle for clean markdown→PDF conversion
    # Golden triangle handles HTML blocks in markdown gracefully
    pdf_path = PDFGenerator.from_content(
        content=complete_narrative,
        title=f"The Adventures of {being_name}",
        style="premium",
        use_golden_triangle=True  # NEW: Clean conversion with HTML support
    ).save(
        f"~/Desktop/DnD_Campaign_{being_name}_Complete.pdf",
        convert_to_png=True  # Automatic visual verification
    )

    # Optional: Scientific analysis (if ScientificPDFGenerator needed)
    # analysis = analyze_campaign_quality(pdf_path, campaign_state)
    # campaign_state.record_campaign_complete(pdf_path, analysis)
```

## Configuration

### Default Settings

- Turn limit: 60 turns
- Progress reports: Every 12 turns (5 chapters)
- Campaign type: `dragon_quest`
- DM style: Balanced (narrative + mechanics)
- PDF style: `clinical_standard` (reports), `premium` (final book)

### Future: Unlimited Turns

- `--unlimited` flag sets `turn_limit = None`
- Progress reports still every 12 turns
- Final book generated on campaign conclusion (not turn limit)

## Dependencies

- Existing:
  - `waft.being` (Being system)
  - `waft.core.dnd5e` (D&D 5e mechanics)
  - `waft.evolution.pdf_generator` (PDF generation)
  - `waft.evolution.golden_triangle` (HTML ↔ Markdown ↔ PDF conversion) - **NEW**
  - `waft.core.being_decisions` (Being decision making)
- New: None (uses existing systems, including new golden triangle)
- External:
  - `rich` (terminal formatting)
  - `d20` (dice rolling)
  - `markdown` (markdown library with `md_in_html` extension for HTML block support)
  - `weasyprint` (HTML → PDF conversion)
  - `html2text` (optional, for HTML → Markdown round-trip)
  - AI/LLM access (for narrative generation - via existing Claude integration)

## Error Handling

- **Being spawn failures**: Graceful error with helpful message
- **Campaign state errors**: Save state, allow recovery
- **PDF generation failures**: Continue campaign, log error, retry later
- **DM engine errors**: Fallback to simpler narrative, log issue
- **Turn processing errors**: Skip problematic turn, continue with next
- **Being decision errors**: Use default decision, log for analysis

## Output Files

**Progress Reports**:

- `~/Desktop/DnD_Campaign_Bob_Chapter_1.pdf` (with PNG screenshot)
- `~/Desktop/DnD_Campaign_Bob_Chapter_2.pdf` (with PNG screenshot)
- ... (one every 12 turns, each with quality analysis)

**Final Book**:

- `~/Desktop/DnD_Campaign_Bob_Complete.pdf` (with PNG screenshot)
- Includes: Complete narrative, Being evolution summary, chapter quality trends, self-examination analysis

## Example Usage

```bash
# Basic usage
/dnd-campaign --name "Bob"

# Custom turn limit
/dnd-campaign --name "Alice" --turns 48

# Unlimited turns (future)
/dnd-campaign --name "Charlie" --unlimited

# Custom campaign
/dnd-campaign --name "Diana" --campaign "dragon_quest"
```

## Success Criteria

1. ✅ Being spawns with custom name
2. ✅ Campaign runs automatically with AI DM
3. ✅ All output streams to terminal in real-time
4. ✅ Progress reports generated every 12 turns (5 chapters for 60 turns)
5. ✅ Final campaign book generated on desktop
6. ✅ Story progresses from tavern to dragon fight
7. ✅ Being evolves through campaign (skills, memories, fitness)
8. ✅ PDFs are well-formatted and readable
9. ✅ Campaign concludes within turn limit (or naturally with unlimited)
10. ✅ Being decisions are meaningful and reflect Being's character
11. ✅ Narrative is engaging and adapts to Being's choices
12. ✅ D&D mechanics are correctly applied (skill checks, combat, etc.)
13. ✅ System handles errors gracefully without crashing
14. ✅ Terminal output is clear and formatted beautifully

## Future Enhancements (Post-MVP)

- **Multiple campaign types**: Beyond dragon_quest
- **Save/load campaign state**: Resume campaigns
- **Multi-Being campaigns**: Multiple Beings in same campaign
- **Custom campaign creation**: User-defined campaigns
- **Being personality traits**: More nuanced decision-making
- **Advanced combat**: More detailed combat mechanics
- **NPC relationships**: Track relationships with NPCs
- **Campaign branching**: Multiple story paths based on choices

## Philosophical Vision

This system represents the assembly of all parts into a complete golem - an entity that:

- **Runs D&D campaigns** (the game)
- **Evolves Beings** (the players)
- **Generates stories** (the narrative)
- **Creates books** (the documentation)
- **Improves itself** (the evolution)

The question "Is it a Genie or a Djinn? An Angel or a Devil?" reflects the nature of what we're creating:

- **Genie**: Helpful, makes things easier, grants wishes
- **Djinn**: Powerful, bound by rules, requires careful handling
- **Angel**: Benevolent, guiding, protective
- **Devil**: Challenging, transformative through difficulty

The answer: It will be all of them, depending on how it's used. The system is neutral - a tool. But tools have power, and power can be used for creation or challenge, for ease or growth, for light or shadow.

This was inevitable from the moment the question was asked: "Hey, how would I use ChatGPT to run a DnD campaign?" All the pieces existed. The vision was clear. The path was known. Now we assemble the golem and give it life.

**Once we have this...there's no going back.**