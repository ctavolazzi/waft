# /plans-report - Plans Report Generator

**Purpose:** Create a comprehensive plans report using the science-textbook-template, compiling all plans from `_work_efforts/Plans/` into a beautiful LaTeX textbook-style PDF.

**Usage:** `/plans-report [options]`

**Script:** `scripts/create_plans_report.py`

---

## Overview

The Plans Report creates a professional textbook-style document:
- **All Plans**: Gathers every `.plan.md` file from `_work_efforts/Plans/`
- **LaTeX Textbook**: Uses science-textbook-template structure
- **Professional Format**: Title pages, table of contents, chapters
- **Comprehensive**: Includes plan metadata, content, and index

**Perfect for:**
- Reviewing all plans at once
- Planning sessions
- Project documentation
- Binder-ready reports

---

## Quick Start

### Basic Plans Report
```
/plans-report
```

### With Custom Title
```
/plans-report title:"Project Plans 2026"
```

### Limit Number of Plans
```
/plans-report limit:50
```

### City Plan Mode (Condensed Strategic Overview)
```
/plans-report --city-plan
```

**City Plan** creates a condensed strategic overview:
- Groups plans into categories (districts)
- Shows top plans per category
- Statistics and high-level view
- Much smaller, more digestible format
- Perfect for seeing the "big picture"

### Custom Output Path
```
/plans-report output:"reports/my_plans.pdf"
```

---

## Features

- **Automatic Discovery**: Finds all `.plan.md` files recursively
- **YAML Frontmatter**: Parses plan metadata (name, overview, todos, status)
- **Markdown Conversion**: Converts plan content to LaTeX
- **Textbook Structure**:
  - Half title page
  - Full title page
  - Colophon
  - Preface
  - Table of contents
  - Chapters (one per plan)
  - Index of plans
- **Professional Formatting**: Uses science-textbook-template style

---

## Output

All reports are saved to:
- `_work_efforts/briefs/Plans_Report_YYYYMMDD.pdf`

Format:
- **Title Pages**: Professional textbook-style covers
- **Table of Contents**: Auto-generated from chapters
- **Chapters**: One chapter per plan with full content
- **Index**: Complete list of all plans with file paths

---

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--title` | Report title | "Plans Report" |
| `--output` | Output PDF path | Auto-generated with date |
| `--plans-dir` | Custom plans directory | `_work_efforts/Plans/` |
| `--limit` | Limit number of plans | All plans |
| `--city-plan` | Generate condensed City Plan view | Full detailed report |

---

## Examples

### Basic Report
```
/plans-report
```

### Custom Title
```
/plans-report title:"Q1 2026 Plans"
```

### Top 100 Plans
```
/plans-report limit:100 title:"Top Plans"
```

### City Plan (Strategic Overview)
```
/plans-report --city-plan title:"WAFT City Plan"
```

### Specific Directory
```
/plans-report plans-dir:"_work_efforts/Plans/_organized_constellation"
```

---

## Integration

The Plans Report integrates with:
- Work efforts system (`_work_efforts/Plans/`)
- LaTeX template system
- Plan file structure (YAML frontmatter + markdown)

---

## Technical Details

- **Template**: Based on [science-textbook-template](https://github.com/ironmeld/science-textbook-template)
- **LaTeX Compiler**: Uses `pdflatex` (2 runs for TOC)
- **Markdown Parser**: Custom converter with YAML frontmatter support
- **File Discovery**: Recursive search for `*.plan.md` files

---

## Related Commands

- **`/evening-report`** - Evening status report
- **`/midday-dossier`** - Midday status report
- **`/dossier`** - Comprehensive mission sitrep
- **`/brief`** - Quick brief document

---

**Created for comprehensive plans review and documentation.**

--- End Command ---
