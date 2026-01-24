# Technical Whitepaper Generator - Complete Example

## Installation & Setup

```bash
# 1. Install Typst
brew install typst

# 2. Install Python dependencies
pip install pyyaml

# 3. Make the generator executable
chmod +x /path/to/whitepaper_generator.py
```

## Example: Creating a "System Analysis" Whitepaper

### Step 1: Initialize Project

```bash
cd ~/Documents/my-analysis
python3 /path/to/whitepaper_generator.py init "System Analysis v2.0"
```

**Created Structure:**
```
my-analysis/
├── whitepaper_config.yaml          # ← Edit this to customize
├── whitepaper_functions.typ         # ← Reusable Typst functions
├── MAIN.typ                         # ← Main compilation file
├── sections/
│   ├── 00_title_page.typ           # ← Edit these
│   ├── 01_abstract.typ
│   ├── 02_executive_summary.typ
│   ├── 10_introduction.typ
│   ├── 20_methodology.typ
│   ├── 30_findings.typ
│   ├── 40_analysis.typ
│   ├── 50_discussion.typ
│   ├── 60_conclusion.typ
│   └── A0_appendix.typ
├── section_pdfs/                    # ← Compiled PDFs go here
└── typst_template/                  # ← Template files
```

### Step 2: Customize Configuration

Edit `whitepaper_config.yaml`:

```yaml
title: "System Analysis v2.0"
author: "Dr. Jane Smith"
date: "2026-01-24"
version: "2.0"

sections:
  # Add your custom sections
  - id: "10_introduction"
    title: "Introduction"
    pages: 4
    required: true
  
  - id: "20_methodology"
    title: "Methodology"
    pages: 3
    required: true
  
  - id: "30_scint_analysis"  # Custom section!
    title: "Scint System Analysis"
    pages: 15
    required: true
  
  - id: "40_genome_tracking"
    title: "Genome Tracking"
    pages: 5
    required: true

styling:
  primary_color: "#1976d2"
  success_color: "#4caf50"
  font_body: "New Computer Modern"
  font_code: "JetBrains Mono"
```

### Step 3: Write Your First Section

Edit `sections/10_introduction.typ`:

```typst
// Introduction
// Pages 1-4

#import "../whitepaper_functions.typ": callout, evidence, metric

= Introduction

#v(0.2in)

== 1.1 Background

This analysis investigates the XYZ system architecture.

#callout(type: "info", title: "Project Context", [
  *System:* XYZ Framework v2.0
  *Analysis Duration:* 8 hours
  *Evidence Collected:* 1,200+ files analyzed
])

== 1.2 Key Discoveries

#grid(
  columns: (1fr, 1fr, 1fr),
  gutter: 0.2in,
  
  metric("Files Analyzed", "1,200", unit: "total"),
  metric("Tests Passing", "95", unit: "of 100"),
  metric("Completeness", "78%", unit: "verified"),
)

== 1.3 Methodology

We employed a **Skeptical Researcher Protocol**:

#callout(type: "success", title: "Investigation Principles", [
  1. **Verify Everything** - Assume nothing
  2. **Quantify Precisely** - No hand-waving
  3. **Document Gaps** - Failures are data
])

=== 1.3.1 Evidence Collection

#evidence("src/core/system.py:105-141", [
  ```python
  def verify_system():
      """Core verification logic."""
      results = run_tests()
      return results.summary()
  ```
])

This code demonstrates the verification approach.

#callout(type: "warning", title: "Limitations", [
  - No security testing performed
  - Limited to functional analysis only
  - 8-hour time constraint
])

== 1.4 Document Structure

*Part I:* Investigation Methodology (pages 1-8)

*Part II:* Core Findings (pages 9-50)

*Part III:* Analysis & Discussion (pages 51-65)

*Part IV:* Appendices (pages 66-72)
```

### Step 4: Compile the Section

```bash
python3 whitepaper_generator.py compile-section 10_introduction
```

**Result:**
- PDF created: `section_pdfs/10_introduction.pdf`
- Automatically opens in your PDF viewer
- Check formatting before continuing

### Step 5: Continue with More Sections

```bash
# Write sections/20_methodology.typ
# Then compile:
python3 whitepaper_generator.py compile-section 20_methodology

# Write sections/30_scint_analysis.typ
# Then compile:
python3 whitepaper_generator.py compile-section 30_scint_analysis

# Check progress
python3 whitepaper_generator.py status
```

**Status Output:**
```
📊 Project Status: System Analysis v2.0
============================================================
Author: Dr. Jane Smith
Version: 2.0
Date: 2026-01-24

📁 Sections (10):
  📄 ✅ Written    | 10_introduction          |  4p | Introduction
  📄 ✅ Written    | 20_methodology           |  3p | Methodology
  📄 ✅ Written    | 30_scint_analysis        | 15p | Scint System Analysis
   📝 Stub       | 40_genome_tracking       |  5p | Genome Tracking
   📝 Stub       | 50_discussion            |  5p | Discussion
   📝 Stub       | 60_conclusion            |  2p | Conclusion
============================================================
Progress: 3/10 sections written
Estimated pages: 34
```

### Step 6: Compile Complete Whitepaper

Once all sections are written:

```bash
python3 whitepaper_generator.py compile-all
```

