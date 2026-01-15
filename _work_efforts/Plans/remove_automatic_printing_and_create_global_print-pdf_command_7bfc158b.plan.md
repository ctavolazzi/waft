---
name: Remove Automatic Printing and Create Global Print-PDF Command
overview: Remove all automatic printing from commands and create a new global "/print-PDF" command that intelligently finds or creates the most relevant PDF using WAFT evolution principles, Oracle insights, and context awareness.
todos:
  - id: audit_printing
    content: Audit all code for automatic printing and remove any remaining instances
    status: pending
  - id: create_pdf_discovery
    content: Create PDFDiscovery class for finding relevant PDFs based on context
    status: pending
  - id: create_pdf_evolution
    content: Create PDFEvolution class for generating evolved PDFs using WAFT principles
    status: pending
  - id: implement_print_command
    content: Implement /print-PDF command in main.py with Oracle integration
    status: pending
  - id: create_command_doc
    content: Create .cursor/commands/print-PDF.md documentation
    status: pending
  - id: update_existing_docs
    content: Update existing command docs to remove automatic printing references
    status: pending
  - id: test_scenarios
    content: "Test all scenarios: existing PDF, no PDF, low relevance, Oracle unavailable"
    status: pending
  - id: sync_global
    content: Sync command to global location for availability in all Cursor instances
    status: pending
---

# Remove Automatic Printing and Create Global Print-PDF Command

## Overview

Remove all automatic printing from existing commands and create a new global `/print-PDF` command that:

- Finds the most relevant PDF based on conversation context and active files
- Creates an evolved PDF using WAFT principles if none exists
- Uses Oracle for epistemic intelligence
- Prints the selected/created PDF

## Phase 1: Remove Automatic Printing

### 1.1 Audit All Printing Locations

**Files to check:**

- `src/waft/pdf.py` - Line 829: `subprocess.run(["lpr", ...])` in print method
- `src/waft/core/science_bitch.py` - Already shows print hints (no actual printing)
- `experiments/deep_tavern_science_experiment.py` - Already fixed (shows hint only)
- `experiments/tavern_science_experiment.py` - Already fixed (shows hint only)
- All command files in `.cursor/commands/` that mention `--print` flag

**Action:** Verify no automatic printing remains, remove any `subprocess.run(["lpr", ...])` calls that execute automatically.

### 1.2 Update PDF Class Print Method

**File:** `src/waft/pdf.py`

**Change:** The `print()` method should only print when explicitly called, not automatically. Ensure it's opt-in only.

**Current state (line 829):**

```python
subprocess.run(["lpr", str(self._generated_path)])
```

**Action:** Verify this is only called explicitly, not automatically during PDF generation.

### 1.3 Update Command Documentation

**Files:** All command `.md` files that mention `--print`

**Action:** Update documentation to clarify that printing is opt-in via `/print-PDF` command, not automatic.

## Phase 2: Create Global Print-PDF Command

### 2.1 Create Command File

**File:** `.cursor/commands/print-PDF.md`

**Structure:**

- Purpose: Intelligent PDF selection and printing
- Usage: `/print-PDF [options]`
- Options: `--force-create`, `--no-print` (preview only), `--style <style>`

### 2.2 Implement PDF Discovery System

**New file:** `src/waft/core/pdf_discovery.py`

**Class:** `PDFDiscovery`

**Methods:**

- `find_relevant_pdf(context: Dict) -> Optional[Path]`
  - Searches for PDFs in:
    - Current directory and subdirectories
    - `_work_efforts/` directories
    - `_pyrite/` directories
    - `_science/` directories
  - Scores PDFs based on:
    - Recency (modification time)
    - Context relevance (filename/content matches conversation)
    - Active work effort association
    - Oracle epistemic state relevance
  - Returns highest-scoring PDF

- `score_pdf(pdf_path: Path, context: Dict) -> float`
  - Calculates relevance score (0.0-1.0)
  - Factors:
    - Recency: `1.0 - (days_old / 30)` (max 30 days)
    - Context match: Filename/content keywords vs conversation
    - Work effort link: PDF in active work effort directory
    - Oracle relevance: Epistemic state alignment

### 2.3 Implement PDF Creation System

**New file:** `src/waft/core/pdf_evolution.py`

**Class:** `PDFEvolution`

**Methods:**

- `evolve_pdf(context: Dict, oracle: TheOracle) -> Path`
  - Uses WAFT evolution principles to decide what PDF to create
  - Consults Oracle for epistemic state
  - Analyzes conversation context
  - Generates appropriate PDF:
    - Conversation summary (if long conversation)
    - Project status report (if working on project)
    - Oracle insights document (if epistemic phase suggests it)
    - Work effort summary (if active work efforts)
    - Hybrid document (combines multiple sources)

- `_determine_pdf_type(context: Dict, oracle_state: Dict) -> str`
  - Returns: `"conversation_summary" | "project_status" | "oracle_insights" | "work_effort" | "hybrid"`
  - Uses Oracle epistemic phase to guide decision
  - Considers conversation length and content
  - Checks for active work efforts

- `_generate_evolved_content(pdf_type: str, context: Dict, oracle: TheOracle) -> str`
  - Generates markdown content based on type
  - Incorporates Oracle insights
  - Uses WAFT evolution principles for content structure
  - Includes "part within the whole" philosophy

