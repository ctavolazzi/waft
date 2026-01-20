#import "@preview/s6t5-page-bordering:1.0.0": s6t5-page-bordering
#import "@preview/typsium-iso-7010:0.1.0": *

// Custom header for WAFT ISO 7010 Usage Guide
#let header = {
  set align(bottom)
  show table.cell.where(y: 0): set align(left)
  set text(weight: "bold", size: 9pt)
  table(
    stroke: (y: none),
    columns: (0.8fr, 1.4fr, 0.8fr),
    rows: 1fr,
    table.hline(),
    [WAFT-ISO-7010], [WAFT ISO 7010 Usage Guide], [
      #context counter(page).display(
        "1 / 1",
        both: true,
      )
    ],
  )
}

// Custom footer
#let footer = {
  set text(weight: "bold", size: 9pt)
  table(
    stroke: (y: none),
    columns: (0.8fr, 1.4fr, 0.8fr),
    rows: 1fr,
    [WAFT-ISO-7010], [WAFT Project Documentation], [
      #context counter(page).display(
        "1 / 1",
        both: true,
      )
    ],
    table.hline(),
  )
}

#show: s6t5-page-bordering.with(
  margin: (left: 30pt, right: 30pt, top: 60pt, bottom: 60pt),
  expand: 15pt,
  space-top: 15pt,
  space-bottom: 15pt,
  stroke-header: 1pt,
  stroke-footer: 1pt,
  header: header,
  footer: footer,
)

// Color scheme
#let primary-blue = rgb("#1a237e")
#let warning-yellow = rgb("#f57f17")
#let danger-red = rgb("#c62828")
#let safety-green = rgb("#2e7d32")
#let code-bg = rgb("#f5f5f5")

#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true, first-line-indent: 0.5cm)
#set heading(numbering: "1.")

= WAFT ISO 7010 Safety Symbols Usage Guide

#align(center)[
  #text(size: 14pt, style: "italic", fill: primary-blue)[
    Complete Guide for Using ISO 7010 Symbols in WAFT
    #linebreak()
    Practical Examples and Best Practices
  ]
]

#v(1cm)

== Quick Start

=== Installation

The `typsium-iso-7010` package is automatically available in WAFT Typst documents. No installation needed - just import it:

```typst
#import "@preview/typsium-iso-7010:0.1.0": *
```

=== Basic Usage

```typst
#warning-sign(1, height: 2cm)
#fire-sign(1, height: 2cm)
#emergency-sign(1, height: 2cm)
```

#v(1cm)

== Using WAFT Wrapper Functions

WAFT provides convenient Python functions for generating documents with ISO 7010 symbols.

=== Method 1: `generate_worldbuild_iso()`

Full control over symbol placement:

```python
from pathlib import Path
from src.waft.templates.typst.wrappers.worldbuild_iso import generate_worldbuild_iso

safety_symbols = [
    {
        "function": "warning-sign",
        "code": 3,  # Electric shock
        "label": "Electrical Hazard",
        "description": "High voltage equipment. Do not touch."
    },
    {
        "function": "fire-sign",
        "code": 1,  # Fire extinguisher
        "label": "Fire Extinguisher",
        "description": "Located 10 meters to your right."
    }
]

pdf_path = generate_worldbuild_iso(
    title="Safety Information",
    content="Your document content...",
    output_path=Path("output/safety_info.pdf"),
    doc_id="SAFETY-001",
    safety_symbols=safety_symbols
)
```

=== Method 2: `generate_worldbuild_with_symbols()`

Simpler method using predefined symbol names:

```python
from src.waft.templates.typst.wrappers.worldbuild_iso import generate_worldbuild_with_symbols

pdf_path = generate_worldbuild_with_symbols(
    title="Laboratory Safety Guide",
    content="Your content...",
    output_path=Path("output/lab_safety.pdf"),
    symbols=["warning", "electric", "fire", "emergency", "first_aid"]
)
```

#text(weight: "bold")[Available predefined symbols:]
- `"warning"` - General warning
- `"danger"` - Danger
- `"electric"` - Electric shock
- `"radiation"` - Ionizing radiation
- `"biohazard"` - Biological hazard
- `"fire"` - Fire extinguisher
- `"emergency"` - Emergency exit
- `"first_aid"` - First aid

#v(1cm)

== Direct Typst Usage

For custom Typst templates, use symbols directly in your `.typ` files.

=== Import Statement

Always import at the top of your Typst file:

```typst
#import "@preview/typsium-iso-7010:0.1.0": *
```

=== Basic Functions

```typst
// Warning signs (yellow triangle)
#warning-sign(n, height: <size>)

// Fire signs (red square)
#fire-sign(n, height: <size>)

// Emergency signs (green square)
#emergency-sign(n, height: <size>)

// Directional arrows
#emergency-arrow(direction: "up" | "down" | "left" | "right", height: <size>)
#fire-arrow(direction: "up" | "down" | "left" | "right", height: <size>)
```

#v(1cm)

== Common Usage Patterns

=== Inline with Text

