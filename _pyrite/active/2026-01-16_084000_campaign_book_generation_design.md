# Campaign Book Generation System Design

**Date**: 2026-01-16 08:40:00 PST  
**Context**: Designing professional campaign book generation (Pathfinder/D&D style)  
**Goal**: Create a system that generates complete, professional campaign books

---

## What Makes a Professional Campaign Book?

### Structure of Pathfinder/D&D Campaign Books

1. **Cover & Title Page**
   - Eye-catching cover design
   - Campaign title and subtitle
   - Author/publisher info
   - Level range indicator

2. **Table of Contents**
   - All major sections
   - Page numbers
   - Clear hierarchy

3. **Introduction/Campaign Overview**
   - Campaign synopsis
   - Level range and party size
   - Estimated play time
   - Themes and tone
   - Setting overview

4. **Player's Guide** (Optional but valuable)
   - Character creation guidelines
   - Recommended classes/races
   - Setting-specific rules
   - Starting equipment
   - Background information

5. **Adventure Path/Modules**
   - Multiple adventures (chapters)
   - Each with:
     - Overview
     - Background
     - Hooks
     - Locations
     - Encounters
     - NPCs
     - Read-aloud text
     - Maps (descriptions or actual)
     - Treasure/rewards

6. **NPCs & Organizations**
   - Major NPCs with stat blocks
   - Organizations and factions
   - Relationship webs
   - Motivations and goals

7. **Locations**
   - Detailed location descriptions
   - Maps (or map descriptions)
   - Points of interest
   - Random encounter tables

8. **Bestiary**
   - Monster stat blocks
   - Organized by CR or type
   - Lore and descriptions
   - Tactics and behavior

9. **Items & Equipment**
   - Magic items
   - Unique equipment
   - Treasure tables
   - Item descriptions

10. **Appendices**
    - Random encounter tables
    - Treasure tables
    - NPC name generators
    - Quick reference tables
    - Index

---

## Current WAFT Capabilities

### ✅ What We Have

1. **Storybook Generation**
   - `Storyteller.create_storybook()`
   - D&D 5e LaTeX template
   - Read-aloud text boxes
   - Sidebars
   - Monster stat blocks
   - Chapter structure

2. **Character Sheets**
   - `generate_character_sheet_latex()`
   - Full D&D 5e character stats
   - Professional formatting

3. **Campaign Orchestration**
   - `CampaignOrchestrator` class
   - Session tracking
   - State management
   - Story generation

4. **Narrative Generation**
   - `GeminiNarrativeEngine`
   - Campaign narrative generation
   - Character descriptions

5. **Monster Stat Blocks**
   - `_build_monster_stat_block()`
   - Full D&D 5e stat block format
   - Actions, abilities, legendary actions

### ⚠️ What We Need

1. **Multi-Section Book Structure**
   - Player's Guide section
   - DM Guide section
   - Adventure modules
   - Bestiary section
   - Appendices

2. **Advanced Layout**
   - Table of contents (auto-generated)
   - Index generation
   - Cross-references
   - Page numbering
   - Section breaks

3. **Campaign-Specific Content**
   - Location descriptions
   - NPC reference cards
   - Organization descriptions
   - Random encounter tables
   - Treasure tables

4. **Map Support**
   - Map descriptions (text-based)
   - Location keys
   - Distance/scale information

5. **Professional Polish**
   - Cover page generation
   - Consistent formatting
   - Professional typography
   - Visual hierarchy

---

## Proposed Architecture

### CampaignBookGenerator Class

```python
class CampaignBookGenerator:
    """Generate professional campaign books like Pathfinder/D&D modules."""
    
    def __init__(self, campaign_data: CampaignData):
        self.campaign_data = campaign_data
        self.storyteller = Storyteller()
        self.sections = []
    
    def generate_campaign_book(self) -> Path:
        """Generate complete campaign book PDF."""
        # 1. Generate cover
        # 2. Generate table of contents
        # 3. Generate introduction
        # 4. Generate player's guide (optional)
        # 5. Generate adventure modules
        # 6. Generate NPCs section
        # 7. Generate locations section
        # 8. Generate bestiary
        # 9. Generate items section
        # 10. Generate appendices
        # 11. Compile into single PDF
        pass
```

### CampaignData Structure

```python
@dataclass
class CampaignData:
    """Complete campaign data structure."""
    
    # Basic Info
    title: str
    subtitle: str
    author: str
    level_range: str  # "1-5", "3-7", etc.
    party_size: str   # "3-5", "4-6", etc.
    estimated_time: str  # "20-30 hours"
    tone: str  # "epic", "dark", "whimsical", etc.
    setting: str
    
    # Content
    introduction: str
    player_guide: Optional[PlayerGuide] = None
    adventures: List[Adventure] = []
    npcs: List[NPC] = []
    locations: List[Location] = []
    monsters: List[Monster] = []
    items: List[Item] = []
    organizations: List[Organization] = []
    
    # Tables
    random_encounters: Dict[str, List[Encounter]] = {}
    treasure_tables: Dict[str, List[Treasure]] = {}
```

