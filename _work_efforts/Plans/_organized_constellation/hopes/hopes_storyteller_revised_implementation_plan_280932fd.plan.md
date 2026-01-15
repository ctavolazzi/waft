---
name: Storyteller Revised Implementation Plan
overview: Revised implementation plan for Storyteller class based on verified assumptions. Extends existing Narrator/TavernKeeper systems, uses single file initially, leverages PDFGenerator's confirmed multi-page support, and accounts for Tracery limitations and character extraction needs.
todos:
  - id: create_storyteller_skeleton
    content: Create storyteller.py with Storyteller class skeleton, __init__, tell_story, and factory methods (from_text, from_data, from_events)
    status: pending
  - id: implement_input_parsing
    content: Implement _parse_input, _parse_text, _parse_structured_data, _parse_events methods with simple character extraction using regex
    status: pending
  - id: implement_story_structure
    content: Implement _generate_structure with linear structure (beginning/middle/end split) and basic three_act structure
    status: pending
  - id: implement_simple_narrative
    content: Implement _simple_narrative and _event_to_prose methods using template-based generation (Tracery if available, fallback to templates)
    status: pending
  - id: implement_pdf_formatting
    content: Implement _format_for_pdf to add chapter headings and scene breaks to narrative text
    status: pending
  - id: integrate_pdfgenerator
    content: Integrate with PDFGenerator.from_content() using premium style, target_pages=None for unlimited pages
    status: pending
  - id: test_minimal_version
    content: Create test script with simple text input, verify PDF generation works, check output quality
    status: pending
  - id: improve_character_extraction
    content: Enhance _extract_characters with better heuristics (context analysis, relationship detection)
    status: pending
  - id: add_setting_extraction
    content: Implement _extract_settings to identify locations and environments from text
    status: pending
  - id: prototype_tracery_complex
    content: Create proof-of-concept Tracery grammar for multi-paragraph narrative (separate prototyping task)
    status: pending

category: hopes
confidence: 0.83
constellation_date: 2026-01-14
---

# Storyteller Revised Implementation Plan

## Overview

Based on investigation findings, this plan creates a Storyteller class that:
- Extends existing `Narrator`/`TavernKeeper` systems (low coupling verified)
- Uses `PDFGenerator` with confirmed multi-page support
- Starts with single `storyteller.py` file (minimal abstractions)
- Accounts for Tracery limitations (needs proof-of-concept)
- Handles character extraction (new requirement)

## Architecture

### Core Design

**Single File Approach:**
- Start with `src/waft/evolution/storyteller.py` (single file)
- Split only if exceeds 500+ lines (following codebase patterns)
- Minimal abstractions (inline logic until used 3+ times)

**Extension Over Replacement:**
- Extend `Narrator` class rather than replace
- Use composition: Storyteller wraps Narrator
- Leverage `TavernKeeper.log_adventure()` for logging
- Reuse Tracery grammars where possible

**PDF Integration:**
- Use `PDFGenerator` with `target_pages` parameter (verified working)
- Extend `premium` style for book formatting
- Add chapter/scene break support to HTML template

## Implementation Details

### 1. Storyteller Class Structure

