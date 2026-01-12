# Storyteller Assumptions Investigation Report

**Date**: 2026-01-12  
**Time**: 05:27:35 PST  
**Purpose**: Verify critical assumptions from assumptions analysis through codebase investigation

---

## Investigation Methodology

1. Codebase analysis of existing narrative systems
2. Code review of PDFGenerator and TwoPageGenerator
3. Web research on Tracery capabilities
4. Dependency analysis of Narrator/TavernKeeper coupling
5. Examples search for multi-page PDF generation

---

## Critical Assumption #1: Tracery Can Handle Medium Complexity

### Investigation Results

**Current Tracery Usage in Codebase:**
- Single-sentence narratives only
- Example: "The foundation holds firm as entropy dissipates."
- Grammar structure: Simple placeholder replacement
- No examples of multi-paragraph narratives
- No examples of character dialogue
- No examples of stateful narratives

**Web Research Findings:**
- Tracery CAN generate multi-paragraph narratives with proper grammar structuring
- Requires higher-level rules (paragraphs, scenes, chapters)
- Can use recursive expansion for complex narratives
- BUT: No evidence in codebase that this has been done
- Alternative libraries exist: `pynarrative`, `storytelling` for complex narratives

**Code Evidence:**
```python
# src/waft/core/tavern_keeper/keeper.py:419
tracery_grammar = tracery.Grammar(grammar)
narrative = tracery_grammar.flatten("#origin#")  # Single sentence output
```

**Verdict**: ⚠️ **PARTIALLY VERIFIED**
- Tracery CAN theoretically handle medium complexity
- But requires significant grammar restructuring
- No evidence in codebase of this capability being used
- Would need to build complex grammar structures from scratch

**Risk Level**: MEDIUM - Feasible but requires work

---

## Critical Assumption #2: PDFGenerator Scales to Book-Length

### Investigation Results

**Code Evidence:**
```python
# src/waft/evolution/pdf_generator.py:335
generator = TwoPageGenerator(weasyprint_available=True, allowed_pages=target_pages or 50)
```

**Examples Found:**
- `generate_session_recap_pdf_waft.py`: Uses `target_pages=20` and `target_pages=50`
- `generate_session_recap_pdf_full.py`: Generates multi-page PDFs with all content
- Code comment: "allowed_pages: Target page count (default: 2, can be any number)"

**Adaptive Algorithm Analysis:**
```python
# src/waft/evolution/two_page_generator.py:648-701
for iteration in range(self.max_iterations):  # Default: 5 iterations
    # Adjust idea count
    if page_count > target_pages:
        ideas_to_show = max(3, int(ideas_to_show * 0.75))  # Reduce
    else:
        ideas_to_show = min(len(all_ideas), int(ideas_to_show * 1.3))  # Increase
```

**Potential Issues:**
- Algorithm designed for 2-page constraint enforcement
- May not scale efficiently to 50+ pages
- Only 5 iterations by default (may not be enough for large targets)
- Algorithm reduces/increases idea count - may not work well for book-length content

**Verdict**: ✅ **VERIFIED WITH CAVEATS**
- Multi-page support exists and is used
- BUT: Algorithm may not be optimal for book-length content
- May need algorithm adjustments for 50+ pages

**Risk Level**: LOW - Works but may need optimization

---

## Critical Assumption #3: Extending Narrator/TavernKeeper is Feasible

### Investigation Results

**Coupling Analysis:**

**Narrator Dependencies:**
```python
# src/waft/core/tavern_keeper/narrator.py:23
def __init__(self, tavern_keeper: TavernKeeper):
    self.tavern = tavern_keeper

# All methods only call:
self.tavern.log_adventure(entry)
```

**TavernKeeper.log_adventure():**
```python
# src/waft/core/tavern_keeper/keeper.py:655
def log_adventure(self, event: Dict[str, Any]) -> None:
    # Just logs to TinyDB or JSON file
    if self.db:
        self.db.table("adventure_journal").insert(event)
    else:
        self._data.setdefault("adventure_journal", []).append(event)
```

**Dependency Summary:**
- Narrator only depends on `log_adventure()` method
- `log_adventure()` is simple logging (TinyDB or JSON)
- No complex dependencies
- TavernKeeper has `get_narrator()` factory method

**Verdict**: ✅ **VERIFIED - LOW COUPLING**
- Narrator is loosely coupled to TavernKeeper
- Only dependency is logging method
- Extension is feasible without breaking changes
- Could even use composition (pass logger instead of full TavernKeeper)

**Risk Level**: LOW - Extension is safe

---

## Critical Assumption #4: "Medium Complexity" is Achievable with Templates

### Investigation Results

