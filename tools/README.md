# Technical Whitepaper Generator

**Automated Evidence-Backed Technical Analysis Document Generator**

A Python tool for creating professional, publication-quality technical whitepapers using Typst. Designed for systematic investigation documentation with evidence tracking.

## Features

✅ **Project Scaffolding** - Initialize complete whitepaper structure
✅ **Modular Sections** - Write sections independently, compile separately  
✅ **Professional Styling** - Pre-configured Typst templates with callouts, metrics, evidence boxes
✅ **Auto-Compilation** - Build individual sections or complete documents
✅ **Status Tracking** - Monitor progress across all sections
✅ **Reusable Templates** - Standardized structure for consistent documentation

## Installation

### Prerequisites

```bash
# Install Typst (macOS)
brew install typst

# Install Python dependencies
pip install pyyaml
```

### Setup

```bash
# Clone or copy the tool
cp whitepaper_generator.py ~/bin/
chmod +x ~/bin/whitepaper_generator.py

# Or use directly from tools/
cd /path/to/your/project
python3 tools/whitepaper_generator.py
```

## Quick Start

### 1. Initialize a New Whitepaper

```bash
cd /path/to/your/analysis/project
python3 /path/to/whitepaper_generator.py init "My Technical Analysis"
```

**This creates:**
```
your-project/
├── whitepaper_config.yaml    # Configuration
├── whitepaper_functions.typ   # Reusable Typst functions
├── MAIN.typ                   # Main compilation file
├── sections/                  # Section files
│   ├── 00_title_page.typ
│   ├── 01_abstract.typ
│   ├── 02_executive_summary.typ
│   ├── 10_introduction.typ
│   ├── 20_methodology.typ
│   ├── 30_findings.typ
│   ├── 40_analysis.typ
│   ├── 50_discussion.typ
│   ├── 60_conclusion.typ
│   └── A0_appendix.typ
├── section_pdfs/              # Individual section PDFs
└── typst_template/            # Template files
```

### 2. Write a Section

Edit `sections/10_introduction.typ`:

```typst
#import "../whitepaper_functions.typ": callout, evidence, metric

= Introduction

This is my introduction content.

#callout(type: "info", title: "Key Finding", [
  Important discovery goes here.
])

#evidence("src/file.py:10-20", [
  ```python
  def example():
      return "code evidence"
  ```
])

#metric("Tests Passing", "42", unit: "of 50")
```

### 3. Compile Individual Section

```bash
python3 whitepaper_generator.py compile-section 10_introduction
```

**Output:** `section_pdfs/10_introduction.pdf` (auto-opens)

### 4. Check Status

```bash
python3 whitepaper_generator.py status
```

**Output:**
```
📊 Project Status: My Technical Analysis
============================================================
Author: Technical Analyst
Version: 1.0
Date: 2026-01-24

📁 Sections (10):
   ✅ Written    | 00_title_page            |  1p | Title Page
   ✅ Written    | 01_abstract              |  1p | Abstract
   📝 Stub       | 02_executive_summary     |  1p | Executive Summary
   📝 Stub       | 10_introduction          |  4p | Introduction
   ...
============================================================
Progress: 2/10 sections written
Estimated pages: 32
```

### 5. Compile Complete Whitepaper

```bash
python3 whitepaper_generator.py compile-all
```

**Output:** `My_Technical_Analysis_COMPLETE.pdf` (auto-opens)

## Configuration

Edit `whitepaper_config.yaml` to customize:

```yaml
title: "My Technical Analysis"
author: "Dr. Aria Vex"
date: "2026-01-24"
version: "1.0"

sections:
  - id: "10_introduction"
    title: "Introduction"
    pages: 4
    required: true

styling:
  primary_color: "#1976d2"
  success_color: "#4caf50"
  warning_color: "#f57c00"
  danger_color: "#d32f2f"
  font_body: "New Computer Modern"
  font_code: "JetBrains Mono"
```

## Available Typst Functions

### Callout Boxes

