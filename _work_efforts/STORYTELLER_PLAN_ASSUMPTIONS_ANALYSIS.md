# Storyteller Plan: Assumptions Analysis

**Date**: 2026-01-12  
**Purpose**: Investigate assumptions in the Storyteller implementation plan to discover a better approach

---

## Assumptions Identified

### 1. **Architectural Assumptions**

#### A1: We need separate modules for each component
**Assumption**: Storyteller requires 6 separate files:
- `narrative_structure.py`
- `narrative_characters.py`
- `narrative_settings.py`
- `narrative_prose.py`
- `narrative_consistency.py`

**Verification**: 
- ❌ **FALSE**: Existing codebase shows preference for minimal abstractions
- Evidence: `PDFGenerator` is a single file with composable methods
- Evidence: Coding style guide says "No unnecessary abstractions - Write code inline unless it's used 3+ times"
- **Better approach**: Start with single `storyteller.py` file, split only if it exceeds 500+ lines

#### A2: We need to build everything from scratch
**Assumption**: All narrative generation must be built new

**Verification**:
- ❌ **FALSE**: Existing narrative systems exist:
  - `TavernKeeper.narrate()` - Uses Tracery grammars for narrative generation
  - `Narrator` class - Handles observations, reflections, celebrations
  - `LabEntryGenerator` - Generates narrative lab entries with structure
  - Tracery grammars already defined for success/failure/level_up narratives
- **Better approach**: Extend existing `Narrator`/`TavernKeeper` systems rather than building new

#### A3: ChatDistiller is the right tool for text input
**Assumption**: Use ChatDistiller to extract ideas from text input

**Verification**:
- ⚠️ **PARTIALLY TRUE**: ChatDistiller extracts ideas, but:
  - It's designed for 2-page PDFs (extracts "top ideas")
  - It categorizes as "decision/insight/action/concept/question" - not narrative elements
  - It doesn't extract characters, settings, or story structure
- **Better approach**: May need narrative-specific extraction, or extend ChatDistiller

### 2. **PDF Generation Assumptions**

#### A4: PDFGenerator can handle book-length content
**Assumption**: PDFGenerator can generate multi-page books

**Verification**:
- ✅ **TRUE**: 
  - `TwoPageGenerator` has `allowed_pages` parameter (default: 2, but configurable)
  - `PDFGenerator.save()` has `target_pages: Optional[int] = None` (None = no limit)
  - Code comment: "allowed_pages: Target page count (default: 2, can be any number)"
  - Example: `TwoPageGenerator(weasyprint_available=True, allowed_pages=target_pages or 50)`
- **Conclusion**: System already supports multi-page PDFs

#### A5: We need narrative-specific PDF styling
**Assumption**: Need new book-style formatting (larger margins, serif fonts, etc.)

**Verification**:
- ⚠️ **PARTIALLY TRUE**:
  - Existing presets: `clinical_standard`, `premium`, `professional`
  - `premium` already has serif fonts, generous margins
  - But may need chapter headings, scene breaks, dialogue formatting
- **Better approach**: Extend existing styling presets rather than creating entirely new system

### 3. **Narrative Generation Assumptions**

#### A6: We need LLM integration for narrative generation
**Assumption**: "May need LLM calls for sophisticated narrative generation"

**Verification**:
- ❓ **UNCLEAR**: 
  - No LLM integration found in codebase (grep found no matches)
  - Existing narrative uses Tracery grammars (template-based)
  - `TavernKeeper.narrate()` uses Tracery, not LLM
- **Question**: Can template-based (Tracery) approach work for medium complexity narratives?
- **Better approach**: Start with Tracery/grammar-based, add LLM only if needed

#### A7: Character extraction from input is necessary
**Assumption**: Must extract characters from input (names, pronouns, entities)

**Verification**:
- ⚠️ **DEPENDS ON INPUT TYPE**:
  - For structured data: Characters may already be defined
  - For text: Extraction needed, but complexity varies
  - Existing: No character extraction system found
- **Better approach**: Support both explicit character definition and automatic extraction

#### A8: Story structure templates are required
**Assumption**: Need templates for three-act, hero's journey, etc.

**Verification**:
- ✅ **TRUE**: Templates would help, but:
  - Existing: `LabEntryGenerator` has structure (Technical → Personal → Realization → Post-Realization)
  - This shows structure templates can work