**File Header with Imports:**
```python
"""
Storyteller - Narrative engine that converts input into story PDFs.

Converts text, structured data, or events into narrative prose and generates PDF books.
"""

from pathlib import Path
from typing import Union, Dict, List, Any, Optional

class Storyteller:
    """
    Narrative engine that converts input into story PDFs.

    Extends Narrator for logging, uses PDFGenerator for output.
    """

    def __init__(
        self,
        input_data: Union[str, Dict, List],
        narrative_style: str = "medium",
        story_structure: str = "linear",  # Start simple
        pdf_style: str = "premium",
        narrator: Optional[Narrator] = None
    ):
        """
        Initialize Storyteller.

        Args:
            input_data: Text string, dict, or list of events
            narrative_style: Complexity level (simple/medium)
            story_structure: Structure template (linear/three_act)
            pdf_style: PDFGenerator style preset
            narrator: Optional Narrator instance (creates if None)
        """
        # Create or use existing Narrator
        if narrator is None:
            from ..core.tavern_keeper import TavernKeeper, Narrator
            tavern = TavernKeeper(Path.cwd())
            self.narrator = Narrator(tavern)
        else:
            self.narrator = narrator

        self.input_data = input_data
        self.narrative_style = narrative_style
        self.story_structure = story_structure
        self.pdf_style = pdf_style

        # Narrative state (for consistency)
        self.characters: Dict[str, Dict] = {}
        self.settings: Dict[str, Dict] = {}
        self.timeline: List[Dict] = []

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
        # 1. Parse input
        narrative_data = self._parse_input()

        # 2. Generate narrative structure
        story_structure = self._generate_structure(narrative_data)

        # 3. Generate narrative prose
        narrative_text = self._generate_narrative(story_structure)

        # 4. Format for PDF
        formatted_content = self._format_for_pdf(narrative_text)

        # 5. Generate PDF
        from .pdf_generator import PDFGenerator
        generator = PDFGenerator.from_content(
            content=formatted_content,
            title=title or "Generated Story",
            style=self.pdf_style
        )

        return generator.save(
            output_path=output_path,
            target_pages=None,  # No limit for books
            open_pdf=open_pdf
        )

    @classmethod
    def from_text(cls, text: str, **kwargs) -> "Storyteller":
        """Create Storyteller from text input."""
        return cls(input_data=text, **kwargs)

    @classmethod
    def from_data(cls, data: Dict, **kwargs) -> "Storyteller":
        """Create Storyteller from structured data."""
        return cls(input_data=data, **kwargs)

    @classmethod
    def from_events(cls, events: List[Dict], **kwargs) -> "Storyteller":
        """Create Storyteller from event list."""
        return cls(input_data=events, **kwargs)
```

### 2. Input Processing

**Text Input:**
```python
def _parse_input(self) -> Dict[str, Any]:
    """Parse input into narrative elements."""
    if isinstance(self.input_data, str):
        return self._parse_text(self.input_data)
    elif isinstance(self.input_data, dict):
        return self._parse_structured_data(self.input_data)
    elif isinstance(self.input_data, list):
        return self._parse_events(self.input_data)
    else:
        raise ValueError(f"Unsupported input type: {type(self.input_data)}")

def _parse_text(self, text: str) -> Dict[str, Any]:
    """Extract narrative elements from text."""
    # Use ChatDistiller for basic extraction
    from .chat_distiller import ChatDistiller
    distiller = ChatDistiller()
    distilled = distiller.distill_text(text)

    # Extract characters (simple: proper nouns, repeated entities)
    characters = self._extract_characters(text)

    # Extract settings (locations mentioned)
    settings = self._extract_settings(text)

    # Extract timeline (sequence of events from ideas)
    timeline = self._extract_timeline(distilled.ideas)

    return {
        "characters": characters,
        "settings": settings,
        "timeline": timeline,
        "ideas": distilled.ideas,
        "summary": distilled.summary
    }
```

**Character Extraction (Simple Approach):**
```python
def _extract_characters(self, text: str) -> Dict[str, Dict]:
    """Extract characters from text (simple approach)."""
    import re
    from collections import Counter

    # Find capitalized words (potential names)
    # Simple heuristic: capitalized words that appear multiple times
    words = re.findall(r'\b[A-Z][a-z]+\b', text)
    word_counts = Counter(words)

    # Filter: must appear 2+ times and not be common words
    common_words = {'The', 'This', 'That', 'There', 'When', 'Where', 'What'}
    characters = {}

    for word, count in word_counts.items():
        if count >= 2 and word not in common_words:
            characters[word] = {
                "name": word,
                "mentions": count,
                "attributes": {}  # Will be filled from context
            }

    return characters
```

