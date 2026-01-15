---
name: WAFT Orientation Guide Creation
overview: Create a comprehensive multi-level orientation guide to WAFT using DocumentBuilder, generating both PDF and Markdown versions for different audiences (Layman, Professional, Scientist).
todos:
  - id: create_script
    content: Create examples/generate_waft_orientation_guide.py following the pattern from generate_waft_field_guide.py
    status: pending
  - id: extract_content
    content: Extract and organize content from README.md, AI_ORIENTATION_RECAP.md, and other source documents
    status: pending
  - id: write_layman
    content: Write Level 1 (Layman) content with simple explanations and analogies
    status: pending
  - id: write_professional
    content: Write Level 2 (Professional) content with technical details for developers
    status: pending
  - id: write_scientist
    content: Write Level 3 (Scientist) content with research-level depth
    status: pending
  - id: generate_pdfs
    content: Generate PDF versions using DocumentBuilder.field_guide() and collection()
    status: pending
  - id: generate_markdown
    content: Generate Markdown versions for each level and combined version
    status: pending
  - id: test_output
    content: Test generated PDFs and Markdown files for quality and completeness
    status: pending
---

# WAFT Orientation Guide Creation Plan

## Overview

Create a comprehensive orientation guide to WAFT that serves multiple audiences through a multi-level approach, similar to the existing field guide example. The guide will be generated using DocumentBuilder and available as both PDF and Markdown formats.

## Tools Available

1. **DocumentBuilder** (`src/waft/document_builder.py`)
   - `field_guide()` template - Perfect for orientation materials
   - `collection()` - For combining multiple documents into a booklet
   - Printer-friendly option available
   - Page count constraints for optimization

2. **Existing Examples**
   - `examples/generate_waft_field_guide.py` - Multi-level field guide pattern
   - `_work_efforts/AI_ORIENTATION_RECAP.md` - Existing orientation content
   - `README.md` - Project overview
   - `docs/STUDY_GYM_GUIDE.md` - Tool documentation
   - `docs/DOCUMENT_BUILDER_EXPLAINED.md` - DocumentBuilder usage

3. **Source Material**
   - README.md - Core concepts and quick start
   - AI_ORIENTATION_RECAP.md - Comprehensive AI system orientation
   - DOCUMENT_BUILDER_EXPLAINED.md - Document generation tools
   - STUDY_GYM_GUIDE.md - Learning system
   - Various work effort documents

## Implementation Plan

### Step 1: Create Generation Script

**File**: `examples/generate_waft_orientation_guide.py`

**Structure**:
- Follow pattern from `generate_waft_field_guide.py`
- Three functions for three audience levels:
  - `generate_level_1_layman()` - Simple explanations
  - `generate_level_2_professional()` - Technical details for developers
  - `generate_level_3_scientist()` - Research-level depth
- Main function that:
  - Generates all three levels as PDFs
  - Combines into a booklet using `DocumentBuilder.collection()`
  - Also generates Markdown versions
  - Saves to `_work_efforts/showcase_documents/`

### Step 2: Content Structure

**Level 1: Layman (Simple Explanations)**
- What is WAFT? (simple analogy)
- Why does it matter?
- Quick start guide
- Core concepts explained simply
- Equipment checklist
- Common use cases

**Level 2: Professional (Developer Focus)**
- Architecture overview
- Installation and setup
- Core components explained
- CLI commands reference
- Project structure
- Development workflow
- Integration patterns
- Best practices

**Level 3: Scientist (Research Depth)**
- Scientific mission and goals
- Three pillars (Substrate, Physics, Flight Recorder)
- Evolutionary architecture
- Agent lifecycle and OODA cycle
- Fitness functions and selection
- Lineage tracking and phylogenetic trees
- Experimental methodology
- Research applications

### Step 3: Content Sources

**From README.md**:
- Core pillars explanation
- Quick start commands
- Installation instructions
- Project structure
- Philosophy and mission

**From AI_ORIENTATION_RECAP.md**:
- Detailed architecture
- Component descriptions
- Code patterns
- File locations
- Common tasks
- Experiment structure

**From DOCUMENT_BUILDER_EXPLAINED.md**:
- DocumentBuilder usage
- Template system
- PDF generation workflow

**From STUDY_GYM_GUIDE.md**:
- Scientific method workflow
- Learning system explanation

