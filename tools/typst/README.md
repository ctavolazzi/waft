# DIALECTIC Typst Tools

Reusable Typst templates and components for the DIALECTIC Engine and other WAFT projects.

## Overview

These tools provide consistent styling for:
- Scientific reports
- Phase reports (Thesis/Antithesis/Synthesis)
- SITREP documents
- General DIALECTIC documents

## Files

### `scientific_base.typ`
Foundation for scientific/research-style reports.

```typst
#import "scientific_base.typ": scientific-doc, callout, code-block, data-table

#show: scientific-doc.with(
  title: "My Research Report",
  authors: ("Author Name",),
  abstract: [This is the abstract...],
  keywords: ("keyword1", "keyword2"),
)

// Your content here
```

### `phase_report.typ`
Templates for DIALECTIC phase reports.

```typst
#import "phase_report.typ": phase-report, thesis-header, evidence-block, progress-indicator

#show: phase-report.with(
  phase: "thesis",
  title: "Assembly Report",
)

#thesis-header()

#evidence-block("proven")[
  This assumption was validated.
]
```

### `sitrep_template.typ`
Military-style SITREP (Situation Report) template.

```typst
#import "sitrep_template.typ": sitrep-doc, sitrep-section, status-indicator, action-item

#show: sitrep-doc.with(
  dtg: "211200Z JAN 2026",
  classification: "UNCLASSIFIED",
)

#sitrep-section(1, "Situation")[
  Current operational status...
]
```

### `dialectic_components.typ`
Shared components following the ODD Realm pattern.

```typst
#import "dialectic_components.typ": *

#thesis-callout[
  This is a thesis-related note.
]

#verification-badge("proven")

#phase-transition("thesis", "antithesis")
```

## Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Thesis Blue | `#1f6feb` | Assembly phase |
| Antithesis Red | `#da3633` | Sanity check phase |
| Synthesis Purple | `#a371f7` | Problem description phase |
| Success Green | `#3fb950` | Proven/complete |
| Warning Orange | `#f0883e` | In progress/unknown |
| Error Red | `#f85149` | Refuted/failed |

## Philosophy

These tools implement the Hegelian dialectical method:

1. **Thesis (Assembly)**: Gather context and establish propositions
2. **Antithesis (Sanity Check)**: Challenge assumptions and validate
3. **Synthesis (Problem Description)**: Resolve and generate conclusions

> "The truth is the whole." - G.W.F. Hegel

## Requirements

- Typst CLI (`cargo install typst-cli`)
- Font: New Computer Modern (included with Typst)

## Integration

These tools are used by the DIALECTIC Engine (`waft dialectic`) to generate PDF reports. They can also be used standalone for any Typst document.

## Related

- DIALECTIC Engine: `src/waft/core/dialectic/`
- DIALECTIC Realm: `_realms/dialectic_realm/`
- ODD Realm Components: `_realms/odd_realm/templates/odd_components.typ`