- **Better approach**: Start with simple structure, add templates incrementally

### 4. **Consistency Assumptions**

#### A9: We need a separate consistency engine
**Assumption**: Need `narrative_consistency.py` for logical validation

**Verification**:
- ⚠️ **MAYBE OVERKILL**:
  - For medium complexity: Basic state tracking may suffice
  - Full consistency engine might be premature optimization
  - Existing: No consistency engine found in codebase
- **Better approach**: Start with simple state tracking, add consistency checking incrementally

### 5. **Integration Assumptions**

#### A10: Existing narrative systems aren't sufficient
**Assumption**: TavernKeeper Narrator can't be extended for Storyteller

**Verification**:
- ❌ **FALSE**: 
  - `Narrator` handles observations, reflections, celebrations
  - `TavernKeeper.narrate()` generates narratives from events
  - Tracery grammars already defined
  - These could be extended rather than replaced
- **Better approach**: Extend `Narrator`/`TavernKeeper` for book-length narratives

#### A11: Medium complexity requires all these components
**Assumption**: Medium complexity = characters + settings + dialogue + arcs + consistency

**Verification**:
- ❓ **UNCLEAR**: 
  - "Medium complexity" is subjective
  - Could start simpler: basic narrative with characters and structure
  - Add complexity incrementally
- **Better approach**: Start minimal, add features based on actual needs

---

## Key Discoveries

### 1. **Existing Narrative Infrastructure**
- ✅ Tracery grammars already exist (`src/waft/core/tavern_keeper/grammars.py`)
- ✅ `Narrator` class for narrative contributions
- ✅ `TavernKeeper.narrate()` for event-based narratives
- ✅ `LabEntryGenerator` shows narrative structure patterns

### 2. **PDF System Capabilities**
- ✅ Multi-page support already exists (`allowed_pages` parameter)
- ✅ Styling presets available (`premium` style for book-like formatting)
- ✅ Component system for adaptive layouts

### 3. **Codebase Patterns**
- ✅ Preference for minimal abstractions (single files until 500+ lines)
- ✅ Composable APIs (like `PDFGenerator.from_content()`)
- ✅ Template-based generation (Tracery, not LLM)

---

## Revised Assumptions (What We Actually Know)

### ✅ **TRUE Assumptions**
1. PDFGenerator can handle multi-page books (via `allowed_pages`)
2. Story structure templates would be useful
3. Existing styling can be extended for book formatting

### ❌ **FALSE Assumptions**
1. Need 6 separate modules (should start with 1 file)
2. Need to build everything from scratch (extend existing systems)
3. Existing narrative systems aren't sufficient (can extend Narrator/TavernKeeper)

### ⚠️ **UNCLEAR/NEEDS INVESTIGATION**
1. Whether Tracery grammars can handle medium complexity (vs. needing LLM)
2. Whether character extraction is needed (depends on input)
3. Whether full consistency engine is needed (may be overkill)

---

## Better Plan Hypothesis

**Hypothesis**: A simpler plan exists that:
1. Extends existing `Narrator`/`TavernKeeper` systems
2. Uses single `storyteller.py` file initially
3. Leverages Tracery grammars for narrative generation
4. Uses existing PDFGenerator with `allowed_pages` for multi-page books
5. Starts minimal, adds complexity incrementally

**Key Insight**: The codebase already has narrative infrastructure. We should extend it rather than replace it.

---

## Next Steps

1. **Verify Tracery capabilities**: Can Tracery handle character dialogue and arcs?
2. **Test multi-page PDFs**: Verify `allowed_pages` works for book-length content
3. **Prototype minimal version**: Single file, basic narrative, extend existing systems
4. **Iterate**: Add features (characters, settings, consistency) only as needed

---

## Questions to Answer

1. **Q**: Can Tracery grammars generate character dialogue and arcs?
   - **Investigation needed**: Review Tracery documentation, test with complex grammars

2. **Q**: What's the actual requirement for "medium complexity"?
   - **Clarification needed**: Examples of desired output would help

3. **Q**: Should we extend Narrator or create new Storyteller?
   - **Decision needed**: Extend vs. new class

4. **Q**: Do we need LLM integration, or can templates work?
   - **Investigation needed**: Prototype with Tracery first, add LLM if needed