**Current Narrative Complexity:**
- Single sentences: ✅ Working
- Multi-paragraph: ❓ Not tested
- Character dialogue: ❓ Not implemented
- Character arcs: ❓ Not implemented
- Stateful narratives: ❓ Not implemented

**Tracery Capabilities (from research):**
- Can generate multi-paragraph with proper grammar structure
- Can handle dialogue with grammar rules
- Can maintain state through grammar rules (but limited)
- Character arcs would require external state tracking

**Verdict**: ⚠️ **UNCLEAR - NEEDS PROTOTYPING**
- Templates CAN theoretically achieve medium complexity
- But requires significant grammar engineering
- Character arcs and consistency need external state (not just Tracery)
- No proof-of-concept exists

**Risk Level**: MEDIUM - Feasible but unproven

---

## Additional Findings

### 1. Performance Considerations

**Adaptive Algorithm:**
- Default: 5 iterations max
- Each iteration: Generate HTML → Count pages → Adjust
- For 50+ pages, may need more iterations
- Performance: O(n) where n = iterations (typically 5)

**Memory:**
- HTML content stored in memory
- For book-length: Could be large but manageable
- No evidence of memory issues in examples

**Verdict**: Performance likely acceptable, but may need iteration limit adjustment

### 2. Input Processing

**ChatDistiller Limitations:**
- Designed for 2-page PDFs (extracts "top ideas")
- Categories: decision/insight/action/concept/question
- Doesn't extract: characters, settings, story structure
- Would need narrative-specific extraction

**Verdict**: ChatDistiller insufficient for narrative extraction - need new approach

### 3. Styling System

**Existing Presets:**
- `premium`: Serif fonts, generous margins ✅
- `clinical_standard`: Times New Roman, 1-inch margins ✅
- `professional`: Georgia serif ✅

**Missing Features:**
- Chapter headings (not in template)
- Scene breaks (not in template)
- Dialogue formatting (not in template)
- Table of contents (not implemented)

**Verdict**: Styling can be extended, but needs template modifications

---

## Revised Risk Assessment

### ✅ LOW RISK (Verified)
1. **PDFGenerator multi-page support** - Confirmed working, examples exist
2. **Narrator/TavernKeeper extension** - Low coupling, safe to extend

### ⚠️ MEDIUM RISK (Partially Verified)
1. **Tracery medium complexity** - Theoretically possible, needs proof-of-concept
2. **"Medium complexity" definition** - Unclear what's actually required
3. **Performance at scale** - Algorithm may need adjustment for 50+ pages

### 🔴 HIGH RISK (Unverified)
1. **Character extraction from text** - No system exists, complexity unknown
2. **Narrative structure generation** - No templates exist for story structures
3. **Consistency engine** - May be required but dismissed as "overkill"

---

## Recommendations

### Immediate Actions (Before Implementation)

1. **Prototype Tracery Complex Grammar**
   - Create test grammar for multi-paragraph narrative
   - Test character dialogue generation
   - Verify stateful narrative capability
   - Document limitations

2. **Test PDFGenerator at Scale**
   - Generate test PDF with 50 pages
   - Measure performance (time, memory)
   - Verify adaptive algorithm works correctly
   - Document any issues

3. **Define "Medium Complexity"**
   - Create example output (what should it look like?)
   - Specify requirements (characters? dialogue? arcs?)
   - Set quality expectations
   - Create acceptance criteria

4. **Investigate Character Extraction**
   - Research NLP libraries for entity extraction
   - Test extraction from sample text
   - Estimate complexity
   - Decide: extract vs. require explicit definition

### Architecture Decisions Needed

1. **Tracery vs. LLM**
   - If Tracery insufficient, need LLM integration
   - Hybrid approach: Tracery for structure, LLM for prose?
   - Cost/performance trade-offs

2. **Extension vs. New Class**
   - Narrator can be extended (low coupling)
   - But Storyteller may need different interface
   - Consider: Composition over inheritance?

3. **Consistency Engine**
   - Is it really "overkill"?
   - What's minimum consistency needed?
   - Simple state tracking vs. full engine?

---

## Conclusion

**Key Findings:**
1. ✅ PDFGenerator CAN handle multi-page books (verified with examples)
2. ✅ Narrator/TavernKeeper CAN be extended (low coupling verified)
3. ⚠️ Tracery CAN theoretically handle medium complexity (needs proof-of-concept)
4. ❓ "Medium complexity" is undefined (needs specification)

**Critical Gaps:**
- No proof Tracery can generate book-length narratives
- No character extraction system exists
- No narrative structure templates exist
- "Medium complexity" requirements undefined

**Next Steps:**
1. Prototype Tracery complex grammar
2. Test PDFGenerator at 50+ pages
3. Define "medium complexity" with examples
4. Investigate character extraction options
5. Then create revised implementation plan

---

**Status**: Investigation complete. Ready for prototyping phase before final plan.