### Section Generators

```python
class CampaignBookSection:
    """Base class for campaign book sections."""
    
    def generate_latex(self) -> str:
        """Generate LaTeX for this section."""
        pass

class IntroductionSection(CampaignBookSection):
    """Campaign introduction and overview."""
    pass

class PlayersGuideSection(CampaignBookSection):
    """Player-facing guide."""
    pass

class AdventureSection(CampaignBookSection):
    """Adventure module section."""
    pass

class NPCsSection(CampaignBookSection):
    """NPCs and organizations."""
    pass

class LocationsSection(CampaignBookSection):
    """Locations and maps."""
    pass

class BestiarySection(CampaignBookSection):
    """Monster manual."""
    pass

class ItemsSection(CampaignBookSection):
    """Items and equipment."""
    pass

class AppendicesSection(CampaignBookSection):
    """Tables and reference material."""
    pass
```

---

## Implementation Plan

### Phase 1: Core Structure
1. Create `CampaignBookGenerator` class
2. Design `CampaignData` dataclass
3. Implement section base class
4. Create LaTeX template for multi-section books

### Phase 2: Section Generators
1. Introduction section
2. Adventure modules section
3. NPCs section
4. Bestiary section
5. Locations section

### Phase 3: Advanced Features
1. Table of contents generation
2. Index generation
3. Cross-references
4. Cover page generation

### Phase 4: Content Generation
1. Random encounter tables
2. Treasure tables
3. NPC reference cards
4. Location descriptions
5. Map descriptions

### Phase 5: Polish
1. Professional formatting
2. Consistent styling
3. Visual hierarchy
4. Typography improvements

---

## Key Design Decisions

### 1. LaTeX vs. Other Formats
**Decision**: Use LaTeX (already have D&D 5e template)
- **Pros**: Professional output, full control, existing template
- **Cons**: Compilation time, complexity
- **Alternative**: Could add HTML/PDF alternative later

### 2. Single PDF vs. Multiple PDFs
**Decision**: Single comprehensive PDF
- **Pros**: Easy to use, professional, complete
- **Cons**: Large file size
- **Alternative**: Could generate separate PDFs per section

### 3. Content Generation
**Decision**: Support both manual and AI-generated content
- Manual: User provides all content
- AI: Use GeminiNarrativeEngine to generate content
- Hybrid: User provides structure, AI fills details

### 4. Map Support
**Decision**: Start with text-based map descriptions
- **Pros**: No image dependencies, easy to generate
- **Cons**: Less visual
- **Future**: Add image map support later

---

## Example Usage

```python
from src.waft.campaign.campaign_book_generator import CampaignBookGenerator, CampaignData

# Create campaign data
campaign = CampaignData(
    title="The Shattered Crown",
    subtitle="A D&D 5e Adventure Path",
    author="WAFT Campaign Generator",
    level_range="1-5",
    party_size="3-5",
    estimated_time="20-30 hours",
    tone="epic",
    setting="Kingdom of Aetheria",
    introduction="...",
    adventures=[...],
    npcs=[...],
    locations=[...],
    monsters=[...],
    items=[...]
)

# Generate book
generator = CampaignBookGenerator(campaign)
pdf_path = generator.generate_campaign_book()

print(f"Campaign book generated: {pdf_path}")
```

---

## Integration Points

### With Existing Systems

1. **Storyteller System**
   - Use for narrative generation
   - Leverage existing storybook features
   - Reuse read-aloud and sidebar formatting

2. **Campaign Orchestrator**
   - Generate books from campaign data
   - Export campaign state to book format
   - Create books from completed campaigns

3. **D&D 5e Engine**
   - Use for stat blocks
   - Leverage character generation
   - Reuse monster templates

4. **Narrative Engine**
   - Generate campaign descriptions
   - Create NPC backstories
   - Write location descriptions

---

## Next Steps

1. **Create Design Document** ✅ (This file)
2. **Prototype Core Structure**
   - CampaignBookGenerator class
   - CampaignData structure
   - Basic LaTeX template

3. **Implement First Section**
   - Start with Introduction section
   - Test LaTeX compilation
   - Verify output quality

4. **Iterate and Expand**
   - Add more sections
   - Improve formatting
   - Add features

---

**Status**: Design phase complete, ready for implementation
