# WAFT Document Generators - Creative Testing Plan

**Date**: 2026-01-11  
**Objective**: Create 7 wildly creative document generators that test edge cases and push the system to its limits

---

## Task Understanding

**Goal**: Create comprehensive document generation system with:
- 7 creative document templates (testing different styles, layouts, edge cases)
- Example documents for each type
- Complete documentation
- Helpful tooling in organized folder structure
- Open all examples for review

**Requirements**:
1. **Eldritch Horror** - Researcher loses mind studying reality
2. **Screenplay** - Script format for film/theater
3. **Sweet Personal** - Heartfelt, gentle, personal letter
4. **Business Corporate** - Professional business document
5. **Code Documentation** - CRITICAL - Architecture, data structures, algorithms, dependencies
6. **Two more creative** - My choice (get wild!)

---

## Plan: 7 Document Generators

### 1. Eldritch Horror Research Journal
**Theme**: "Man studying reality loses his mind as reality starts looking back"

**Features to Test**:
- Progressive typography degradation
- Strikethrough, scribbles, annotations
- Strange symbols and corrupted text
- Layout breakdown (reality breaking)
- Increasingly unhinged content
- "The abyss stares back" aesthetic

**Edge Cases**:
- Text that becomes unreadable
- Overlapping annotations
- Non-standard character encoding
- Degrading margins and spacing
- Reality-breaking layout shifts

**Template**: `eldritch_journal.py`

---

### 2. Screenplay Template
**Theme**: Professional script format

**Features to Test**:
- Scene headers (INT./EXT. LOCATION - TIME)
- Character names (centered, uppercase)
- Dialogue with proper indentation
- Parentheticals (character direction)
- Action/description blocks
- Transitions (CUT TO:, FADE IN:, etc.)
- Industry-standard Courier 12pt
- Page breaks for scene changes

**Edge Cases**:
- Long dialogue that wraps
- Multiple parentheticals
- Complex action sequences
- Scene transitions
- Character name formatting

**Template**: `screenplay.py`

---

### 3. Heartfelt Personal Letter
**Theme**: Sweet, kind, gentle, personal

**Features to Test**:
- Soft, warm colors
- Handwritten-style fonts (if available)
- Decorative borders
- Personal, intimate spacing
- Optional letterhead/stationery
- Emphasis on emotion and connection
- Warm typography

**Edge Cases**:
- Long emotional content
- Multiple paragraphs
- Personal touches (decorative elements)
- Warm color palette
- Gentle spacing

**Template**: `heartfelt_letter.py`

---

### 4. Business Invoice/Contract
**Theme**: Professional corporate document

**Features to Test**:
- Company letterhead
- Invoice itemization with calculations
- Contract terms and conditions
- Legal formatting
- Signature blocks with dates
- Payment terms
- Professional business aesthetic
- Precise tables and calculations

**Edge Cases**:
- Complex itemization tables
- Legal text formatting
- Signature block positioning
- Calculation accuracy
- Multi-page contracts

**Template**: `invoice_contract.py`

---

### 5. Code Documentation (CRITICAL)
**Theme**: Technical documentation for code/APIs/architecture

**Features to Test**:
- Clear technical writing
- Code blocks with syntax highlighting
- API reference formatting
- Data structure documentation
- Algorithm explanations
- Dependency trees
- Architecture overviews
- Parameter tables
- Return value documentation
- Class/function documentation

**Edge Cases**:
- Complex code examples
- Multi-language code blocks
- Nested data structures
- Long API documentation
- Architecture diagrams (text-based)
- Dependency graphs

**Template**: `code_documentation.py`

**CRITICAL**: This must be reliable and production-ready for project documentation.

---

### 6. Children's Storybook
**Theme**: Whimsical, colorful, playful

**Features to Test**:
- Large, readable fonts
- Colorful, playful design
- Illustration placeholders
- Page-per-spread layout
- Whimsical borders
- Story progression
- Simple, clear typography