```typst
#warning-sign(3, height: 1em) indicates electrical hazards.
```

Example: #warning-sign(3, height: 1em) indicates electrical hazards.

=== In Grids

```typst
#grid(
  columns: 3,
  column-gutter: 12pt,
  align: center,
)[
  #warning-sign(1, height: 2cm),
  #fire-sign(1, height: 2cm),
  #emergency-sign(1, height: 2cm),
]
```

#grid(
  columns: 3,
  column-gutter: 12pt,
  align: center,
)[
  #warning-sign(1, height: 2cm),
  #fire-sign(1, height: 2cm),
  #emergency-sign(1, height: 2cm),
]

=== With Labels

```typst
#grid(
  columns: (1fr, 2fr),
  align: center,
)[
  #emergency-sign(1, height: 2cm),
  [
    *Emergency Exit*
    #linebreak()
    Use this door in case of emergency
  ],
]
```

#grid(
  columns: (1fr, 2fr),
  align: center,
)[
  #emergency-sign(1, height: 2cm),
  [
    *Emergency Exit*
    #linebreak()
    Use this door in case of emergency
  ],
]

=== With Directional Arrows

```typst
#grid(
  columns: 2,
  align: center,
)[
  #emergency-sign(1, height: 2cm),
  #emergency-arrow(direction: "right", height: 2cm),
]
```

#grid(
  columns: 2,
  align: center,
)[
  #emergency-sign(1, height: 2cm),
  #emergency-arrow(direction: "right", height: 2cm),
]

#v(1cm)

== Symbol Reference

=== Warning Signs (Yellow Triangle)

#grid(
  columns: (2fr, 3fr),
  column-gutter: 16pt,
  row-gutter: 12pt,
  align: center,
)[
  #warning-sign(1, height: 2cm)
  [
    #text(weight: "bold")[Warning Sign 1 (W001)]
    #linebreak()
    #text(style: "italic")[General warning]
    #linebreak()
    #v(4pt)
    #text(size: 9pt)[General hazard warning. Use when specific nature not covered by other signs.]
  ]
  
  #warning-sign(3, height: 2cm)
  [
    #text(weight: "bold")[Warning Sign 3 (W012)]
    #linebreak()
    #text(style: "italic")[Electricity]
    #linebreak()
    #v(4pt)
    #text(size: 9pt)[Risk of electric shock. Use near electrical equipment or high-voltage areas.]
  ]
]

=== Fire Signs (Red Square)

#grid(
  columns: (2fr, 3fr),
  column-gutter: 16pt,
  row-gutter: 12pt,
  align: center,
)[
  #fire-sign(1, height: 2cm)
  [
    #text(weight: "bold")[Fire Sign 1 (F001)]
    #linebreak()
    #text(style: "italic")[Fire extinguisher]
    #linebreak()
    #v(4pt)
    #text(size: 9pt)[Indicates location of fire extinguisher. Red square with white symbol.]
  ]
  
  #fire-sign(2, height: 2cm)
  [
    #text(weight: "bold")[Fire Sign 2 (F002)]
    #linebreak()
    #text(style: "italic")[Fire hose reel]
    #linebreak()
    #v(4pt)
    #text(size: 9pt)[Indicates location of fire hose reel. Use to mark fire hose storage.]
  ]
]

=== Emergency Signs (Green Square)

#grid(
  columns: (2fr, 3fr),
  column-gutter: 16pt,
  row-gutter: 12pt,
  align: center,
)[
  #emergency-sign(1, height: 2cm)
  [
    #text(weight: "bold")[Emergency Sign 1 (E001/E002)]
    #linebreak()
    #text(style: "italic")[Emergency exit]
    #linebreak()
    #v(4pt)
    #text(size: 9pt)[Indicates emergency exit or escape route. Green square with white symbol.]
  ]
  
  #emergency-sign(2, height: 2cm)
  [
    #text(weight: "bold")[Emergency Sign 2 (E003)]
    #linebreak()
    #text(style: "italic")[First aid]
    #linebreak()
    #v(4pt)
    #text(size: 9pt)[Indicates location of first aid equipment or station.]
  ]
]

#v(1cm)

== Best Practices

=== Symbol Sizing

Use appropriate sizes for context:

#block(
  fill: code-bg,
  stroke: primary-blue,
  radius: 4pt,
  inset: 12pt,
  width: 100%,
)[
  #text(weight: "bold")[Size Recommendations:]
  #v(6pt)
  #text[
    • Inline text: `height: 1em` (matches text size)
    #linebreak()
    • Small displays: `height: 1cm` to `2cm`
    #linebreak()
    • Standard signs: `height: 3cm` to `5cm`
    #linebreak()
    • Large displays: `height: 10cm` or larger
  ]
]

=== Consistency

Use consistent sizes for the same type of symbol throughout your document:

```typst
// Good: Consistent sizing
#warning-sign(1, height: 2cm)
#warning-sign(3, height: 2cm)
#warning-sign(5, height: 2cm)
```

=== Context and Labels

Always provide context or labels when the meaning might not be immediately clear:

```typst
// Good: With label
#grid(
  columns: (1fr, 2fr),
  align: center,
)[
  #emergency-sign(1, height: 2cm),
  [*Emergency Exit* - Use in case of emergency],
]
```

=== Integration with WAFT

In WAFT projects, consider:
- Adding symbols to document headers/footers
- Creating dedicated safety sections
- Including symbols in procedural documents
- Adding to facility maps and layouts

#v(1cm)

== WAFT Integration Examples

=== Example 1: Safety Information Panel

```python
from pathlib import Path
from src.waft.templates.typst.wrappers.worldbuild_iso import generate_worldbuild_iso

safety_symbols = [
    {
        "function": "warning-sign",
        "code": 3,
        "label": "Electrical Hazard",
        "description": "High voltage equipment. Do not touch."
    },
    {
        "function": "fire-sign",
        "code": 1,
        "label": "Fire Extinguisher",
        "description": "Located 10 meters to your right."
    },
    {
        "function": "emergency-sign",
        "code": 1,
        "label": "Emergency Exit",
        "description": "Use in case of emergency."
    }
]

generate_worldbuild_iso(
    title="Facility Safety Information",
    content="Your content here...",
    output_path=Path("output/safety_panel.pdf"),
    doc_id="SAFETY-001",
    safety_symbols=safety_symbols
)
```

=== Example 2: Custom Typst Template

You can use symbols in any custom Typst template:

```typst
#import "@preview/typsium-iso-7010:0.1.0": *

= Laboratory Safety Guide

== Hazard Identification

#grid(
  columns: 2,
  column-gutter: 16pt,
  row-gutter: 12pt,
)[
  #warning-sign(3, height: 3cm),
  [
    *Electrical Hazard*
    #linebreak()
    High voltage equipment. Do not touch.
  ],
  #fire-sign(1, height: 3cm),
  [
    *Fire Extinguisher*
    #linebreak()
    Located at each exit.
  ],
]
```

#v(1cm)

== Troubleshooting

=== Symbol Not Displaying

#text(weight: "bold")[Problem:] Symbol doesn't appear in compiled PDF.

#text(weight: "bold")[Solutions:]
1. Check import statement is at top: `#import "@preview/typsium-iso-7010:0.1.0": *`
2. Verify symbol number exists (try `#warning-sign(1, height: 2cm)` first)
3. Check for syntax errors (missing commas, etc.)

=== Wrong Symbol Appearing

#text(weight: "bold")[Problem:] Symbol number doesn't match expected ISO code.

#text(weight: "bold")[Solution:] Package uses numeric indices (1, 2, 3...) not ISO codes (W001, F001, etc.). Test different numbers to find the right symbol.

=== Size Issues

#text(weight: "bold")[Problem:] Symbol too large or too small.

#text(weight: "bold")[Solution:] Adjust the `height` parameter:
- Too small? Increase: `height: 5cm`
- Too large? Decrease: `height: 1cm`
- Inline? Match text: `height: 1em`

#v(1cm)

== Quick Reference

=== Import
```typst
#import "@preview/typsium-iso-7010:0.1.0": *
```

=== Warning Signs
```typst
#warning-sign(1, height: 2cm)  // General warning
#warning-sign(3, height: 2cm)  // Electric shock
#warning-sign(5, height: 2cm)  // Biological hazard
```

=== Fire Signs
```typst
#fire-sign(1, height: 2cm)     // Fire extinguisher
#fire-sign(2, height: 2cm)     // Fire hose reel
```

=== Emergency Signs
```typst
#emergency-sign(1, height: 2cm) // Emergency exit
#emergency-sign(2, height: 2cm) // First aid
#emergency-sign(3, height: 2cm) // Emergency telephone
```

=== Arrows
```typst
#emergency-arrow(direction: "right", height: 2cm)
#fire-arrow(direction: "up", height: 2cm)
```

#v(1cm)

== Additional Resources

#block(
  fill: rgb("#e8f5e9"),
  stroke: safety-green,
  radius: 4pt,
  inset: 12pt,
  width: 100%,
)[
  #text(weight: "bold", fill: safety-green)[Reference Materials]
  #v(6pt)
  #text[
    • WAFT Functions: `src/waft/templates/typst/wrappers/worldbuild_iso.py`
    #linebreak()
    • Symbol Guide: `NARRATIVE-WAFT/ISO_7010_SYMBOLS_GUIDE.pdf`
    #linebreak()
    • Markdown Guide: `docs/WAFT_ISO_7010_USAGE_GUIDE.md`
    #linebreak()
    • Package: `@preview/typsium-iso-7010:0.1.0`
    #linebreak()
    • Standard: ISO 7010:2019
    #linebreak()
    • Wikipedia: https://en.wikipedia.org/wiki/ISO_7010
  ]
]

#v(2cm)

#align(center)[
  #text(size: 10pt, style: "italic", fill: primary-blue)[
    WAFT Project - ISO 7010 Integration Guide
    #linebreak()
    Last updated: January 2026
  ]
]
