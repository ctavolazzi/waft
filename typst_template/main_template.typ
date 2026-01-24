// WAFT Framework: Evidence-Backed Technical Analysis
// MAIN COMPILATION FILE
// Professional Publication System

#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge
#import "@preview/tablex:0.0.9": tablex, cellx, rowspanx, colspanx

// ============================================================================
// GLOBAL SETTINGS
// ============================================================================

#set document(
  title: "WAFT Framework: Evidence-Backed Technical Analysis",
  author: "Dr. Aria Vex",
  date: datetime(year: 2026, month: 1, day: 24),
  keywords: ("WAFT", "AI Agents", "Self-Modifying", "Evolutionary", "Framework"),
)

#set page(
  paper: "us-letter",
  margin: (
    top: 1in,
    bottom: 1in,
    left: 1.25in,
    right: 1.25in,
  ),
)

#set text(
  font: "New Computer Modern",
  size: 11pt,
  fill: rgb("#333333"),
  hyphenate: true,
)

#set par(
  justify: true,
  leading: 0.65em,
  spacing: 1em,
)

#set heading(
  numbering: "1.1",
)

// Code block styling
#show raw.where(block: true): it => {
  set text(font: "JetBrains Mono", size: 9pt)
  block(
    fill: rgb("#f5f5f5"),
    stroke: 1pt + rgb("#cccccc"),
    radius: 4pt,
    inset: 12pt,
    width: 100%,
    it
  )
}

#show raw.where(block: false): it => {
  box(
    fill: rgb("#f0f0f0"),
    outset: (x: 3pt, y: 2pt),
    radius: 2pt,
    text(font: "JetBrains Mono", size: 10pt, it)
  )
}

// Heading styling
#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  block(
    width: 100%,
    fill: rgb("#1976d2"),
    inset: 16pt,
    radius: 4pt,
    text(fill: white, size: 20pt, weight: "bold", it.body)
  )
  v(0.3in)
}

#show heading.where(level: 2): it => {
  v(0.2in)
  block(
    width: 100%,
    above: 0.3in,
    below: 0.2in,
    text(fill: rgb("#1976d2"), size: 16pt, weight: "bold")[
      #counter(heading).display() #it.body
    ]
  )
  line(length: 100%, stroke: 2pt + rgb("#1976d2"))
  v(0.1in)
}

// Figure styling
#show figure: it => {
  set align(center)
  v(0.2in)
  block(
    stroke: 1pt + rgb("#cccccc"),
    radius: 4pt,
    inset: 12pt,
    width: 100%,
    [
      #it.body
      #v(0.1in)
      #text(size: 10pt, style: "italic", fill: rgb("#666666"))[
        #it.caption
      ]
    ]
  )
  v(0.2in)
}

// Table styling
#show table: it => {
  set align(center)
  v(0.2in)
  block(
    width: 100%,
    it
  )
  v(0.2in)
}

// Link styling
#show link: it => {
  text(fill: rgb("#1976d2"), underline: true, it)
}

// ============================================================================
// IMPORT CUSTOM FUNCTIONS
// ============================================================================

#import "waft_functions.typ": callout, evidence, metric

// ============================================================================
// COVER PAGE
// ============================================================================

#include "WAFT_COVER_PAGE.typ"

// ============================================================================
// FRONT MATTER (Roman numerals)
// ============================================================================

#set page(
  numbering: "i",
  header: none,
  footer: context [
    #line(length: 100%, stroke: 0.5pt + rgb("#cccccc"))
    #v(0.05in)
    #align(center)[
      #text(size: 10pt, fill: rgb("#666666"))[
        Page #counter(page).display("i")
      ]
    ]
  ],
)

#counter(page).update(1)

// Title Page
#include "sections/00_title_page.typ"

// Abstract
#include "sections/01_abstract.typ"

// Executive Summary
#include "sections/02_executive_summary.typ"

// Table of Contents (auto-generated)
#pagebreak()
#outline(
  title: [Table of Contents],
  depth: 2,
  indent: auto,
)

// List of Figures
#pagebreak()
#outline(
  title: [List of Figures],
  target: figure.where(kind: image),
)

// List of Tables
#pagebreak()
#outline(
  title: [List of Tables],
  target: figure.where(kind: table),
)

// List of Code Listings
#pagebreak()
#outline(
  title: [List of Code Listings],
  target: figure.where(kind: raw),
)

// ============================================================================
// MAIN BODY (Arabic numerals)
// ============================================================================

#set page(
  numbering: "1",
  header: context [
    #text(size: 10pt, fill: rgb("#666666"))[
      WAFT Framework: Evidence-Backed Technical Analysis
      #h(1fr)
      #counter(page).display("1")
    ]
    #v(0.05in)
    #line(length: 100%, stroke: 0.5pt + rgb("#cccccc"))
  ],
  footer: context [
    #line(length: 100%, stroke: 0.5pt + rgb("#cccccc"))
    #v(0.05in)
    #align(center)[
      #text(size: 9pt, fill: rgb("#999999"), style: "italic")[
        Dr. Aria Vex | January 24, 2026
      ]
    ]
  ],
)

#counter(page).update(1)

// Chapter 1: Introduction (pages 1-4)
#include "sections/10_introduction.typ"

// Chapter 2: Methodology (pages 5-8)
#include "sections/20_methodology.typ"

// Chapter 3: Core Claims Analysis (pages 9-13)
#include "sections/30_core_claims.typ"

// Chapter 4: Scint Gym - Deep Dive (pages 14-28) ⭐ NEXT TO WRITE
#include "sections/40_scint_gym.typ"

// Chapter 5: Genome Evolution System (pages 29-37)
#include "sections/50_genome_evolution.typ"

// Chapter 6: Pantheon Architecture (pages 38-43)
#include "sections/60_pantheon.typ"

// Chapter 7: Narrative/Gamification (pages 44-51)
#include "sections/70_narrative.typ"

// Chapter 8: Empirica Integration (pages 52-55)
#include "sections/80_empirica.typ"

// Chapter 9: Documentation Quality (pages 56-58)
#include "sections/90_documentation.typ"

// Chapter 10: Implementation Gaps (pages 59-63)
#include "sections/A0_gaps.typ"

// Chapter 11: Final Assessment (pages 64-65)
#include "sections/B0_assessment.typ"

// ============================================================================
// BACK MATTER
// ============================================================================

#set page(
  numbering: "1",
  header: none,
)

// Appendix A: Full Test Output
#include "sections/C0_appendix_tests.typ"

// Appendix B: Telemetry Data
#include "sections/C1_appendix_telemetry.typ"

// Appendix C: Directory Structure
#include "sections/C2_appendix_structure.typ"

// References
#include "sections/D0_references.typ"

// Glossary
#include "sections/D1_glossary.typ"

// Index
#include "sections/D2_index.typ"

// ============================================================================
// FINAL PAGE
// ============================================================================

#include "WAFT_FINAL_PAGE.typ"
