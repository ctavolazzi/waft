# WAFT Docs

**Complete document generation workflow: field guides, booklets, printer-friendly versions, session summaries, and redaction tools.**

Orchestrates the entire WAFT document generation process including field guides at three complexity levels (layman, professional, scientist), printer-friendly versions, complete booklets with binder system, session summaries, and PDF redaction capabilities.

**Use when:** Need to generate WAFT documentation, field guides, booklets, printer-friendly documents, session summaries, or redact PDFs.

---

## Purpose

This command provides:
- **Field Guide Generation**: Three-level field guides (layman, professional, scientist)
- **Printer-Friendly Conversion**: Black-and-white, minimal-ink versions
- **Booklet Assembly**: Complete booklets using binder system
- **Session Summaries**: Comprehensive PDF summaries of chat sessions
- **PDF Redaction**: Storytelling tool for redacting information
- **Unified Workflow**: Single command for all document generation needs

---

## Quick Start

### Generate Complete Field Guide Booklet
```
/waft-docs field-guide
```

Generates all three field guide levels and combines into complete booklet.

### Generate Printer-Friendly Version
```
/waft-docs field-guide --printer-friendly
```

Generates printer-friendly (black-and-white) versions of all field guides.

### Generate Session Summary
```
/waft-docs session-summary
```

Creates comprehensive PDF summary of current chat session.

### Redact PDF
```
/waft-docs redact --input path/to/file.pdf --areas "100,200,300,400"
```

Redacts specified areas in a PDF (for storytelling/classified documents).

---

## Workflow Sequence

### Phase 1: Field Guide Generation

**Execute**: Generate field guides at three complexity levels

**Purpose**: Create comprehensive WAFT documentation for different audiences

**Steps**:
1. Generate Level 1: Layman's Guide (simple explanations)
2. Generate Level 2: Professional Guide (technical details)
3. Generate Level 3: ML AI Scientist Guide (research methodology)
4. Optionally generate printer-friendly versions

**Output**:
- `WAFT_Field_Guide_Layman.pdf`
- `WAFT_Field_Guide_Professional.pdf`
- `WAFT_Field_Guide_Scientist.pdf`
- Printer-friendly versions (if requested)

**Location**: `_work_efforts/showcase_documents/`

---

### Phase 2: Booklet Assembly

**Execute**: Combine field guides into complete booklet

**Purpose**: Create unified document collection with binder system

**Steps**:
1. Generate individual field guide PDFs (if not already done)
2. Create binder with title and metadata
3. Add sections for each level
4. Add documents to sections
5. Generate complete booklet with dividers

**Output**:
- `WAFT_Field_Guide_Complete_Booklet.pdf`
- Includes cover, TOC, section dividers, and all three guides

**Location**: `_work_efforts/showcase_documents/`

---

### Phase 3: Printer-Friendly Conversion

**Execute**: Convert documents to black-and-white, minimal-ink format

**Purpose**: Create cost-effective printing versions