```typst
#callout(type: "info", title: "Title", [
  Content goes here.
])

// Types: info, success, warning, danger, note
```

### Evidence Boxes

```typst
#evidence("src/file.py:10-20", [
  ```python
  def example():
      return "verified code"
  ```
])
```

### Metrics

```typst
#metric("Label", "Value", unit: "unit")
// Example: Tests Passing | 42 | of 50
```

## Workflow Example

**For a WAFT-style analysis:**

```bash
# 1. Initialize
python3 whitepaper_generator.py init "WAFT Analysis"

# 2. Customize config (add your sections)
vim whitepaper_config.yaml

# 3. Write sections in order
vim sections/10_introduction.typ
python3 whitepaper_generator.py compile-section 10_introduction

vim sections/20_methodology.typ
python3 whitepaper_generator.py compile-section 20_methodology

vim sections/30_findings.typ
python3 whitepaper_generator.py compile-section 30_findings

# 4. Check progress
python3 whitepaper_generator.py status

# 5. Compile complete document
python3 whitepaper_generator.py compile-all
```

## Section Naming Convention

Use hexadecimal prefixes for ordering:

- `00-0F`: Front matter (title, abstract, TOC)
- `10-9F`: Main body chapters
- `A0-BF`: Conclusions and assessments
- `C0-DF`: Appendices
- `D0-FF`: Back matter (references, glossary, index)

## Troubleshooting

### Typst Compilation Errors

**Problem:** `error: unclosed label`
**Solution:** Escape `<` symbols: `less than` instead of `<`

**Problem:** `error: no text within stars`
**Solution:** Use single `*` for emphasis, not `**` in isolation

**Problem:** `error: unknown variable: diagram`
**Solution:** Add import: `#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge`

### Section Not Compiling

```bash
# Test section syntax manually
cd your-project
typst compile sections/10_introduction.typ test.pdf
```

### Missing Fonts

If fonts are missing, edit `whitepaper_config.yaml`:

```yaml
styling:
  font_body: "Arial"  # Use system font
  font_code: "Courier"
```

## Advanced Usage

### Custom Section Templates

Create `templates/section_template.typ`:

```typst
#import "../whitepaper_functions.typ": callout, evidence, metric

= {{TITLE}}

#callout(type: "note", title: "Section Overview", [
  *Purpose:* {{PURPOSE}}
  *Pages:* {{PAGES}}
])

== {{TITLE}}.1 Background

== {{TITLE}}.2 Analysis

== {{TITLE}}.3 Findings
```

### Batch Compilation

```bash
# Compile all sections
for section in sections/*.typ; do
  id=$(basename "$section" .typ)
  python3 whitepaper_generator.py compile-section "$id"
done
```

### Custom Styling

Edit `whitepaper_functions.typ` to add your own functions:

```typst
#let my_custom_box(content) = {
  block(
    fill: rgb("#your-color"),
    stroke: 2pt + rgb("#border-color"),
    radius: 4pt,
    inset: 16pt,
    width: 100%,
    content
  )
}
```

## Real-World Example

This tool was built from the **WAFT Framework Analysis** workflow, which produced a 72-page evidence-backed whitepaper with:

- 29 figures
- 28 tables
- 12 code listings
- 6 major sections
- Full source code verification
- Test execution outputs
- Telemetry data samples

**Result:** Professional publication-quality PDF generated from modular Typst sections.

## Command Reference

| Command | Description |
|---------|-------------|
| `init <name>` | Initialize new whitepaper project |
| `compile-section <id>` | Compile single section to PDF |
| `compile-all` | Compile complete whitepaper |
| `status` | Show project status and progress |

## Contributing

To add new features:

1. Fork the tool
2. Add new commands to `main()`
3. Implement methods in `WhitepaperGenerator` class
4. Update README with usage examples

## License

MIT License - Use freely for technical documentation

## Credits

Built for the **WAFT Framework Evidence-Backed Analysis** project by Dr. Aria Vex.

Inspired by the need for systematic, reproducible technical investigation documentation.