**From docs/**:
- System overview
- Integration guides
- Vision documents

### Step 4: Document Generation

**PDF Generation**:
```python
# Level 1
doc1 = DocumentBuilder.field_guide(
    title="WAFT Orientation Guide: Layman's Level",
    content=layman_content,
    series="ORIENTATION",
    number="ORG-001",
    printer_friendly=True
)

# Level 2
doc2 = DocumentBuilder.field_guide(
    title="WAFT Orientation Guide: Professional Level",
    content=professional_content,
    series="ORIENTATION",
    number="ORG-002",
    printer_friendly=True
)

# Level 3
doc3 = DocumentBuilder.field_guide(
    title="WAFT Orientation Guide: Scientist Level",
    content=scientist_content,
    series="ORIENTATION",
    number="ORG-003",
    printer_friendly=True
)

# Combine into booklet
collection = DocumentBuilder.collection("WAFT Orientation Guide")
collection.add(doc1)
collection.add(doc2)
collection.add(doc3)
collection.save("WAFT_Orientation_Guide_Complete.pdf")
```

**Markdown Generation**:
- Generate separate `.md` files for each level
- Include frontmatter with metadata
- Save to `docs/orientation/` directory
- Also create combined version

### Step 5: Output Structure

**PDFs**:
- `_work_efforts/showcase_documents/WAFT_Orientation_Guide_Layman.pdf`
- `_work_efforts/showcase_documents/WAFT_Orientation_Guide_Professional.pdf`
- `_work_efforts/showcase_documents/WAFT_Orientation_Guide_Scientist.pdf`
- `_work_efforts/showcase_documents/WAFT_Orientation_Guide_Complete.pdf` (booklet)
- `_work_efforts/showcase_documents/WAFT_Orientation_Guide_Complete_PrinterFriendly.pdf`

**Markdown**:
- `docs/orientation/WAFT_Orientation_Guide_Layman.md`
- `docs/orientation/WAFT_Orientation_Guide_Professional.md`
- `docs/orientation/WAFT_Orientation_Guide_Scientist.md`
- `docs/orientation/WAFT_Orientation_Guide_Complete.md` (combined)

### Step 6: Content Organization

Each level should include:

1. **Introduction** - What this level covers
2. **What is WAFT?** - Appropriate depth for audience
3. **Core Concepts** - Explained at appropriate level
4. **Getting Started** - Installation and first steps
5. **Key Components** - Architecture overview
6. **Common Tasks** - Practical examples
7. **Next Steps** - Where to go from here
8. **References** - Links to deeper documentation

### Step 7: HTML Content Formatting

Use DocumentBuilder's HTML content format:
- `<h2>`, `<h3>` for headings
- `<p>` for paragraphs
- `<ul>`, `<li>` for lists
- `<div class="note">` for notes
- `<div class="warning">` for warnings
- `<div class="caution">` for cautions
- `<code>` for code snippets
- `<div class="procedure">` for step-by-step instructions

### Step 8: Integration with Existing Systems

- Reference existing documentation
- Link to work efforts where relevant
- Point to examples directory
- Reference Study Gym for learning
- Include DocumentBuilder usage examples

## Files to Create/Modify

**New Files**:
1. `examples/generate_waft_orientation_guide.py` - Main generation script
2. `docs/orientation/WAFT_Orientation_Guide_Layman.md` - Markdown version
3. `docs/orientation/WAFT_Orientation_Guide_Professional.md` - Markdown version
4. `docs/orientation/WAFT_Orientation_Guide_Scientist.md` - Markdown version
5. `docs/orientation/WAFT_Orientation_Guide_Complete.md` - Combined markdown

**Output Files** (generated):
- PDFs in `_work_efforts/showcase_documents/`
- Markdown files in `docs/orientation/`

## Success Criteria

1. ✅ Three distinct levels of content (Layman, Professional, Scientist)
2. ✅ Both PDF and Markdown formats available
3. ✅ Combined PDF booklet with binder
4. ✅ Printer-friendly PDF option
5. ✅ Comprehensive coverage of WAFT concepts
6. ✅ Clear progression from simple to advanced
7. ✅ Practical examples and use cases
8. ✅ References to deeper documentation
9. ✅ Professional formatting and structure
10. ✅ Reusable generation script

## Next Steps After Plan Approval

1. Create the generation script following the pattern
2. Extract and organize content from source materials
3. Write content for each level
4. Generate PDFs using DocumentBuilder
5. Generate Markdown versions
6. Test output quality
7. Update documentation index if needed