**Features**:
- White backgrounds only (#fff)
- Gray borders instead of black (#666, #ccc)
- Light gray table headers (#f5f5f5)
- Thick black borders only for important warnings
- Optimized for cost-effective printing

**Output**:
- Printer-friendly versions of all generated documents
- Same content, optimized styling

---

### Phase 4: Session Summary Generation

**Execute**: Generate comprehensive session summary PDF

**Purpose**: Document important information from chat session

**Content Includes**:
- Session goals and objectives
- Changes made (printer-friendly updates, framework design)
- Architecture decisions (DocumentBuilder, composable units)
- Tools created (redactor, helpers)
- Verification results
- Next steps

**Output**:
- `SESSION_SUMMARY_YYYY-MM-DD.pdf`
- Printer-friendly format with lighter borders

**Location**: `_work_efforts/showcase_documents/`

---

### Phase 5: PDF Redaction

**Execute**: Redact information from PDFs

**Purpose**: Create classified documents, mystery stories, redacted reports

**Features**:
- Manual area redaction (x, y, width, height)
- Text redaction (future: automatic text detection)
- Black rectangular overlays
- Preserves original PDF structure

**Output**:
- Redacted PDF with black rectangles over specified areas

---

## Command Options

### Field Guide Generation

**Standard (Color Version)**:
```
/waft-docs field-guide
```

**Printer-Friendly Version**:
```
/waft-docs field-guide --printer-friendly
```

**Individual Level**:
```
/waft-docs field-guide --level layman
/waft-docs field-guide --level professional
/waft-docs field-guide --level scientist
```

### Booklet Generation

**Complete Booklet**:
```
/waft-docs booklet
```

**Printer-Friendly Booklet**:
```
/waft-docs booklet --printer-friendly
```

### Session Summary

**Generate Summary**:
```
/waft-docs session-summary
```

**Custom Summary**:
```
/waft-docs session-summary --title "Custom Title" --focus "specific topic"
```

### PDF Redaction

**Redact Areas**:
```
/waft-docs redact --input file.pdf --areas "x1,y1,w1,h1" "x2,y2,w2,h2"
```

**Redact with Labels**:
```
/waft-docs redact --input file.pdf --areas "100,200,300,400:classified" "500,600,200,100:secret"
```

---

## Complete Execution Sequence

### Standard Workflow
```
1. /waft-docs field-guide          → Generate all three field guides
2. /waft-docs booklet              → Assemble complete booklet
3. /waft-docs field-guide --printer-friendly  → Generate printer-friendly versions
4. /waft-docs booklet --printer-friendly      → Assemble printer-friendly booklet
```

### Quick Workflow
```
/waft-docs all
```

Generates everything: field guides, booklets, printer-friendly versions.

### Session Documentation
```
/waft-docs session-summary
```

Generates comprehensive session summary PDF.

---

## Implementation Details

### Command Execution

The command can be executed in two ways:

1. **Via Cursor Command** (Recommended):
   ```
   /waft-docs field-guide
   ```
   The AI assistant will execute the appropriate Python scripts.

2. **Via Command Line Script**:
   ```bash
   python scripts/generate_waft_docs.py field-guide
   python scripts/generate_waft_docs.py field-guide --printer-friendly
   python scripts/generate_waft_docs.py booklet
   python scripts/generate_waft_docs.py session-summary
   python scripts/generate_waft_docs.py redact --input file.pdf --areas "100,200,300,400"
   python scripts/generate_waft_docs.py all
   ```

### Scripts Used

1. **Main CLI Script**:
   - `scripts/generate_waft_docs.py` - Unified command-line interface

2. **Field Guide Generation**:
   - `examples/generate_waft_field_guide.py` - Standard color version
   - `examples/generate_waft_field_guide_printer_friendly.py` - Printer-friendly version

3. **Booklet Assembly**:
   - Uses `src/waft/binder.py` - Binder system for combining PDFs
   - Creates sections, dividers, TOC automatically

4. **Session Summary**:
   - `examples/generate_session_summary.py` - Session summary generator
   - Uses printer-friendly template with lighter borders

5. **PDF Redaction**:
   - `src/waft/pdf_redactor.py` - PDFRedactor class
   - `examples/demo_redactor_simple.py` - Demo script

### Template System

- **Field Guide Template**: `src/waft/templates/field_guide.py`
- **Printer-Friendly Template**: Inline in `generate_waft_field_guide_printer_friendly.py`
- **Styling**: CSS-based, optimized for WeasyPrint rendering

### Output Directory

All generated documents are saved to:
```
_work_efforts/showcase_documents/
```

---

## Usage Examples

### Example 1: Generate Complete Documentation Set
```
/waft-docs all
```

**What it does**:
1. Generates all three field guide levels (color)
2. Generates printer-friendly versions
3. Assembles complete booklet (color)
4. Assembles printer-friendly booklet
5. Outputs all files to showcase_documents/

**Output**:
- 6 individual PDFs (3 color + 3 printer-friendly)
- 2 complete booklets (color + printer-friendly)

### Example 2: Quick Field Guide Only
```
/waft-docs field-guide --level professional
```

**What it does**:
- Generates only the professional-level field guide
- Color version by default

**Output**:
- `WAFT_Field_Guide_Professional.pdf`

### Example 3: Printer-Friendly Booklet
```
/waft-docs booklet --printer-friendly
```

**What it does**:
- Generates printer-friendly versions of all three guides
- Assembles into complete printer-friendly booklet

**Output**:
- `WAFT_Field_Guide_Complete_Booklet_PrinterFriendly.pdf`

### Example 4: Session Summary
```
/waft-docs session-summary
```

**What it does**:
- Analyzes current chat session
- Generates comprehensive PDF summary
- Uses printer-friendly template

**Output**:
- `SESSION_SUMMARY_YYYY-MM-DD.pdf`

### Example 5: Redact PDF
```
/waft-docs redact --input _work_efforts/showcase_documents/SESSION_SUMMARY_2026-01-11.pdf --areas "100,200,300,400" "500,600,200,100"
```

**What it does**:
- Loads specified PDF
- Adds black rectangles at specified coordinates
- Saves redacted version

**Output**:
- `SESSION_SUMMARY_2026-01-11_redacted.pdf`

---

## Integration with Other Commands

This command can be combined with:
- `/checkpoint` - Document generation checkpoint
- `/recap` - Session recap before generating summary
- `/verify` - Verify generated documents
- `/reflect` - Reflect on document generation process

---

## When to Use

**Use `/waft-docs` when**:
- ✅ Need to generate WAFT field guides
- ✅ Want to create complete documentation booklets
- ✅ Need printer-friendly versions
- ✅ Want to document a session
- ✅ Need to redact PDFs for storytelling
- ✅ Starting new documentation project
- ✅ Updating existing documentation

**Don't use `/waft-docs` when**:
- ❌ Just need a simple text document
- ❌ Don't need PDF output
- ❌ Working on non-WAFT documentation
- ❌ Need real-time document editing

---

## Output Summary

After completion, provides:
1. **Field Guides**: Three-level documentation (layman, professional, scientist)
2. **Complete Booklets**: Unified collections with binder system
3. **Printer-Friendly Versions**: Cost-effective black-and-white PDFs
4. **Session Summaries**: Comprehensive chat session documentation
5. **Redacted PDFs**: Storytelling/classified document versions

---

## Best Practices

1. **Generate Regularly**: Keep documentation up-to-date
2. **Use Printer-Friendly**: For cost-effective printing
3. **Session Summaries**: Document important sessions
4. **Version Control**: Commit generated PDFs to git
5. **Test Generation**: Verify PDFs open correctly
6. **Redact Carefully**: Double-check coordinates before redaction

---

## Troubleshooting

### Issue: Template Generation Fails
**Cause**: Missing WeasyPrint dependencies
**Solution**: Run `uv sync` to install dependencies

### Issue: Binder Merge Errors
**Cause**: Corrupted PDF files
**Solution**: Regenerate source PDFs

### Issue: Printer-Friendly Not Working
**Cause**: Template not using printer-friendly helper
**Solution**: Use `--printer-friendly` flag explicitly

### Issue: Redaction Coordinates Wrong
**Cause**: PDF coordinate system (bottom-left origin)
**Solution**: Verify coordinates match PDF page size

---

## Technical Details

### DocumentBuilder Framework

The command uses the unified `DocumentBuilder` framework:
- **Location**: `src/waft/document_builder.py`
- **Features**: Fluent API, composable units, automatic printer-friendly conversion
- **Usage**: `DocumentBuilder.field_guide(...).generate()`

### Binder System

Booklet assembly uses the binder system:
- **Location**: `src/waft/binder.py`
- **Features**: Sections, dividers, TOC, metadata
- **Usage**: `Binder(...).add_section(...).generate(...)`

### PDF Redactor

Redaction uses the PDFRedactor class:
- **Location**: `src/waft/pdf_redactor.py`
- **Features**: Area redaction, text redaction (future), overlay merging
- **Usage**: `PDFRedactor(pdf_path).add_area_redaction(...).save(...)`

---

## Time Estimates

- **Field Guide (Single)**: ~5-10 seconds
- **Field Guide (All Three)**: ~15-30 seconds
- **Booklet Assembly**: ~10-20 seconds
- **Printer-Friendly Conversion**: ~5-10 seconds per document
- **Session Summary**: ~10-15 seconds
- **PDF Redaction**: ~2-5 seconds

**Total (Complete Set)**: ~1-2 minutes

---

## Error Handling

If any phase fails:
- Document the failure
- Continue with remaining phases if possible
- Note what was skipped
- Provide summary of what completed vs. what failed
- Suggest remediation steps

---

**This command provides a complete workflow for generating all WAFT documentation - from field guides to session summaries to redacted PDFs - all in one unified command.**

---

End Command ---
