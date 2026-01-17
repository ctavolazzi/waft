# /show-me - Display Concepts, Operations, and Data

**Shows everything relevant happening in the current chat session.**

---

## Purpose

This command displays a comprehensive overview of:
- **Work Efforts**: Current and recent work efforts from this session
- **LaTeX Templates**: Available templates in the registry
- **Librarian Catalog**: Cataloged records and templates
- **Experiments**: Recent scientific method experiments
- **Chat Context**: Key concepts and operations from current conversation

**Use when:**
- You want to see what's been done in this chat
- You need an overview of available resources
- You want to understand the current state of the system
- You need to see what templates, work efforts, or data are available

---

## Usage

```bash
/show-me [OPTIONS]
```

**Options:**
- `--work-efforts, -w`: Show work efforts (default: true)
- `--templates, -t`: Show LaTeX templates (default: true)
- `--catalog, -c`: Show Librarian catalog (default: true)
- `--experiments, -e`: Show recent experiments (default: true)
- `--chat-context, -x`: Show chat context summary (default: true)
- `--proof-cases, -p`: Show recent proof cases (default: true)
- `--all, -a`: Show everything (default)
- `--format, -f`: Output format (html, table, json, markdown, pdf, latex) - **default: html**
- `--output, -o`: Output file path (required for html/pdf/latex formats)
- `--convert, -c`: Convert HTML to another format (pdf, latex) - only works with html format

---

## Examples

```bash
# Generate HTML report (default - WAFT's preferred format)
/show-me --output overview.html

# Generate HTML and convert to PDF
/show-me --output overview.html --convert pdf

# Generate HTML and convert to LaTeX
/show-me --output overview.html --convert latex

# Generate PDF directly (HTML intermediate)
/show-me --format pdf --output overview.pdf

# Generate LaTeX directly (HTML intermediate)
/show-me --format latex --output overview.tex

# Show in table format (console)
/show-me --format table

# Show in JSON format
/show-me --format json

# Show only work efforts and templates
/show-me --work-efforts --templates --format html --output we_templates.html
```

---

## What Gets Displayed

### 1. Work Efforts
- Current session work efforts (from today)
- Recent work efforts from `_work_efforts/`
- Status (open, active, completed, paused)
- Work effort ID and title extracted from index files
- **Note**: Looks for index files using work effort ID (e.g., `WE-260116-65m0_index.md`) extracted from directory name

### 2. LaTeX Templates
- All registered templates from LaTeXTemplateRegistry
- Categories and tags
- Template descriptions
- Available generate functions

### 3. Librarian Catalog
- Cataloged records
- Templates in catalog
- Records by type and category
- Recent catalog entries

### 4. Experiments
- Recent scientific method experiments
- Experiment results
- Hypothesis verification status
- Data collected

### 5. Chat Context
- Key concepts discussed
- Operations performed
- Files created/modified
- Systems integrated

---

## Output Format

### HTML Format (Default) ⭐
**WAFT's preferred format** - Beautiful, WAFT-branded HTML template with integrated PDF conversion algorithm.

**WAFT HTML Template Features:**
- 🎨 **WAFT-branded styling** - Gradient header with WAFT logo and colors
- 📄 **Integrated PDF conversion** - Built-in WeasyPrint algorithm
- 🖨️ **Print-optimized CSS** - Perfect for PDF generation
- 📱 **Responsive design** - Works on all screen sizes
- 🏷️ **Semantic HTML** - Proper document structure
- ⚡ **Fast conversion** - HTML → PDF in one step

**Conversion Options:**
- **PDF**: Use `--convert pdf` or `--format pdf` (uses integrated algorithm)
- **LaTeX**: Use `--convert latex` or `--format latex`
- **Other formats**: HTML is a universal intermediate format

**Template Location:** `src/waft/templates/waft_html_template.py`

### Table Format
Organized sections with Rich tables (console output):
- Work Efforts table
- Templates table
- Catalog summary
- Experiments summary
- Chat context summary

### JSON Format
Structured JSON with all data:
```json
{
  "work_efforts": [...],
  "templates": [...],
  "catalog": {...}},
  "experiments": [...],
  "chat_context": {...},
  "proof_cases": [...]
}
```

### Markdown Format
Markdown document with sections:
- Work Efforts list
- Templates list
- Catalog entries
- Experiments
- Proof cases
- Chat summary

### PDF Format
Generated from HTML using WeasyPrint:
- Professional styling
- Print-ready
- Includes all sections

### LaTeX Format
Generated from HTML:
- Academic document structure
- Can be compiled with pdflatex/xelatex
- Includes proper LaTeX commands

---

## Integration

This command uses:
- **LaTeXTemplateRegistry**: `get_latex_registry()`
- **Librarian**: `Librarian(project_path)`
- **Work Efforts System**: Scans `_work_efforts/` directory for today's work efforts
- **Scientific Method Tool**: Reads experiment files from `scientific_method_tool/proof_experiments/`
- **Chat Context**: Returns static summary (can be enhanced to analyze conversation)

## Implementation Details

**Work Effort Detection**:
- Scans `_work_efforts/` for directories starting with `WE-`
- Filters to work efforts from today (date pattern in work effort ID)
- Extracts work effort ID from directory name (part before first underscore)
- Looks for index file: `{work_effort_id}_index.md`
- Falls back to `{directory_name}_index.md` if not found
- Extracts status and title from index file frontmatter

**Known Issues Fixed**:
- ✅ Fixed index file naming mismatch (2026-01-16)
- ✅ Improved status detection to handle "open" status
- ✅ Work effort ID extraction from directory names

---

## When to Use

**Use `/show-me` when**:
- ✅ Want overview of current session
- ✅ Need to see available resources
- ✅ Want to understand system state
- ✅ Need to find templates or work efforts
- ✅ Want to see what's been cataloged
- ✅ Need context for next steps

**Don't use `/show-me` when**:
- ❌ Need detailed analysis (use specific commands)
- ❌ Need to modify data (use specific commands)
- ❌ Need real-time updates (use monitoring tools)

---

## Output Location

- **Console**: Formatted display with Rich tables
- **File** (if `--output` specified): Markdown or JSON file

---

**This command provides a comprehensive overview of everything relevant in the current chat session.**

--- End Command ---