### 2.4 Integrate with Main CLI

**File:** `src/waft/main.py`

**Add command:**

```python
@app.command()
def print_pdf(
    force_create: bool = typer.Option(False, "--force-create", help="Force creation of new PDF"),
    no_print: bool = typer.Option(False, "--no-print", help="Generate but don't print"),
    style: str = typer.Option("clinical_standard", "--style", help="PDF style"),
):
    """Print most relevant PDF or create evolved PDF using WAFT."""
    # Implementation
```

### 2.5 Command Implementation Logic

**Flow:**

1. Gather context (conversation, active files, work efforts)
2. Initialize Oracle (if Empirica available)
3. Try to find relevant PDF using `PDFDiscovery`
4. If found and relevant (score > 0.5):

   - Print it
   - Log to Oracle: "Printed relevant PDF: {path}"

5. If not found or score < 0.5:

   - Use `PDFEvolution` to create evolved PDF
   - Consult Oracle for epistemic guidance
   - Generate PDF using WAFT evolution principles
   - Print the created PDF
   - Log to Oracle: "Created and printed evolved PDF: {path}"

### 2.6 Oracle Integration

**Integration points:**

- Query Oracle for epistemic state before PDF creation
- Use Oracle insights to guide PDF content
- Log PDF operations to Oracle (findings)
- Use Oracle CHECK gate for PDF creation decisions

**Example:**

```python
oracle = TheOracle(project_path)
state = oracle.get_epistemic_state()
phase = oracle.get_epistemic_phase()

# Use phase to guide PDF type
if phase == "Data Gathering":
    pdf_type = "conversation_summary"
elif phase == "Synthesis":
    pdf_type = "oracle_insights"
# etc.
```

## Phase 3: WAFT Evolution Integration

### 3.1 Evolution Decision Making

**File:** `src/waft/core/pdf_evolution.py`

**Use WAFT principles:**

- "Part within the whole": PDF reflects current context within larger project
- "As above, so below": PDF structure mirrors epistemic state
- Evolution: PDF content evolves based on what system knows/doesn't know

**Implementation:**

- Analyze epistemic state (knowledge, uncertainty, findings, unknowns)
- Structure PDF to reflect current phase
- Include relevant findings and highlight unknowns
- Use evolution engine to refine content structure

### 3.2 Content Generation

**Approach:**

- Use `PDF.from_content()` or `PDF.from_template()` based on type
- Generate markdown content that:
  - Summarizes conversation context
  - Incorporates Oracle insights
  - Reflects epistemic state
  - Links to work efforts if relevant
  - Includes "part within the whole" perspective

## Phase 4: Testing and Documentation

### 4.1 Test Scenarios

1. **Existing PDF found:**

   - Recent PDF in project directory
   - Should print it

2. **No PDF found:**

   - Should create evolved PDF
   - Should consult Oracle
   - Should print created PDF

3. **Low relevance PDF found:**

   - Old PDF exists but not relevant
   - Should create new evolved PDF instead

4. **Oracle unavailable:**

   - Should still work without Oracle
   - Fallback to simple context-based creation

### 4.2 Documentation

**Update:**

- `.cursor/commands/print-PDF.md` - Full command documentation
- `docs/PDF_COMMANDS.md` - Overview of PDF-related commands
- Remove `--print` flags from other command docs (redirect to `/print-PDF`)

## Phase 5: Global Command Sync

### 5.1 Sync to Global Location

**Action:** After implementation, run:

```bash
./scripts/sync-cursor-commands.sh
```

This makes `/print-PDF` available globally in all Cursor instances.

## Files to Modify

### New Files

- `.cursor/commands/print-PDF.md` - Command documentation
- `src/waft/core/pdf_discovery.py` - PDF discovery system
- `src/waft/core/pdf_evolution.py` - PDF evolution system

### Modified Files

- `src/waft/main.py` - Add `print_pdf` command
- `src/waft/pdf.py` - Verify print method is opt-in only
- `.cursor/commands/pdf-me.md` - Update to mention `/print-PDF` for printing
- `.cursor/commands/waft-docs.md` - Update to mention `/print-PDF` for printing
- Other command docs - Remove automatic printing references

## Implementation Notes

### Philosophy Integration

**"The part within the whole":**

- PDF reflects current work within larger project context
- Includes links to related work efforts
- Shows how current session fits into project evolution

**"As above, so below":**

- PDF structure mirrors epistemic state
- High knowledge → structured, detailed PDF
- High uncertainty → exploratory, question-focused PDF
- Oracle phase → PDF type and content structure

### WAFT Evolution

- PDF content evolves based on:
  - What system knows (findings)
  - What system doesn't know (unknowns)
  - Current epistemic phase
  - Conversation context
  - Active work efforts

### Oracle Integration

- Query epistemic state before creation
- Use insights to guide content
- Log operations as findings
- Use CHECK gates for decisions

## Success Criteria

1. ✅ No automatic printing in any command
2. ✅ `/print-PDF` command works globally
3. ✅ Finds relevant PDFs based on context
4. ✅ Creates evolved PDFs when needed
5. ✅ Integrates with Oracle for intelligence
6. ✅ Uses WAFT evolution principles
7. ✅ Reflects "part within the whole" philosophy
8. ✅ Documentation updated