**Result:**
- Complete PDF: `System_Analysis_v2.0_COMPLETE.pdf`
- All sections integrated
- Auto-generated Table of Contents
- Professional formatting
- Automatically opens

## Available Typst Functions

### 1. Callout Boxes (5 types)

```typst
#callout(type: "info", title: "Information", [
  General information content.
])

#callout(type: "success", title: "Success", [
  Confirmed findings.
])

#callout(type: "warning", title: "Warning", [
  Limitations or concerns.
])

#callout(type: "danger", title: "Critical", [
  Major issues or failures.
])

#callout(type: "note", title: "Note", [
  Additional context.
])
```

### 2. Evidence Boxes

```typst
#evidence("src/file.py:105-141", [
  ```python
  def example_function():
      return "verified code"
  ```
])

#evidence("Command output", [
  ```bash
  $ pytest tests/
  ======================== 42 passed in 0.23s ========================
  ```
])
```

### 3. Metrics

```typst
#metric("Label", "Value", unit: "description")

// Examples:
#metric("Tests Passing", "42", unit: "of 50")
#metric("Completeness", "78%", unit: "verified")
#metric("Files Analyzed", "1,200", unit: "total")
```

### 4. Grids for Layout

```typst
#grid(
  columns: (1fr, 1fr, 1fr),
  gutter: 0.2in,
  
  metric("Metric 1", "100"),
  metric("Metric 2", "200"),
  metric("Metric 3", "300"),
)
```

### 5. Tables

```typst
#figure(
  table(
    columns: (auto, auto, 1fr),
    align: (left, center, left),
    [*Column 1*], [*Column 2*], [*Column 3*],
    [Row 1 A], [Row 1 B], [Row 1 C],
    [Row 2 A], [Row 2 B], [Row 2 C],
  ),
  caption: [Table Description]
)
```

### 6. Diagrams (Fletcher)

```typst
#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge

#figure(
  diagram(
    spacing: (15mm, 12mm),
    node-stroke: 2pt + rgb("#1976d2"),
    edge-stroke: 2pt + rgb("#1976d2"),
    
    node((0, 0), [Step 1], shape: rect),
    node((0, 1), [Step 2], shape: rect),
    node((0, 2), [Step 3], shape: rect),
    
    edge((0, 0), (0, 1), "->", label: "process"),
    edge((0, 1), (0, 2), "->", label: "verify"),
  ),
  caption: [Process Flow]
)
```

## Common Patterns

### Investigation Section Template

```typst
= Section Title

#callout(type: "success", title: "✅ VERIFIED - 85% Complete", [
  Brief summary of findings.
])

== Claim Statement

#quote(block: true)[
  *"Original claim from documentation"*
])

== Source Code Evidence

#evidence("src/file.py:10-30", [
  ```python
  # Actual implementation
  ```
])

== Test Verification

#evidence("Test output", [
  ```bash
  $ pytest tests/test_feature.py -v
  ======================== 5 passed in 0.23s ========================
  ```
])

== Completeness Assessment

#callout(type: "warning", title: "Implementation Gaps", [
  - Gap 1
  - Gap 2
])

#callout(type: "success", title: "Final Score: 85%", [
  *Rationale:* Core functionality complete, minor gaps documented.
])
```

## Troubleshooting

### Common Typst Errors

**Error:** `unclosed label`
**Fix:** Escape `<` symbols:
```typst
// Bad
*Low (<50%):* text

// Good
*Low (less than 50%):* text
```

**Error:** `no text within stars`
**Fix:** Don't use empty `**`:
```typst
// Bad
**Trade-off:** text

// Good
*Trade-off:* text
```

**Error:** `unknown variable: diagram`
**Fix:** Add import at top of section:
```typst
#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge
```

### Compilation Issues

If a section fails to compile:

```bash
# Test directly with Typst
cd your-project
typst compile sections/10_introduction.typ test.pdf

# Check for syntax errors
cat sections/10_introduction.typ | grep -n "<\|**"
```

## Best Practices

1. **Write incrementally** - Compile each section before moving to next
2. **Use evidence boxes** - Back up every claim with code/output
3. **Quantify metrics** - Use exact numbers, not vague descriptions
4. **Document gaps** - Note limitations explicitly
5. **Test early** - Compile sections frequently to catch errors
6. **Keep sections modular** - Each section should be independently compilable

## Complete Workflow Summary

```bash
# 1. Initialize
python3 whitepaper_generator.py init "My Analysis"

# 2. Customize
vim whitepaper_config.yaml

# 3. Write & compile iteratively
for section in 10_intro 20_method 30_findings; do
  vim sections/${section}.typ
  python3 whitepaper_generator.py compile-section $section
done

# 4. Check progress
python3 whitepaper_generator.py status

# 5. Compile complete document
python3 whitepaper_generator.py compile-all

# 6. Review output
open *_COMPLETE.pdf
```

## Example Output

**From the WAFT Analysis:**
- **72 pages** of evidence-backed analysis
- **29 figures**, **28 tables**, **12 code listings**
- **6 major sections** with sub-sections
- Professional publication quality
- Full source code verification
- Test execution outputs included
- Telemetry data samples embedded

**Result:** A comprehensive, reproducible technical investigation document ready for stakeholder review or publication.
