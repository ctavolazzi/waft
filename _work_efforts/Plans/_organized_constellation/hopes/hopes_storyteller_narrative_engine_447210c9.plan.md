---
name: Storyteller Narrative Engine
overview: Create a Storyteller class that transforms any input (text or structured data) into a narrative PDF book with character arcs, settings, logical consistency, story structure, dialogue, and prose. The class will integrate with existing PDF generation infrastructure while adding sophisticated narrative transformation capabilities.
todos:
  - id: create_storyteller_skeleton
    content: Create Storyteller class skeleton in src/waft/evolution/storyteller.py with basic structure, input parsing methods (from_text, from_data, from_events), and tell_story method
    status: pending
  - id: implement_input_parsing
    content: "Implement input parsing: text input using ChatDistiller, structured data parsing, event sequence extraction, character/setting identification"
    status: pending
  - id: create_narrative_structure
    content: Create narrative_structure.py with story structure templates (three-act, hero journey), scene/chapter organization, and pacing management
    status: pending
  - id: implement_character_engine
    content: "Create narrative_characters.py: character extraction from input, character arc generation, dialogue voice differentiation, character consistency tracking"
    status: pending
  - id: implement_setting_generator
    content: "Create narrative_settings.py: setting extraction, world-building consistency, environmental description generation"
    status: pending
  - id: implement_prose_generator
    content: "Create narrative_prose.py: narrative prose generation, dialogue formatting, descriptive text, style consistency"
    status: pending
  - id: implement_consistency_engine
    content: "Create narrative_consistency.py: logical consistency checking, timeline tracking, character/setting consistency validation, plot coherence"
    status: pending
  - id: integrate_pdf_generation
    content: "Integrate with PDFGenerator: create narrative-specific styling preset, format chapters/scenes, add table of contents, implement book-style formatting"
    status: pending
  - id: create_example_usage
    content: Create example script demonstrating Storyteller usage with both text and structured data inputs
    status: pending
  - id: add_tests
    content: Add unit tests for character extraction, narrative structure generation, consistency checking, and PDF output
    status: pending

category: hopes
confidence: 0.55
constellation_date: 2026-01-14
---

# Storyteller Narrative Engine Implementation Plan

## Overview

The Storyteller class will be a narrative engine that converts input (text or structured data) into a complete narrative PDF book. It will generate stories with character arcs, settings, logical consistency, story structure, dialogue, and prose.

## Architecture

### Core Components

1. **Storyteller Class** (`src/waft/evolution/storyteller.py`)

   - Main orchestrator class
   - Handles input parsing (text/structured data)
   - Coordinates narrative generation pipeline
   - Integrates with PDFGenerator for output