**Structured Data:**
```python
def _parse_structured_data(self, data: Dict) -> Dict[str, Any]:
    """Parse structured data (characters, events already defined)."""
    return {
        "characters": data.get("characters", {}),
        "settings": data.get("settings", {}),
        "timeline": data.get("events", []),
        "ideas": [],
        "summary": data.get("summary", "")
    }

def _parse_events(self, events: List[Dict]) -> Dict[str, Any]:
    """Parse list of events into narrative structure."""
    # Extract characters from events
    characters = {}
    settings = {}
    timeline = []
    
    for event in events:
        # Add to timeline
        timeline.append(event)
        
        # Extract character if present
        if "character" in event:
            char_name = event["character"]
            if char_name not in characters:
                characters[char_name] = {
                    "name": char_name,
                    "mentions": 0,
                    "attributes": {}
                }
            characters[char_name]["mentions"] += 1
        
        # Extract setting if present
        if "location" in event:
            location = event["location"]
            if location not in settings:
                settings[location] = {
                    "name": location,
                    "mentions": 0
                }
            settings[location]["mentions"] += 1
    
    return {
        "characters": characters,
        "settings": settings,
        "timeline": timeline,
        "ideas": [],
        "summary": f"Story with {len(events)} events"
    }

def _extract_settings(self, text: str) -> Dict[str, Dict]:
    """Extract settings/locations from text (simple approach)."""
    import re
    from collections import Counter
    
    # Find location indicators (simple patterns)
    location_patterns = [
        r'\b(?:in|at|from|to|near|around)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
        r'\b(the|a|an)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
    ]
    
    locations = []
    for pattern in location_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if isinstance(match, tuple):
                locations.extend([m for m in match if m and m[0].isupper()])
            else:
                if match and match[0].isupper():
                    locations.append(match)
    
    location_counts = Counter(locations)
    
    # Filter common words and low-frequency mentions
    common_words = {'The', 'This', 'That', 'There', 'When', 'Where', 'What', 'How', 'Why'}
    settings = {}
    
    for location, count in location_counts.items():
        if count >= 2 and location not in common_words and len(location) > 2:
            settings[location] = {
                "name": location,
                "mentions": count
            }
    
    return settings

def _extract_timeline(self, ideas: List) -> List[Dict]:
    """Extract timeline of events from ideas."""
    timeline = []
    
    # Convert ideas to timeline events
    for idea in ideas:
        event = {
            "description": idea.content if hasattr(idea, 'content') else str(idea),
            "category": idea.category if hasattr(idea, 'category') else "event",
            "importance": idea.importance if hasattr(idea, 'importance') else 0.5,
            "timestamp": idea.extracted_at if hasattr(idea, 'extracted_at') else None
        }
        timeline.append(event)
    
    # Sort by timestamp if available, otherwise by order
    timeline.sort(key=lambda x: x.get("timestamp") or "")
    
    return timeline
```

### 3. Narrative Structure Generation

**Simple Linear Structure (Start Here):**
```python
def _generate_structure(self, narrative_data: Dict) -> Dict[str, Any]:
    """Generate story structure from narrative data."""

    if self.story_structure == "linear":
        return self._linear_structure(narrative_data)
    elif self.story_structure == "three_act":
        return self._three_act_structure(narrative_data)
    else:
        return self._linear_structure(narrative_data)  # Default

def _linear_structure(self, data: Dict) -> Dict[str, Any]:
    """Simple linear structure: beginning, middle, end."""
    timeline = data["timeline"]

    # Split timeline into three parts
    total = len(timeline)
    beginning = timeline[:total//3]
    middle = timeline[total//3:2*total//3]
    end = timeline[2*total//3:]

    return {
        "beginning": beginning,
        "middle": middle,
        "end": end,
        "characters": data["characters"],
        "settings": data["settings"]
    }
```

