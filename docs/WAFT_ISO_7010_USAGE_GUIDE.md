# WAFT ISO 7010 Safety Symbols Usage Guide

Complete guide for using ISO 7010 safety symbols in WAFT Typst documents.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Using WAFT Wrapper Functions](#using-waft-wrapper-functions)
3. [Direct Typst Usage](#direct-typst-usage)
4. [Symbol Reference](#symbol-reference)
5. [Integration Examples](#integration-examples)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Installation

The `typsium-iso-7010` package is automatically available in WAFT Typst documents. No installation needed - just import it:

```typst
#import "@preview/typsium-iso-7010:0.1.0": *
```

### Basic Usage

```typst
// In any Typst document
#warning-sign(1, height: 2cm)
#fire-sign(1, height: 2cm)
#emergency-sign(1, height: 2cm)
```

---

## Using WAFT Wrapper Functions

WAFT provides convenient Python functions for generating documents with ISO 7010 symbols.

### Method 1: Using `generate_worldbuild_iso()`

The most flexible method - full control over symbol placement:

```python
from pathlib import Path
from src.waft.templates.typst.wrappers.worldbuild_iso import generate_worldbuild_iso

# Define your symbols
safety_symbols = [
    {
        "function": "warning-sign",
        "code": 3,  # Electric shock (W012 in ISO 7010)
        "label": "Electrical Hazard",
        "description": "High voltage equipment. Do not touch."
    },
    {
        "function": "fire-sign",
        "code": 1,  # Fire extinguisher (F001)
        "label": "Fire Extinguisher",
        "description": "Located 10 meters to your right."
    },
    {
        "function": "emergency-sign",
        "code": 1,  # Emergency exit (E001/E002)
        "label": "Emergency Exit",
        "description": "Use in case of emergency."
    }
]

# Generate document
pdf_path = generate_worldbuild_iso(
    title="Safety Information",
    content="Your document content here...",
    output_path=Path("output/safety_info.pdf"),
    doc_id="SAFETY-001",
    safety_symbols=safety_symbols,
    classification="INTERNAL"
)
```

### Method 2: Using `generate_worldbuild_with_symbols()`

Simpler method using predefined symbol names:

```python
from pathlib import Path
from src.waft.templates.typst.wrappers.worldbuild_iso import generate_worldbuild_with_symbols

# Use predefined symbol names
pdf_path = generate_worldbuild_with_symbols(
    title="Laboratory Safety Guide",
    content="Your content here...",
    output_path=Path("output/lab_safety.pdf"),
    symbols=["warning", "electric", "fire", "emergency", "first_aid"],
    doc_id="LAB-SAFETY-001"
)
```

**Available predefined symbols:**
- `"warning"` - General warning (W001)
- `"danger"` - Danger (W002)
- `"electric"` - Electric shock (W012)
- `"radiation"` - Ionizing radiation (W003)
- `"biohazard"` - Biological hazard (W009)
- `"fire"` - Fire extinguisher (F001)
- `"emergency"` - Emergency exit (E001)
- `"first_aid"` - First aid (E003)

---

## Direct Typst Usage

For custom Typst templates, use symbols directly in your `.typ` files.

### Import Statement

Always import at the top of your Typst file:

```typst
#import "@preview/typsium-iso-7010:0.1.0": *
```

### Basic Symbol Functions

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

### Common Patterns

#### Inline with Text

```typst
#warning-sign(3, height: 1em) indicates electrical hazards in this area.
```

#### In Grids

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

#### With Labels

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

#### With Directional Arrows

```typst
#grid(
  columns: 2,
  align: center,
)[
  #emergency-sign(1, height: 2cm),
  #emergency-arrow(direction: "right", height: 2cm),
]
```

---

## Symbol Reference

### Warning Signs (Yellow Triangle)

| Package Index | ISO Code | Description | Usage |
|--------------|----------|-------------|-------|
| 1 | W001 | General warning | General hazard warning |
| 2 | W002 | Explosive material | Explosives storage/handling |
| 3 | W003 | Radioactive material | Radiation areas |
| 4 | W004 | Laser beam | Laser equipment |
| 5 | W009 | Biological hazard | Biohazard areas |

**Function:** `#warning-sign(n, height: <size>)`

### Fire Signs (Red Square)

| Package Index | ISO Code | Description | Usage |
|--------------|----------|-------------|-------|
| 1 | F001 | Fire extinguisher | Fire extinguisher location |
| 2 | F002 | Fire hose reel | Fire hose location |
| 3 | F003 | Fire ladder | Fire ladder location |
| 4 | F004 | Collection of firefighting equipment | Fire equipment storage |
| 5 | F005 | Fire alarm call point | Fire alarm location |

**Function:** `#fire-sign(n, height: <size>)`

### Emergency Signs (Green Square)

| Package Index | ISO Code | Description | Usage |
|--------------|----------|-------------|-------|
| 1 | E001/E002 | Emergency exit (left/right) | Emergency exits |
| 2 | E003 | First aid | First aid stations |
| 3 | E004 | Emergency telephone | Emergency phones |
| 4 | E011 | Eyewash station | Eyewash equipment |
| 5 | E012 | Safety shower | Emergency showers |

**Function:** `#emergency-sign(n, height: <size>)`

### Directional Arrows

**Emergency Arrows:**
```typst
#emergency-arrow(direction: "up", height: 2cm)
#emergency-arrow(direction: "down", height: 2cm)
#emergency-arrow(direction: "left", height: 2cm)
#emergency-arrow(direction: "right", height: 2cm)
```

**Fire Arrows:**
```typst
#fire-arrow(direction: "up", height: 2cm)
#fire-arrow(direction: "down", height: 2cm)
#fire-arrow(direction: "left", height: 2cm)
#fire-arrow(direction: "right", height: 2cm)
```

---

## Integration Examples

### Example 1: Safety Information Panel

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

content = """
== Safety Procedures

Follow these procedures in case of emergency:

1. Evacuate immediately using the marked emergency exits
2. Do not use elevators
3. Report to the assembly point
4. Wait for further instructions
"""

generate_worldbuild_iso(
    title="Facility Safety Information",
    content=content,
    output_path=Path("output/safety_panel.pdf"),
    doc_id="SAFETY-001",
    safety_symbols=safety_symbols
)
```

### Example 2: Custom Typst Template

```typst
#import "@preview/typsium-iso-7010:0.1.0": *
#import "@preview/s6t5-page-bordering:1.0.0": s6t5-page-bordering

#set page(margin: 1in)
#set text(size: 11pt)

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
  #warning-sign(5, height: 3cm),
  [
    *Biological Hazard*
    #linebreak()
    Biohazard materials present. Use proper PPE.
  ],
  #fire-sign(1, height: 3cm),
  [
    *Fire Extinguisher*
    #linebreak()
    Located at each exit.
  ],
  #emergency-sign(2, height: 3cm),
  [
    *First Aid Station*
    #linebreak()
    Room 101, first floor.
  ],
]

== Emergency Procedures

#emergency-sign(1, height: 2cm) #emergency-arrow(direction: "right", height: 2cm) #emergency-arrow(direction: "right", height: 2cm) #emergency-sign(1, height: 2cm)

Follow the emergency exit signs to evacuate safely.
```

### Example 3: Integration with WAFT Templates

You can combine ISO 7010 symbols with other WAFT Typst templates:

```python
from src.waft.templates.typst.wrappers.worldbuild_iso import generate_worldbuild_iso
from src.waft.templates.typst.wrappers.worldbuild_yagenda import generate_worldbuild_agenda

# Create agenda with safety symbols
agenda_content = generate_worldbuild_agenda(
    # ... agenda parameters
)

# Add safety symbols to the document
generate_worldbuild_iso(
    title="Meeting Agenda - Safety Briefing",
    content=agenda_content,
    output_path=Path("output/safety_meeting.pdf"),
    safety_symbols=[
        {"function": "warning-sign", "code": 1, "label": "General Warning", "description": "Please review safety procedures"},
        {"function": "emergency-sign", "code": 1, "label": "Emergency Exits", "description": "Know your nearest exit"}
    ]
)
```

---

## Best Practices

### 1. Symbol Sizing

Use appropriate sizes for context:

- **Inline text:** `height: 1em` (matches text size)
- **Small displays:** `height: 1cm` to `2cm`
- **Standard signs:** `height: 3cm` to `5cm`
- **Large displays:** `height: 10cm` or larger

### 2. Consistency

Use consistent sizes for the same type of symbol throughout your document:

```typst
// Good: Consistent sizing
#warning-sign(1, height: 2cm)
#warning-sign(3, height: 2cm)
#warning-sign(5, height: 2cm)

// Bad: Inconsistent sizing
#warning-sign(1, height: 1cm)
#warning-sign(3, height: 5cm)
#warning-sign(5, height: 2.5cm)
```

### 3. Context and Labels

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

// Bad: Symbol alone (may be unclear)
#emergency-sign(1, height: 2cm)
```

### 4. Placement

Place symbols where they are clearly visible and not obstructed. In WAFT documents, consider:

- Adding symbols to document headers/footers
- Creating dedicated safety sections
- Including symbols in procedural documents
- Adding to facility maps and layouts

### 5. Standards Compliance

Follow ISO 7010 guidelines:
- Use correct colors (yellow for warnings, red for fire, green for emergency)
- Maintain proper shapes (triangle for warnings, square for fire/emergency)
- Provide appropriate sizing for visibility
- Include text labels when necessary

---

## Troubleshooting

### Symbol Not Displaying

**Problem:** Symbol doesn't appear in compiled PDF.

**Solutions:**
1. Check that the import statement is at the top of your file:
   ```typst
   #import "@preview/typsium-iso-7010:0.1.0": *
   ```

2. Verify the symbol number exists in the package:
   - Try `#warning-sign(1, height: 2cm)` first (most common symbols)
   - Check package documentation for available symbols

3. Check for syntax errors:
   ```typst
   // Correct
   #warning-sign(1, height: 2cm)
   
   // Incorrect (missing comma)
   #warning-sign(1 height: 2cm)
   ```

### Wrong Symbol Appearing

**Problem:** Symbol number doesn't match expected ISO code.

**Solution:** The package uses numeric indices (1, 2, 3...) not ISO codes (W001, F001, etc.). You may need to test which number corresponds to which symbol:

```typst
// Test different numbers to find the right symbol
#warning-sign(1, height: 2cm)  // Try 1
#warning-sign(2, height: 2cm)  // Try 2
#warning-sign(3, height: 2cm)  // Try 3
```

### Size Issues

**Problem:** Symbol is too large or too small.

**Solution:** Adjust the `height` parameter:

```typst
// Too small? Increase height
#warning-sign(1, height: 5cm)

// Too large? Decrease height
#warning-sign(1, height: 1cm)

// For inline use, match text size
#warning-sign(1, height: 1em)
```

### Package Not Found

**Problem:** Typst can't find the package.

**Solution:** Ensure you're using the correct package name and version:

```typst
// Correct
#import "@preview/typsium-iso-7010:0.1.0": *

// Incorrect (wrong version or name)
#import "@preview/typsium-iso-7010:1.0.0": *
#import "@preview/iso-7010:0.1.0": *
```

---

## Advanced Usage

### Creating Custom Symbol Functions

You can create reusable symbol functions in your Typst templates:

```typst
#import "@preview/typsium-iso-7010:0.1.0": *

#let safety-panel(
  symbol-type: "warning",
  code: 1,
  label: none,
  description: none,
) = {
  let symbol = if symbol-type == "warning" {
    warning-sign(code, height: 2cm)
  } else if symbol-type == "fire" {
    fire-sign(code, height: 2cm)
  } else {
    emergency-sign(code, height: 2cm)
  }
  
  grid(
    columns: (1fr, 2fr),
    align: center,
  )[
    symbol,
    [
      if label != none [*#label*]
      if description != none [#description]
    ],
  ]
}

// Usage
#safety-panel(symbol-type: "warning", code: 3, label: "Electrical Hazard", description: "High voltage area")
```

### Combining with WAFT Templates

ISO 7010 symbols work with all WAFT Typst templates. You can add them to:

- Worldbuilding documents
- Campaign books
- Scientific papers
- Business reports
- Any custom Typst template

Just import the package and use the symbols anywhere in your Typst content.

---

## Reference

- **Package:** `@preview/typsium-iso-7010:0.1.0`
- **Standard:** ISO 7010:2019
- **WAFT Functions:** `src/waft/templates/typst/wrappers/worldbuild_iso.py`
- **Symbol Guide:** `NARRATIVE-WAFT/ISO_7010_SYMBOLS_GUIDE.pdf`
- **Wikipedia Reference:** https://en.wikipedia.org/wiki/ISO_7010
- **ISO Standard:** https://www.iso.org/standard/72424.html

---

## Quick Reference Card

```typst
// Import (always at top)
#import "@preview/typsium-iso-7010:0.1.0": *

// Warning signs (yellow triangle)
#warning-sign(1, height: 2cm)  // General warning
#warning-sign(3, height: 2cm)  // Electric shock
#warning-sign(5, height: 2cm)  // Biological hazard

// Fire signs (red square)
#fire-sign(1, height: 2cm)     // Fire extinguisher
#fire-sign(2, height: 2cm)     // Fire hose reel

// Emergency signs (green square)
#emergency-sign(1, height: 2cm) // Emergency exit
#emergency-sign(2, height: 2cm) // First aid
#emergency-sign(3, height: 2cm) // Emergency telephone

// Arrows
#emergency-arrow(direction: "right", height: 2cm)
#fire-arrow(direction: "up", height: 2cm)
```

---

*Last updated: January 2026*
*WAFT Project - ISO 7010 Integration Guide*
