---
name: PROJECT LIGHTCONE Binder Generation
overview: Create a complete binder of corporate horror documents for "PROJECT LIGHTCONE MASTER FILE" using the existing DocumentEngine system. Generate both PDF outputs and markdown source files, organized by tabs (Tab 1 → Tab 5).
todos:
  - id: sync_repository
    content: Pull latest main (includes merged PR
    status: pending
  - id: create_work_effort
    content: Create work effort for PROJECT LIGHTCONE binder generation
    status: pending
  - id: create_generation_module
    content: Create src/waft/generate_lightcone_docs.py with document generation functions
    status: pending
  - id: tab1_documents
    content: "Generate Tab 1 documents: Light Cone Topology description, The God Problem memo"
    status: pending
  - id: tab2_documents
    content: "Generate Tab 2 documents: Lazarus Protocol, Suspension-9 MSDS, Fulgurite Core schematic, Scream Filter log"
    status: pending
  - id: tab3_documents
    content: "Generate Tab 3 documents: Memetic Saturation Report, Greys Field Guide"
    status: pending
  - id: tab4_documents
    content: "Generate Tab 4 documents: Phase Burn Chart, Reality Check Form, Subject K Dossier"
    status: pending
  - id: tab5_documents
    content: "Generate Tab 5 documents: Protocol SILENT NIGHT, Protocol JUDGMENT DAY"
    status: pending
  - id: create_binder_index
    content: Create binder index/README.md with table of contents and document organization
    status: pending
---

# PROJECT LIGHTCONE Master File Binder Generation Plan

## Overview

Generate a complete binder of documents following the "1990s industrial xerox chic" aesthetic for the PROJECT LIGHTCONE MASTER FILE. Documents will be created using the existing `DocumentEngine` system in `src/waft/foundation.py`, producing both PDF outputs and markdown source files for manual formatting.

## Existing Infrastructure

- **DocumentEngine**: Located in `src/waft/foundation.py` with block-based API
- **Content Blocks Available**: `SectionHeader`, `TextBlock`, `KeyValueBlock`, `LogBlock`, `WarningBlock`, `SignatureBlock`
- **Config Presets**: `classified_dossier()`, `scientific_log()`, `legal_audit()`
- **Example**: `src/waft/generate_artifacts.py` shows usage patterns
- **Inspiration File**: `TM-ARCH-009-SOURCE-EYES-ONLY.pdf` - Primary style reference document (Cosmological Architecture of the Human Organism)

## Style Reference & Emulation Guidelines

### Inspiration Document Analysis

**Reference**: `TM-ARCH-009-SOURCE-EYES-ONLY.pdf` (Cosmological Architecture)

**Key Style Elements to Emulate**:

- **Header Structure**: "FIELD MANUAL" prominently displayed, document ID (TM.00C-ARCH-009 v2.1), organization name "TELEPORT MASSIVE"
- **Visual Elements**: Human figure diagrams with energy signatures, translocation vectors, vortex graphics
- **Security Classifications**: "TOP SECRET // ORACLE EYES ONLY" black box stamp, "WARNING: COGNITOHAZARD" warning bar
- **Typography**: Bold sans-serif headers, standard sans-serif body text, distressed/xeroxed quality for security stamps
- **Layout**: Dark grey border with inner dotted line, watermark logo pattern, grayscale color scheme
- **Aesthetic**: 1990s industrial xerox chic, corporate horror, utilitarian but worn appearance

### Content Variation Strategy

**While maintaining style consistency, each document must vary**:

1. **Composition**: Different layouts (two-column for MSDS, single-column for protocols, forms vs. reports)
2. **Severity**: Varying threat levels (from "INTERNAL USE" to "TOP SECRET" to "TACTICAL NUCLEAR STERILIZATION")
3. **Context**: Different departments (Engineering, Medical, Environmental, Emergency Response)
4. **Findings**: Unique evidence per document (technical data, medical symptoms, environmental readings, containment failures)
5. **Evidence Type**: Varying formats (charts, logs, forms, schematics, field guides, protocols)

**Style Consistency Checklist** (apply to all documents):

- [ ] TELEPORT MASSIVE header/logo
- [ ] Document ID format (TM-XXX-###)
- [ ] Security classification stamps
- [ ] Warning blocks for hazards
- [ ] Grayscale aesthetic
- [ ] Corporate bureaucratic tone
- [ ] Distressed/xeroxed quality indicators
- [ ] Border and watermark patterns

## Document Structure

### Tab 1: Doctrine & Theory (The "Bible")

**Status**: One document exists (TM-ARCH-009: Cosmological Architecture)

**To Create**:

1. **TM-VIS-001: Light Cone Topology Diagram** (fold-out visual aid)

   - Note: Diagram will be described in markdown; visual created in design software
   - Content: Human stick figure with "Cone of Reality" projection
   - Labels: "Event Horizon," "Chaos Gradient," "The Dark (Xenos Habitat)"
   - Hand-drawn red circles around "blind spots"

2. **TM-MEMO-042: "The God Problem"**

   - Format: Internal memo/risk assessment
   - Content: Philosophical discussion on why we cannot "ask" the Sleeper for help
   - Risk: Total ego death for entire species

### Tab 2: Engineering & Hardware (The "Meat Grinder")

**To Create**:

1. **TM-ENG-114: The Lazarus Protocol (Ignition Sequence)**

   - Format: Technical manual (similar to existing dossier style)
   - Content: "Artificial Soul/Lightning" document (already drafted per user)

2. **TM-ENG-004: Material Safety Data Sheet - Suspension-9**

   - Format: MSDS sheet (content provided in user's example)
   - Content: Hyper-Refined Schreibersite safety data
   - Visual: NFPA 704 Fire Diamond (Blue 3, Red 4, Yellow 4, White W)
   - Note: Handwritten annotations to be added in design software

3. **TM-ENG-205: Schematic - The Fulgurite Core (Type-IV)**

   - Format: Technical blueprint
   - Content: Description of "CPU" (glass jar with preserved organ, capacitor bank)
   - Note: Visual schematic created in design software; text description in markdown

4. **TM-MAINT-088: Maintenance Log - "The Scream Filter"**

   - Format: Checklist/log document
   - Content: Acoustic dampener replacement procedures
   - Technician note: "Filters clogged again. Sounded like a thousand people crying in a tunnel."

### Tab 3: Environmental & Fallout (The "Pollution")

**To Create**:

1. **TM-ENV-202: Memetic Saturation Report ("Psychic Ash")**

   - Format: Environmental report with map
   - Content: Industrial buildup of "dead soul residue" in atmosphere
   - Map: Weather map of USA showing "High Pressure Depression Fronts"
   - Warning: "Rain in Sector 7 has tested positive for 'Melancholy.'"

2. **TM-FIELD-156: Field Guide - Identifying "Greys" (Ash-Entities)**

   - Format: Field identification guide
   - Content: Grainy photos (described), shadow people in fog
   - Instruction: "Do not acknowledge them. If you look at them, you give them mass."

### Tab 4: Personnel & Medical (The "Human Cost")

**To Create**:

1. **TM-MED-301: Chart - The Phase Burn Spectrum**

   - Format: Medical progression chart
   - Content: Stages from "Déjà vu" to "Full Temporal Dissociation"
   - Stage 4 Symptoms: "Subject claims to remember the future," "Subject attempts to walk through solid walls"

2. **TM-FORM-88B: "Reality Check" Self-Assessment**

   - Format: Mandatory daily quiz form
   - Questions: "Is the President the same person as yesterday?", "Do you recognize your hands?", "Have you heard the static speak your name?"

3. **TM-DOSSIER-K: Subject K (The Nephilim)**

   - Format: Personnel dossier with photos/interviews
   - Content: Phaseburner containment failure
   - Status: "Subject simply walked out of the cell. Claims he 'chose the timeline where the door was open.'"

### Tab 5: Emergency Protocols (The "Oh Sh*t" Plans)

**To Create**:

1. **TM-PROTO-001: Protocol SILENT NIGHT**

   - Format: Emergency procedure document
   - Content: Response to "Light Cone" flicker (Humanity waking/dying)
   - Steps: Broadcast "Lullaby" frequencies, deploy amnestic aerosols

2. **TM-PROTO-002: Protocol JUDGMENT DAY**

   - Format: Emergency procedure document
   - Content: Response to Fulgurite Core becoming localized deity
   - Action: "Tactical Nuclear Sterilization of the facility"

## Implementation Strategy

### Phase 0: Repository Synchronization & Style Analysis

**Before any work begins**:

1. **Repository Sync**:

   - Fetch latest changes from remote: `git fetch origin`
   - **Checkout working branch**: `git checkout claude/cursor-plan-epI5z`
   - Pull latest changes: `git pull origin claude/cursor-plan-epI5z`
   - **Note**: Working simultaneously with Cursor on same branch - coordinate commits carefully
   - Verify clean working state: `git status` should show minimal uncommitted changes

2. **Existing Infrastructure Review**:

   - Review `src/waft/scripts/mint_genesis.py` - Genesis artifact generation (Kafka Protocol style)
   - Review `src/waft/reports/scientific_report.py` - Clinical Standard report generator
   - Review `src/waft/foundation.py` - DocumentEngine block-based API
   - Review `src/waft/generate_artifacts.py` - Existing artifact generation patterns
   - **Leverage existing code**: Build on `mint_genesis.py` and `scientific_report.py` patterns rather than starting from scratch

3. **Style Reference Analysis**:

   - Locate and review `TM-ARCH-009-SOURCE-EYES-ONLY.pdf` (inspiration document)
   - Compare with existing `_fracture/ARTIFACT_001_GENESIS.pdf` for style consistency
   - Document key visual elements: header structure, security stamps, typography, layout patterns
   - Extract style patterns: border styles, watermark placement, warning block formats
   - Note content structure: how information is organized, severity indicators, evidence presentation
   - Create style reference notes for consistent application across all generated documents

**Commands**:

```bash
git fetch origin
git checkout main
git pull origin main  # Includes merged PR #5 (cursor development plan)
git checkout -b claude/lightcone-binder-generation
git status  # Verify clean
# If conflicts: git stash, pull, then git stash pop
```

### Phase 1: Create Document Generation Module

**File**: `src/waft/generate_lightcone_docs.py`

**Build on Existing Infrastructure**:
- **Leverage**: `src/waft/scripts/mint_genesis.py` patterns (Kafka Protocol density, visual noise, bureaucratic style)
- **Leverage**: `src/waft/reports/scientific_report.py` patterns (Clinical Standard, clean headers, metadata rails)
- **Leverage**: `src/waft/foundation.py` DocumentEngine (block-based API, redaction, watermarks)
- **Extend**: Create new module that combines patterns from all three existing generators

**Structure**:

- **Style Helper Functions** (inspired by mint_genesis.py and scientific_report.py):
  - `create_teleport_massive_header()` - Standard header with logo, document ID, organization name
  - `create_security_stamp()` - TOP SECRET, ORACLE EYES ONLY, COGNITOHAZARD warnings (like mint_genesis.py barcode/checklist style)
  - `create_field_manual_config()` - DocumentConfig preset matching TM-ARCH-009 style
  - `apply_xerox_aesthetic()` - Instructions for distressed/worn appearance (markdown notes)
  - `draw_watermark_layer()` - Background watermark pattern (from mint_genesis.py)
  - `draw_system_check_rail()` - Left margin checklist column (from mint_genesis.py)

- **Document Generators**:
  - One function per document: `generate_tm_vis_001()`, `generate_tm_memo_042()`, etc.
  - Each function varies: composition, severity, context, findings, evidence type
  - All functions maintain: style consistency (header format, security stamps, typography)
  - **Use FPDF directly** (like mint_genesis.py) for complex layouts, **DocumentEngine** (like generate_artifacts.py) for simpler documents

- **Shared Helper Functions**:
  - MSDS formatting templates (two-column layout, NFPA diamond)
  - Protocol step formatting (numbered procedures)
  - Medical chart structures (progression stages, symptom lists)
  - Form field layouts (checkboxes, text fields)

- **Main Function**:
  - `generate_all_lightcone_docs()` - Calls all generators, organizes by tab
  - Output: Both PDF (via FPDF/DocumentEngine) and markdown source files

### Phase 2: Document-Specific Configurations

**MSDS Documents** (Suspension-9):

- Use `DocumentConfig` with two-column layout
- Font: Times New Roman or Arial Narrow (condensed)
- Add NFPA diamond description in markdown
- Include handwritten annotation placeholders

**Field Manuals** (existing style):

- Use `DocumentConfig.classified_dossier()`
- Header: "TELEPORT MASSIVE // FIELD MANUAL"
- Watermark: "TOP SECRET // ORACLE EYES ONLY"
- Font: Courier New, Arial Black headers

**Protocols**:

- Use `DocumentConfig.classified_dossier()`
- Numbered steps format
- Warning blocks for critical actions

**Medical Charts**:

- Use `KeyValueBlock` for progression stages
- `LogBlock` for symptom lists
- Clinical report aesthetic

### Phase 3: Content Generation (Tab by Tab)

**Tab 1 Implementation**:

1. Create `generate_light_cone_topology()` - markdown description of diagram
2. Create `generate_god_problem_memo()` - philosophical risk assessment

**Tab 2 Implementation**:

1. Create `generate_lazarus_protocol()` - technical manual
2. Create `generate_suspension9_msds()` - MSDS sheet (content from user example)
3. Create `generate_fulgurite_schematic()` - blueprint description
4. Create `generate_scream_filter_log()` - maintenance checklist

**Tab 3 Implementation**:

1. Create `generate_memetic_saturation_report()` - environmental report
2. Create `generate_greys_field_guide()` - identification guide

**Tab 4 Implementation**:

1. Create `generate_phase_burn_chart()` - medical progression chart
2. Create `generate_reality_check_form()` - daily assessment form
3. Create `generate_subject_k_dossier()` - personnel dossier

**Tab 5 Implementation**:

1. Create `generate_protocol_silent_night()` - emergency procedure
2. Create `generate_protocol_judgment_day()` - emergency procedure

### Phase 4: Output Organization

**Directory Structure**:

```
_work_efforts/lightcone_binder/
├── pdf/
│   ├── tab1_doctrine/
│   │   ├── TM-ARCH-009_Cosmological_Architecture.pdf (exists)
│   │   ├── TM-VIS-001_Light_Cone_Topology.pdf
│   │   └── TM-MEMO-042_The_God_Problem.pdf
│   ├── tab2_engineering/
│   │   ├── TM-ENG-114_Lazarus_Protocol.pdf
│   │   ├── TM-ENG-004_Suspension9_MSDS.pdf
│   │   ├── TM-ENG-205_Fulgurite_Core_Schematic.pdf
│   │   └── TM-MAINT-088_Scream_Filter_Log.pdf
│   ├── tab3_environmental/
│   ├── tab4_personnel/
│   └── tab5_emergency/
├── markdown/
│   ├── tab1_doctrine/
│   ├── tab2_engineering/
│   ├── tab3_environmental/
│   ├── tab4_personnel/
│   └── tab5_emergency/
└── README.md (binder index/table of contents)
```

## Visual Elements (Design Software Notes)

**Elements requiring manual design work**:

- Light Cone Topology diagram (fold-out)
- NFPA 704 Fire Diamond graphic
- Fulgurite Core schematic blueprint
- Weather map (Memetic Saturation Report)
- Grainy photos (Greys Field Guide)
- Phase Burn Spectrum chart visualization
- Coffee stains, handwritten notes, stamps ("REDACTED", "BURN AFTER READING")

**Markdown will include**:

- Detailed descriptions of visual elements
- Placement instructions
- Style notes (e.g., "Add red circles around blind spots")
- Typography specifications

## Aesthetic Guidelines (Applied in Code)

**Typography**:

- Headers: Arial Black (or Courier Bold)
- Body: Courier New (or Times New Roman for MSDS)
- Monospace: Courier for logs/technical data

**Layout**:

- Two-column for MSDS sheets
- Single column for field manuals
- Margins: Standard (72pt) with option for tighter (36pt) for forms

**Watermarks**:

- "TOP SECRET // ORACLE EYES ONLY"
- "INTERNAL USE ONLY"
- "BURN AFTER READING"
- "DRAFT"

**Redaction**:

- Use `AutoRedactor` for sensitive terms
- Black bars for classified sections

## Technical Implementation Details

### DocumentEngine Extensions Needed

- **Two-column layout**: May need custom block or manual positioning for MSDS
- **Form fields**: For "Reality Check" form (checkboxes, text fields)
- **Chart/table blocks**: For Phase Burn Spectrum (may use `KeyValueBlock` creatively)

### Content Sources

- **Inspiration Document**: `TM-ARCH-009-SOURCE-EYES-ONLY.pdf` - Primary style reference (study before generating)
- **User-provided MSDS content** (Suspension-9) - use as-is, but vary presentation
- **User-provided structure breakdown** - expand into full documents with unique content
- **Existing "Cosmological Architecture" document** - reference for style consistency, but create distinct compositions

### Style Emulation Requirements

**For each document, ensure**:

1. **Header matches TM-ARCH-009 format**: "FIELD MANUAL" / "MSDS" / "PROTOCOL" etc., document ID, TELEPORT MASSIVE branding
2. **Security classifications vary**: Some "INTERNAL USE", some "TOP SECRET", some "ORACLE EYES ONLY"
3. **Visual elements differ**: Each document has unique diagrams/charts/forms appropriate to its type
4. **Content is unique**: Different findings, evidence, technical data, medical symptoms, environmental readings
5. **Severity levels vary**: From routine maintenance logs to tactical nuclear sterilization protocols
6. **Context shifts**: Engineering vs. Medical vs. Environmental vs. Emergency Response perspectives
7. **Aesthetic consistency**: All maintain grayscale, xeroxed, corporate horror aesthetic

## Execution Order

1. **Sync repository**: Checkout main, pull latest (includes merged PR #5), create new branch
   - **Note**: Working simultaneously with Cursor - coordinate commits to avoid conflicts
   - Stash any local changes if needed: `git stash`
   - Checkout main: `git checkout main`
   - Pull latest: `git pull origin main`
   - Create new branch: `git checkout -b claude/lightcone-binder-generation`

2. **Review existing infrastructure**: Study `mint_genesis.py`, `scientific_report.py`, `generate_artifacts.py`
   - Understand patterns: Kafka Protocol density, Clinical Standard style, DocumentEngine blocks
   - Identify reusable functions and style elements

3. **Create work effort** for tracking

4. **Create generation module** (`generate_lightcone_docs.py`)
   - Build on existing patterns from mint_genesis.py and scientific_report.py
   - Extend DocumentEngine for new document types

5. **Tab 1**: Generate remaining doctrine documents
6. **Tab 2**: Generate all engineering documents
7. **Tab 3**: Generate environmental documents
8. **Tab 4**: Generate personnel/medical documents
9. **Tab 5**: Generate emergency protocols
10. **Create binder index** (README.md with table of contents)

## Branch Coordination

**Claude Code Working Branch**: `claude/update-plan-merge-gFm6u` (already synced with main)

**AI Assistant Working Branch**: `claude/lightcone-binder-generation` (or coordinate with Claude Code's branch)

**Status**: Previous branch `claude/cursor-plan-epI5z` has been merged into main (PR #5)

**Coordination Strategy**:
- **Claude Code**: Working on `claude/update-plan-merge-gFm6u` - Document generation code, PDF outputs
- **AI Assistant**: Can work on same branch or coordinate file ownership
- **File Ownership**:
  - Claude Code: `src/waft/generate_lightcone_docs.py`, PDF generation functions
  - AI Assistant: Markdown source files, visual design notes, manual design elements
- **Communication**: Report progress after each tab completion
- **Before committing**: Always `git pull` to get latest changes
- **After committing**: Push immediately to coordinate branch
- **Merge strategy**: Both branches can merge independently when complete, or coordinate to work on same branch

## Answers to Claude Code's Questions

### 1. TM-ARCH-009 Location
**Answer**: The file `TM-ARCH-009-SOURCE-EYES-ONLY.pdf` is the inspiration document mentioned by the user. It should be:
- Referenced in the user's local files (may be in project root or `_fracture/` directory)
- Used as style reference for all generated documents
- If not found in repo, user will provide it or we'll work from the description provided

**Action**: Search for it, if not found, proceed with style analysis based on user's description and existing `_fracture/ARTIFACT_001_GENESIS.pdf` for reference.

### 2. Output Priority
**Answer**: Start with **Tab 1 documents first** (quick wins to establish pattern)
- This validates the generation framework with simpler documents
- Establishes style consistency early
- Provides immediate visual feedback

**Recommended Order**:
1. Create generation framework (`generate_lightcone_docs.py`)
2. Generate Tab 1 documents (Light Cone Topology, God Problem memo)
3. Review and refine style
4. Continue with remaining tabs

### 3. MSDS Content
**Answer**: The Suspension-9 MSDS content is **provided in the user's original message** (in the "EXAMPLES BEGIN" section). The full MSDS text is included there with all sections. Use that content as-is, but vary the presentation/composition per the style variation strategy.

**Location**: User's message contains the complete MSDS text starting with "MATERIAL SAFETY DATA SHEET (MSDS)" and includes all sections (1-7).

## Success Criteria

- All documents generated as PDFs using DocumentEngine/FPDF
- All documents have markdown source files
- Documents follow "1990s industrial xerox chic" aesthetic
- Visual element descriptions included for design software
- Binder index/table of contents created
- Documents organized by tab in directory structure
- Style consistency maintained across all documents (emulating TM-ARCH-009)
- Each document has unique composition, severity, context, findings, and evidence

## Final Coordination Summary

**Claude Code Status**: ✅ Starting Phase 0 execution
- **Branch**: `claude/update-plan-merge-gFm6u`
- **Focus**: Document generation code, PDF outputs
- **Starting with**: Framework creation → Tab 1 documents
- **Style Reference**: Using `_fracture/ARTIFACT_001_GENESIS.pdf` + user descriptions

**AI Assistant Status**: Ready to coordinate
- **Focus**: Markdown source files, visual design notes, manual design elements
- **Coordination**: Monitor progress, provide feedback, handle design elements

**Communication Protocol**:
- Claude Code reports after: Phase 0, Tab 1, each subsequent tab
- AI Assistant: Available for questions, design feedback, markdown formatting
- File conflicts: Unlikely (different file types)

**Plan Status**: ✅ FINALIZED - Ready for execution