2. **Narrative Structure** (`src/waft/evolution/narrative_structure.py`)

   - Story structure templates (3-act, hero's journey, etc.)
   - Scene/chapter organization
   - Pacing and flow management

3. **Character Engine** (`src/waft/evolution/narrative_characters.py`)

   - Character extraction from input
   - Character arc generation
   - Character consistency tracking
   - Dialogue voice differentiation

4. **Setting Generator** (`src/waft/evolution/narrative_settings.py`)

   - Setting extraction and generation
   - World-building consistency
   - Environmental descriptions

5. **Prose Generator** (`src/waft/evolution/narrative_prose.py`)

   - Narrative prose generation
   - Dialogue formatting
   - Descriptive text generation
   - Style consistency

6. **Consistency Engine** (`src/waft/evolution/narrative_consistency.py`)

   - Logical consistency checking
   - Timeline tracking
   - Character/setting consistency
   - Plot coherence validation

## Implementation Details

### 1. Storyteller Class Structure

```python
class Storyteller:
    """
    Narrative engine that converts input into story PDFs.

    Capabilities:
 - Accept text or structured data input
 - Extract characters, settings, events
 - Generate narrative structure
 - Create character arcs
 - Generate dialogue and prose
 - Ensure logical consistency
 - Output as PDF book
    """

    def __init__(
        self,
        input_data: Union[str, Dict, List],
        narrative_style: str = "medium",
        story_structure: str = "three_act",
        pdf_style: str = "premium"
    ):
        """
        Initialize Storyteller.

        Args:
            input_data: Text string, dict, or list of events
            narrative_style: Complexity level (simple/medium/novel)
            story_structure: Structure template (three_act/hero_journey/etc)
            pdf_style: PDFGenerator style preset
        """

    def tell_story(
        self,
        output_path: Optional[Path] = None,
        title: Optional[str] = None,
        open_pdf: bool = False
    ) -> Path:
        """
        Generate complete narrative PDF.

        Returns:
            Path to generated PDF
        """

    @classmethod
    def from_text(cls, text: str, **kwargs) -> "Storyteller":
        """Create Storyteller from text input."""

    @classmethod
    def from_data(cls, data: Dict, **kwargs) -> "Storyteller":
        """Create Storyteller from structured data."""

    @classmethod
    def from_events(cls, events: List[Dict], **kwargs) -> "Storyteller":
        """Create Storyteller from event list."""
```

### 2. Input Processing Pipeline

**Text Input:**

- Use ChatDistiller to extract ideas/events
- Identify potential characters (proper nouns, repeated entities)
- Extract settings (locations, environments)
- Extract timeline/sequence of events
- Identify key themes and conflicts

**Structured Data:**

- Parse JSON/dict structure
- Extract character data (names, attributes, relationships)
- Extract event sequences
- Extract setting information
- Map to narrative elements

### 3. Narrative Structure Generation

**Story Structure Templates:**

- Three-Act Structure (Setup → Confrontation → Resolution)
- Hero's Journey (Call → Trials → Return)
- Freytag's Pyramid (Exposition → Rising Action → Climax → Falling Action → Resolution)

**Implementation:**

- Map extracted events to structure beats
- Create chapter/scene breaks
- Ensure proper pacing
- Build narrative tension

### 4. Character Engine

**Character Extraction:**

- Identify characters from input (names, pronouns, entities)
- Infer character attributes from context
- Track character relationships
- Identify character goals and conflicts

**Character Arc Generation:**

- Define character starting state
- Identify character growth/changes
- Create character development trajectory
- Ensure character consistency throughout

**Dialogue Generation:**

- Create distinct voices for each character
- Generate contextually appropriate dialogue
- Maintain character voice consistency
- Format dialogue with proper attribution

### 5. Setting Generator

**Setting Extraction:**

- Identify locations from input
- Extract environmental details
- Build world consistency
- Create setting descriptions

**Setting Integration:**

- Weave settings into narrative
- Use settings to enhance mood/atmosphere
- Maintain spatial/temporal consistency

### 6. Prose Generator

**Narrative Prose:**

- Generate descriptive passages
- Create narrative flow
- Vary sentence structure
- Maintain consistent tone

**Dialogue Formatting:**

- Proper dialogue tags
- Action beats
- Natural conversation flow

### 7. Consistency Engine

**Logical Consistency:**

- Timeline validation (no time travel errors)
- Character consistency (same name, attributes throughout)
- Setting consistency (locations remain consistent)
- Plot coherence (events follow logically)

**Implementation:**

- Track all narrative elements in state
- Validate against previous state
- Flag inconsistencies
- Auto-correct minor inconsistencies

### 8. PDF Integration

**Integration with PDFGenerator:**

- Use PDFGenerator for final output
- Apply narrative-specific styling
- Format chapters/scenes
- Include table of contents
- Add character list/setting guide (optional)

**Narrative-Specific Styling:**

- Book-style formatting (larger margins, serif fonts)
- Chapter headings
- Scene breaks
- Dialogue formatting
- Prose-friendly line spacing

## File Structure

```
src/waft/evolution/
├── storyteller.py              # Main Storyteller class
├── narrative_structure.py       # Story structure templates
├── narrative_characters.py     # Character extraction and arcs
├── narrative_settings.py       # Setting generation
├── narrative_prose.py          # Prose and dialogue generation
└── narrative_consistency.py    # Consistency checking
```

## Dependencies

**Existing Systems:**

- `PDFGenerator` - PDF output
- `ChatDistiller` - Text extraction (for text input)
- `StylingGenome` - PDF styling

**New Dependencies:**

- May need LLM integration for narrative generation (if not using templates)
- Pattern matching for character/setting extraction
- State tracking for consistency

## Implementation Phases

### Phase 1: Core Structure

1. Create Storyteller class skeleton
2. Implement input parsing (text and structured)
3. Basic narrative structure mapping
4. Integration with PDFGenerator

### Phase 2: Character System

1. Character extraction from input
2. Character arc generation
3. Basic dialogue generation
4. Character consistency tracking

### Phase 3: Setting & Prose

1. Setting extraction and generation
2. Prose generation engine
3. Dialogue formatting
4. Narrative flow management

### Phase 4: Consistency & Polish

1. Consistency engine implementation
2. Logical validation
3. Error correction
4. Output formatting refinement

## Example Usage

```python
from src.waft.evolution.storyteller import Storyteller

# From text
storyteller = Storyteller.from_text(
    text="User asked to build a feature. We discussed options...",
    narrative_style="medium",
    story_structure="three_act"
)
pdf_path = storyteller.tell_story(
    title="The Feature That Changed Everything",
    open_pdf=True
)

# From structured data
events = [
    {"character": "Developer", "action": "started work", "time": "morning"},
    {"character": "Developer", "action": "encountered bug", "time": "afternoon"},
    {"character": "Developer", "action": "solved bug", "time": "evening"}
]
storyteller = Storyteller.from_events(events)
pdf_path = storyteller.tell_story()
```

## Integration Points

1. **PDFGenerator**: Use for final PDF output with narrative styling
2. **ChatDistiller**: Leverage for text input processing
3. **TavernKeeper Narrator**: Could share narrative generation patterns
4. **StylingGenome**: Use for book-style PDF formatting

## Considerations

- **LLM Usage**: May need LLM calls for sophisticated narrative generation (vs. template-based)
- **Performance**: Narrative generation could be computationally expensive
- **Consistency**: Complex state tracking needed for long narratives
- **Styling**: Book-style PDF formatting (different from technical docs)
- **Extensibility**: Allow custom story structures and narrative styles