**Edge Cases**:
- Large font sizes
- Color usage
- Simple layouts
- Page breaks for story flow
- Decorative elements

**Template**: `storybook.py`

---

### 7. Newspaper Front Page
**Theme**: Classic newspaper layout

**Features to Test**:
- Multi-column layout
- Banner headline
- Subheadlines
- Bylines
- Photo placeholders with captions
- Pull quotes
- Classic newspaper aesthetic
- Date/edition info

**Edge Cases**:
- Multi-column text flow
- Headline sizing
- Photo placement
- Column balancing
- Newspaper-style typography

**Template**: `newspaper.py`

---

## Implementation Plan

### Phase 1: Template Creation (7 templates)
1. Create each template file in `src/waft/templates/`
2. Follow pattern from `simple_scientific.py`
3. Each template should have:
   - HTML/CSS template string
   - Generation function
   - Example usage in `if __name__ == "__main__"`

### Phase 2: Example Generation
1. Create `examples/generate_all_document_types.py`
2. Generate one example of each document type
3. Save to `_work_efforts/document_examples/`
4. Open all PDFs for review

### Phase 3: Documentation
1. Create `docs/DOCUMENT_GENERATORS_GUIDE.md`
2. Document each template:
   - Purpose and use cases
   - Features and capabilities
   - Parameters and options
   - Example usage
   - Edge cases handled
3. Create quick reference guide

### Phase 4: Tooling & Organization
1. Create `tools/document_generators/` folder
2. Include:
   - `README.md` - Overview and quick start
   - `template_reference.md` - All templates reference
   - `example_generator.py` - Script to generate all examples
   - `template_tester.py` - Test edge cases
   - `usage_examples.md` - Code examples for each template

### Phase 5: Testing & Validation
1. Generate all 7 document types
2. Open each PDF for visual review
3. Test edge cases
4. Verify robustness
5. Document any issues found

---

## Folder Structure

```
_work_efforts/document_generators/
├── README.md                    # Main documentation
├── examples/                    # Generated example PDFs
│   ├── eldritch_journal.pdf
│   ├── screenplay.pdf
│   ├── heartfelt_letter.pdf
│   ├── invoice_contract.pdf
│   ├── code_documentation.pdf
│   ├── storybook.pdf
│   └── newspaper.pdf
├── tools/                       # Helper tools
│   ├── generate_all.py         # Generate all examples
│   ├── template_tester.py      # Test edge cases
│   └── usage_examples.md       # Code examples
└── docs/                        # Documentation
    ├── template_reference.md   # All templates reference
    └── guide.md                # User guide
```

---

## Success Criteria

**Templates Created**:
- ✅ 7 template files in `src/waft/templates/`
- ✅ Each follows established pattern
- ✅ Each has example usage

**Examples Generated**:
- ✅ 7 example PDFs created
- ✅ All PDFs open successfully
- ✅ Each demonstrates template capabilities

**Documentation**:
- ✅ Complete guide for all templates
- ✅ Quick reference available
- ✅ Usage examples provided

**Tooling**:
- ✅ Generator script for all examples
- ✅ Testing tools for edge cases
- ✅ Helpful utilities in tools folder

**Quality**:
- ✅ All templates work correctly
- ✅ Edge cases handled
- ✅ Robust and reliable
- ✅ Code documentation template is production-ready

---

## Timeline Estimate

- **Template Creation**: 2-3 hours (7 templates)
- **Example Generation**: 1 hour (7 examples)
- **Documentation**: 1-2 hours (comprehensive docs)
- **Tooling**: 1 hour (helper scripts)
- **Testing**: 1 hour (edge cases, validation)

**Total**: ~6-8 hours of focused work

---

## Risks & Considerations

**Risks**:
- Some templates may be complex (screenplay, newspaper)
- Edge cases might reveal WeasyPrint limitations
- Code documentation must be production-ready (high stakes)

**Mitigation**:
- Start with simpler templates
- Test edge cases early
- Focus extra attention on code documentation
- Iterate based on results

---

**Plan Status**: Ready for critique and consideration
