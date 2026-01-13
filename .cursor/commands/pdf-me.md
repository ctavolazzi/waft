# /pdf-me - PDF Generator from Markdown

**Purpose:** Generate professional PDFs from markdown files and optionally print them.

**Usage:** `/pdf-me <file_path> [options]`

**Script:** Uses `PDFGenerator` from `src/waft.evolution.pdf_generator`

---

## Overview

The PDF-me command generates professional PDFs from markdown files using WAFT's PDF generation system. Perfect for creating printable versions of plans, documentation, work efforts, or any markdown content.

**Features:**
- Generate PDFs from any markdown file
- Professional formatting (clinical_standard style)
- Automatic title detection
- Optional printing
- Opens PDF in Preview automatically

---

## Quick Start

### Basic Usage
```
/pdf-me _work_efforts/PLAN_BOOKLET_CREATOR_INTEGRATION.md
```

### With Custom Title
```
/pdf-me _work_efforts/PLAN_BOOKLET_CREATOR_INTEGRATION.md title:"Booklet Plan"
```

### Print PDF
```
/pdf-me _work_efforts/PLAN_BOOKLET_CREATOR_INTEGRATION.md
/print-PDF
```

**Note:** The `/pdf-me` command no longer has a `--print` flag. Use `/print-PDF` to print PDFs intelligently based on context.

### Specify Output Path
```
/pdf-me _work_efforts/PLAN_BOOKLET_CREATOR_INTEGRATION.md --output plan.pdf
```

---

## Usage Examples

### Generate PDF from Plan
```
/pdf-me _work_efforts/PLAN_BOOKLET_CREATOR_INTEGRATION.md
```

### Generate and Print
```
/pdf-me _work_efforts/PLAN_BOOKLET_CREATOR_INTEGRATION.md
/print-PDF
```

**Note:** Use `/print-PDF` to print the generated PDF (or any relevant PDF).

### Generate with Custom Title
```
/pdf-me docs/README.md title:"Project Documentation"
```

### Generate Work Effort PDF
```
/pdf-me _work_efforts/WE-260112-ffbt_booklet_creator_integration_prototype/WE-260112-ffbt_index.md
```

---

## Command Options

### Required
- **File Path**: Path to markdown file (relative or absolute)

### Optional
- **`--title "Title"`** or **`title:"Title"`**: Custom PDF title (default: extracted from filename)
- **`--output <path>`**: Custom output path (default: same directory as input with `.pdf` extension)
- **`--print`**: ❌ **REMOVED** - Use `/print-PDF` command instead for intelligent printing
- **`--no-open`**: Don't open PDF in Preview (default: opens automatically)
- **`--style <style>`**: PDF style (default: `clinical_standard`, options: `clinical_standard`, `premium`, `professional`)

---

## Output

**Default Location:**
- Same directory as input file
- Filename: `[original_name].pdf`
- Example: `PLAN_BOOKLET_CREATOR_INTEGRATION.md` → `PLAN_BOOKLET_CREATOR_INTEGRATION.pdf`

**Format:**
- Professional formatting (clinical_standard style)
- Print-ready (1 inch margins)
- Academic weight (Times New Roman body, Helvetica headers)
- Proper page breaks and typography

---

## Implementation

The command uses WAFT's `PDFGenerator` class:

```python
from pathlib import Path
from src.waft.evolution.pdf_generator import PDFGenerator

# Read markdown file
content = Path(file_path).read_text()

# Generate PDF
generator = PDFGenerator.from_content(
    content=content,
    title=title or extract_title(file_path),
    style=style or "clinical_standard"
)

# Save PDF
output_path = output or Path(file_path).with_suffix('.pdf')
generator.save(output_path, open_pdf=not no_open)

# Print if requested
if print_pdf:
    import subprocess
    subprocess.run(['lp', str(output_path)])
```

---

## Integration

This command integrates with:
- **PDFGenerator**: Core PDF generation system
- **DocumentBuilder**: Alternative PDF generation (future)
- **One-Pager System**: For 2-page documents (use `/one-pager` instead)
- **WAFT Docs**: For field guides and booklets (use `/waft-docs` instead)

---

## When to Use

**Use `/pdf-me` when:**
- ✅ Need PDF from markdown file
- ✅ Want professional formatting
- ✅ Need to print documentation
- ✅ Creating printable versions of plans/work efforts

**Don't use `/pdf-me` when:**
- ❌ Need 2-page one-pager (use `/one-pager`)
- ❌ Need field guide/booklet (use `/waft-docs`)
- ❌ Need specialized formatting (use specific generators)

---

## Examples

### Generate Plan PDF
```
/pdf-me _work_efforts/PLAN_BOOKLET_CREATOR_INTEGRATION.md
```

### Generate and Print Plan
```
/pdf-me _work_efforts/PLAN_BOOKLET_CREATOR_INTEGRATION.md
/print-PDF
```

### Generate Work Effort PDF
```
/pdf-me _work_efforts/WE-260112-ffbt_booklet_creator_integration_prototype/PLANNING_LINEAGE.md title:"Planning Lineage"
```

### Generate Documentation PDF
```
/pdf-me docs/PDF_GENERATION_GUIDE.md --style premium
```

---

## Related Commands

- **`/print-PDF`** - Intelligently find and print relevant PDFs (use this for printing)
- **`/one-pager`** - Generate 2-page one-pagers
- **`/waft-docs`** - Generate field guides and booklets
- **`/one-pager-chat`** - Generate one-pager from chat session

---

**Command Status**: ✅ Ready to use