### 4. Narrative Generation

**Tracery-Based (Start Simple):**
```python
def _generate_narrative(self, structure: Dict) -> str:
    """Generate narrative prose from structure."""

    if self.narrative_style == "simple":
        return self._simple_narrative(structure)
    elif self.narrative_style == "medium":
        return self._medium_narrative(structure)
    else:
        return self._simple_narrative(structure)

def _simple_narrative(self, structure: Dict) -> str:
    """Simple narrative: paragraph per event."""
    paragraphs = []

    # Beginning
    paragraphs.append("# Beginning\n\n")
    for event in structure["beginning"]:
        paragraphs.append(self._event_to_prose(event))

    # Middle
    paragraphs.append("\n# Middle\n\n")
    for event in structure["middle"]:
        paragraphs.append(self._event_to_prose(event))

    # End
    paragraphs.append("\n# End\n\n")
    for event in structure["end"]:
        paragraphs.append(self._event_to_prose(event))

    return "\n\n".join(paragraphs)

def _event_to_prose(self, event: Dict) -> str:
    """Convert event to prose (simple template-based)."""
    # Use Tracery if available, fallback to simple template
    try:
        import tracery
        from tracery.modifiers import base_english
        from ..core.tavern_keeper.grammars import SUCCESS_GRAMMAR
        
        # Create Tracery grammar from existing grammar dict
        grammar = tracery.Grammar(SUCCESS_GRAMMAR)
        grammar.add_modifiers(base_english)
        
        # Generate narrative using Tracery
        narrative = grammar.flatten("#origin#")
        
        # Replace placeholders with event data if present
        if "location" in event:
            narrative = narrative.replace("#component#", event["location"])
        if "action" in event:
            narrative = narrative.replace("#action#", event["action"])
        if "description" in event:
            narrative = narrative.replace("#narrative#", event["description"])
        
        return narrative
    except (ImportError, AttributeError):
        # Fallback: simple template
        return f"{event.get('description', 'An event occurred')}."
```

**Medium Complexity (Tracery with State):**
```python
def _medium_narrative(self, structure: Dict) -> str:
    """Medium complexity: characters, dialogue, arcs."""
    # This requires Tracery proof-of-concept first
    # For now, use simple narrative with character names
    narrative = self._simple_narrative(structure)

    # Add character references
    for char_name, char_data in structure["characters"].items():
        narrative = narrative.replace(char_name, f"**{char_name}**")

    return narrative
```

### 5. PDF Formatting

**Extend Premium Style:**
```python
def _format_for_pdf(self, narrative: str) -> str:
    """Format narrative for PDF with book-style elements."""

    # Add chapter headings if structure detected
    if "# Beginning" in narrative:
        narrative = narrative.replace("# Beginning", "## Chapter 1: Beginning")
    if "# Middle" in narrative:
        narrative = narrative.replace("# Middle", "## Chapter 2: Middle")
    if "# End" in narrative:
        narrative = narrative.replace("# End", "## Chapter 3: End")

    # Add scene breaks (double newlines)
    narrative = narrative.replace("\n\n\n", "\n\n---\n\n")

    return narrative
```

### 6. Integration with PDFGenerator

**Use Existing System:**
```python
# In tell_story() method:
from .pdf_generator import PDFGenerator

generator = PDFGenerator.from_content(
    content=formatted_content,
    title=title or "Generated Story",
    style=self.pdf_style  # "premium" for book-like formatting
)

# Generate with no page limit
return generator.save(
    output_path=output_path,
    target_pages=None,  # No limit - let it be as long as needed
    open_pdf=open_pdf
)
```

## File Structure

```
src/waft/evolution/
└── storyteller.py              # Single file (start here)
    - Storyteller class
    - Input parsing methods
    - Narrative generation methods
    - PDF formatting methods
    - Character/setting extraction (simple)
```

