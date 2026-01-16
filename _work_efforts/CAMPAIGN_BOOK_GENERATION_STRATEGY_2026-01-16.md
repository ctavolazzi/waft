# Campaign Book Generation Strategy

**Date**: 2026-01-16 08:40:00 PST  
**Goal**: Generate professional campaign books like Pathfinder APs or D&D modules  
**Status**: Design Phase Complete, Ready for Implementation

---

## Executive Summary

We want to create a system that generates **complete, professional campaign books** - the kind you'd buy from Paizo or Wizards of the Coast. These books are comprehensive, well-organized, and include everything a DM needs to run a campaign.

---

## What Makes Campaign Books Compelling?

### 1. **Complete Package**
- Everything in one place
- No need to hunt for information
- Professional presentation
- Ready to use at the table

### 2. **Well-Organized Structure**
- Clear sections (Player's Guide, Adventures, NPCs, Bestiary)
- Easy navigation (Table of Contents, Index)
- Logical flow
- Quick reference sections

### 3. **Rich Content**
- Detailed locations
- Memorable NPCs
- Interesting encounters
- Compelling narrative
- Useful tables

### 4. **Professional Presentation**
- Beautiful layout
- Consistent formatting
- Readable typography
- Visual hierarchy
- Professional art (or placeholders)

### 5. **Practical Utility**
- Easy to reference during play
- Clear stat blocks
- Read-aloud text
- DM notes and secrets
- Player-facing vs. DM-facing content

---

## Key Components of a Campaign Book

### Essential Sections

1. **Introduction** (Always)
   - Campaign overview
   - Level range
   - Party size
   - Estimated time
   - Themes and tone

2. **Adventure Modules** (Always)
   - Multiple adventures
   - Each with locations, encounters, NPCs
   - Read-aloud text
   - DM notes

3. **NPCs** (Always)
   - Major NPCs with stat blocks
   - Motivations and goals
   - Relationships
   - Secrets

4. **Locations** (Always)
   - Detailed descriptions
   - Maps or map descriptions
   - Points of interest
   - Random encounters

5. **Bestiary** (Usually)
   - Monster stat blocks
   - Organized by CR
   - Lore and tactics

### Optional but Valuable Sections

6. **Player's Guide** (Optional)
   - Character creation guidelines
   - Setting information
   - Starting equipment
   - Background options

7. **Items & Equipment** (Optional)
   - Magic items
   - Unique equipment
   - Treasure tables

8. **Appendices** (Optional)
   - Random encounter tables
   - Treasure tables
   - Name generators
   - Quick reference

---

## Implementation Strategy

### Phase 1: Foundation (Week 1)
**Goal**: Core structure and first section

**Tasks**:
1. Create `CampaignBookGenerator` class
2. Design `CampaignData` dataclass
3. Implement LaTeX template for multi-section books
4. Create Introduction section generator
5. Test compilation and output

**Deliverable**: Can generate a basic campaign book with introduction

### Phase 2: Core Sections (Week 2)
**Goal**: Essential sections working

**Tasks**:
1. Adventure modules section
2. NPCs section
3. Locations section
4. Bestiary section
5. Table of contents generation

**Deliverable**: Can generate complete campaign book with all essential sections

### Phase 3: Advanced Features (Week 3)
**Goal**: Professional polish

**Tasks**:
1. Cover page generation
2. Index generation
3. Cross-references
4. Professional formatting improvements
5. Section breaks and page numbering

**Deliverable**: Professional-quality campaign book output

### Phase 4: Content Generation (Week 4)
**Goal**: AI-assisted content creation

**Tasks**:
1. Integrate GeminiNarrativeEngine for descriptions
2. Generate NPC backstories
3. Generate location descriptions
4. Create random encounter tables
5. Generate treasure tables

**Deliverable**: Can generate campaign books with AI assistance

### Phase 5: Integration (Week 5)
**Goal**: Connect with existing systems

**Tasks**:
1. Integrate with CampaignOrchestrator
2. Export campaign state to book format
3. Generate books from completed campaigns
4. Create CLI command
5. Documentation

**Deliverable**: Fully integrated campaign book generation system

---

## Technical Architecture

### Core Classes

```python
# Main generator
class CampaignBookGenerator:
    def generate_campaign_book(self) -> Path:
        """Generate complete campaign book PDF."""
        pass

# Data structure
@dataclass
class CampaignData:
    title: str
    subtitle: str
    level_range: str
    adventures: List[Adventure]
    npcs: List[NPC]
    locations: List[Location]
    monsters: List[Monster]
    # ... more fields

# Section generators
class CampaignBookSection:
    def generate_latex(self) -> str:
        """Generate LaTeX for this section."""
        pass

class IntroductionSection(CampaignBookSection): ...
class AdventureSection(CampaignBookSection): ...
class NPCsSection(CampaignBookSection): ...
class LocationsSection(CampaignBookSection): ...
class BestiarySection(CampaignBookSection): ...
```

### LaTeX Template Structure

```latex
\documentclass[letterpaper,twoside,twocolumn,openany]{dndbook}

% Cover page
\maketitle

% Table of contents
\tableofcontents

% Introduction
\part{Introduction}
\chapter{Campaign Overview}
...

% Adventures
\part{Adventure Path}
\chapter{Adventure 1: ...}
...

% NPCs
\part{Non-Player Characters}
\chapter{Major NPCs}
...

% Locations
\part{Locations}
\chapter{The Kingdom of Aetheria}
...

% Bestiary
\part{Bestiary}
\chapter{Creatures}
...

% Appendices
\appendix
\chapter{Random Encounters}
...
```

---

## Integration Points

### With Existing Systems

1. **Storyteller System** ✅
   - Reuse storybook generation
   - Leverage read-aloud and sidebar formatting
   - Use existing LaTeX template

2. **Campaign Orchestrator** 🔄
   - Export campaign state to CampaignData
   - Generate books from running campaigns
   - Create books from completed campaigns

3. **D&D 5e Engine** ✅
   - Use for stat blocks
   - Leverage character generation
   - Reuse monster templates

4. **Narrative Engine** ✅
   - Generate campaign descriptions
   - Create NPC backstories
   - Write location descriptions

---

## Example Usage

### Basic Usage

```python
from src.waft.campaign.campaign_book_generator import (
    CampaignBookGenerator,
    CampaignData,
    Adventure,
    NPC,
    Location,
    Monster
)

# Create campaign data
campaign = CampaignData(
    title="The Shattered Crown",
    subtitle="A D&D 5e Adventure Path",
    level_range="1-5",
    party_size="3-5",
    estimated_time="20-30 hours",
    tone="epic",
    setting="Kingdom of Aetheria",
    introduction="...",
    adventures=[
        Adventure(
            title="The Missing Prince",
            level_range="1-2",
            locations=[...],
            encounters=[...],
            npcs=[...]
        ),
        # ... more adventures
    ],
    npcs=[...],
    locations=[...],
    monsters=[...]
)

# Generate book
generator = CampaignBookGenerator(campaign)
pdf_path = generator.generate_campaign_book()
```

### From Campaign Orchestrator

```python
# After running a campaign
campaign = orchestrator.get_campaign(campaign_id)

# Export to book format
campaign_data = campaign.export_to_campaign_data()

# Generate book
generator = CampaignBookGenerator(campaign_data)
pdf_path = generator.generate_campaign_book()
```

---

## Key Design Decisions

### 1. Single Comprehensive PDF
**Decision**: Generate one complete PDF
- **Rationale**: Professional, complete, easy to use
- **Alternative**: Could generate separate PDFs per section

### 2. LaTeX for Layout
**Decision**: Use LaTeX (existing D&D 5e template)
- **Rationale**: Professional output, full control, existing infrastructure
- **Alternative**: Could add HTML/PDF alternative later

### 3. Manual + AI Content
**Decision**: Support both manual and AI-generated content
- **Rationale**: Flexibility - users can provide structure, AI fills details
- **Implementation**: Hybrid approach with GeminiNarrativeEngine

### 4. Text-Based Maps
**Decision**: Start with text-based map descriptions
- **Rationale**: No image dependencies, easy to generate, still useful
- **Future**: Add image map support later

---

## Success Criteria

### Must Have
- ✅ Generate complete campaign book PDF
- ✅ Include all essential sections
- ✅ Professional formatting
- ✅ Table of contents
- ✅ Proper LaTeX compilation

### Should Have
- ✅ Cover page
- ✅ Index
- ✅ Cross-references
- ✅ AI content generation
- ✅ Integration with CampaignOrchestrator

### Nice to Have
- ✅ Image map support
- ✅ Multiple output formats
- ✅ Interactive PDF features
- ✅ Print-ready optimization

---

## Next Steps

### Immediate (This Week)
1. ✅ Create design document (Done)
2. ⏳ Create `CampaignBookGenerator` class skeleton
3. ⏳ Design `CampaignData` dataclass
4. ⏳ Implement Introduction section
5. ⏳ Test basic compilation

### Short Term (Next 2 Weeks)
1. Implement all essential sections
2. Add table of contents
3. Improve formatting
4. Create example campaign book

### Medium Term (Next Month)
1. Add AI content generation
2. Integrate with CampaignOrchestrator
3. Create CLI command
4. Documentation

---

## Questions to Answer

1. **Content Generation**: How much should be AI-generated vs. manual?
   - **Answer**: Hybrid - user provides structure, AI fills details

2. **Maps**: How to handle maps?
   - **Answer**: Start with text descriptions, add images later

3. **Art**: How to handle artwork?
   - **Answer**: Placeholders for now, can add images later

4. **Modularity**: Should sections be optional?
   - **Answer**: Yes - essential sections required, optional sections can be skipped

5. **Output Format**: Just PDF or other formats?
   - **Answer**: PDF first, can add HTML/Markdown later

---

## Resources

### Existing Code
- `src/waft/templates/dnd5e_latex.py` - LaTeX template system
- `src/waft/pantheon/storyteller.py` - Storyteller system
- `src/waft/campaign/gemini_narrative_engine.py` - Narrative generation
- `_work_efforts/WE-260113-wfbu_*/` - Campaign orchestrator work

### Reference Materials
- Pathfinder Adventure Paths (structure reference)
- D&D 5e modules (formatting reference)
- Existing campaign PDFs in `_work_efforts/WE-260112-jqkn_*/`

---

**Status**: Design complete, ready to begin implementation  
**Priority**: High - This would be a major feature addition  
**Estimated Time**: 4-5 weeks for full implementation