**Split Only If:**
- File exceeds 500+ lines
- Clear separation of concerns emerges
- Methods used 3+ times elsewhere

## Dependencies

**Existing (Verified):**
- `PDFGenerator` - Multi-page PDF generation ✅
- `Narrator`/`TavernKeeper` - Logging and narrative patterns ✅
- `ChatDistiller` - Text extraction (for ideas) ✅
- `StylingGenome` - PDF styling ✅

**New (Minimal):**
- Tracery (already in codebase) - Narrative generation
- Simple regex/NLP for character extraction (no new libraries initially)

**Optional (If Needed):**
- NLP library for better character extraction (spaCy, NLTK)
- LLM integration (if Tracery insufficient)

## Implementation Phases

### Phase 1: Minimal Viable Storyteller (Week 1)
1. Create `storyteller.py` skeleton
2. Implement text input parsing (simple character extraction)
3. Implement linear story structure
4. Implement simple narrative generation (template-based)
5. Integrate with PDFGenerator
6. Test with simple input

**Deliverable**: Can generate basic narrative PDF from text

### Phase 2: Character & Structure (Week 2)
1. Improve character extraction
2. Add three-act structure template
3. Add setting extraction
4. Enhance narrative prose generation
5. Test with structured data input

**Deliverable**: Can generate structured narratives with characters

### Phase 3: Medium Complexity (Week 3)
1. Prototype Tracery complex grammar (if Phase 1/2 successful)
2. Add dialogue generation (if Tracery supports)
3. Add character arcs (simple state tracking)
4. Add consistency checking (basic)
5. Test medium complexity output

**Deliverable**: Can generate medium complexity narratives

### Phase 4: Polish & Extend (Week 4)
1. Add more story structure templates
2. Improve prose quality
3. Add book-style PDF formatting (chapters, scene breaks)
4. Performance optimization
5. Documentation and examples

**Deliverable**: Production-ready Storyteller

## Risk Mitigation

### Tracery Limitations
- **Risk**: Tracery can't handle medium complexity
- **Mitigation**: Start with simple templates, add Tracery incrementally
- **Fallback**: Use template-based generation if Tracery insufficient

### Character Extraction
- **Risk**: Simple extraction insufficient
- **Mitigation**: Start with simple regex, improve incrementally
- **Fallback**: Require explicit character definition for text input

### Performance
- **Risk**: Slow generation for long narratives
- **Mitigation**: Test early with realistic inputs
- **Fallback**: Add caching, optimize algorithms

## Example Usage

```python
from src.waft.evolution.storyteller import Storyteller

# From text (simple)
storyteller = Storyteller.from_text(
    text="Alice started working on the project. She encountered a bug. She fixed it.",
    narrative_style="simple",
    story_structure="linear"
)
pdf_path = storyteller.tell_story(title="Alice's Adventure")

# From structured data
events = [
    {"character": "Developer", "action": "started work", "time": "morning"},
    {"character": "Developer", "action": "encountered bug", "time": "afternoon"},
    {"character": "Developer", "action": "solved bug", "time": "evening"}
]
storyteller = Storyteller.from_events(events)
pdf_path = storyteller.tell_story()
```

## Success Criteria

**Phase 1 Success:**
- Can generate PDF from text input
- Output is readable narrative (not just bullet points)
- PDF has multiple pages if content is long

**Phase 2 Success:**
- Characters are identified and referenced consistently
- Story has clear structure (beginning/middle/end)
- Settings are mentioned appropriately

**Phase 3 Success:**
- Narrative has character dialogue (if Tracery supports)
- Character arcs are visible (character changes over time)
- Output quality meets "medium complexity" definition

## Next Steps

1. **Prototype Tracery complex grammar** (separate prototyping plan)
2. **Test PDFGenerator at 50+ pages** (verify performance)
3. **Define "medium complexity"** (create example outputs)
4. **Start Phase 1 implementation** (minimal viable version)