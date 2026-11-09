// WAFT Framework: Evidence-Backed Technical Analysis
// MAIN COMPILATION FILE
// Professional Academic Publication System
// Style: Clean, Feature-Rich, No Color

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
  size: 12pt,
  fill: black,
  hyphenate: true,
)

#set par(
  justify: true,
  leading: 0.65em,
  spacing: 1.2em,
  first-line-indent: 1.5em,
)

#set heading(
  numbering: "1.1",
)

// ============================================================================
// TYPOGRAPHY ENHANCEMENTS
// ============================================================================

// Strong emphasis with small caps
#show strong: set text(weight: "semibold")

// Emphasis styling
#show emph: set text(style: "italic")

// Superscript/subscript
#set super(typographic: true)
#set sub(typographic: true)

// Smart quotes
#set smartquote(enabled: true)

// ============================================================================
// CODE BLOCK STYLING - Clean with line numbers
// ============================================================================

#show raw.where(block: true): it => {
  set text(font: "JetBrains Mono", size: 9pt, fill: black)
  set par(justify: false, leading: 0.5em)

  block(
    fill: luma(248),
    stroke: (left: 3pt + luma(180)),
    inset: (left: 16pt, top: 12pt, bottom: 12pt, right: 12pt),
    radius: 0pt,
    width: 100%,
    breakable: true,
    {
      // Add line numbers
      let lines = it.text.split("\n")
      let digits = str(lines.len()).len()
      for (i, line) in lines.enumerate() {
        let num = str(i + 1)
        text(fill: luma(160), size: 8pt)[#(" " * (digits - num.len()))#num ]
        text(fill: black)[#line]
        if i < lines.len() - 1 { linebreak() }
      }
    }
  )
}

#show raw.where(block: false): it => {
  box(
    fill: luma(245),
    outset: (x: 2pt, y: 2pt),
    radius: 2pt,
    text(font: "JetBrains Mono", size: 10pt, fill: black, it)
  )
}

// ============================================================================
// HEADING STYLING - Clean Academic
// ============================================================================

// Level 1: Chapter headings
#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  v(0.5in)
  block(
    width: 100%,
    below: 0.4in,
    {
      text(size: 11pt, weight: "regular", tracking: 0.1em, upper(
        [Chapter #counter(heading).display("1")]
      ))
      v(0.15in)
      line(length: 100%, stroke: 1.5pt + black)
      v(0.15in)
      text(size: 22pt, weight: "bold", it.body)
      v(0.05in)
      line(length: 2in, stroke: 0.75pt + black)
    }
  )
}

// Level 2: Section headings
#show heading.where(level: 2): it => {
  v(0.35in)
  block(
    width: 100%,
    above: 0.3in,
    below: 0.2in,
    {
      text(size: 14pt, weight: "bold")[
        #counter(heading).display("1.1") #h(0.5em) #it.body
      ]
      v(0.08in)
      line(length: 100%, stroke: 0.5pt + luma(120))
    }
  )
}

// Level 3: Subsection headings
#show heading.where(level: 3): it => {
  v(0.25in)
  block(
    width: 100%,
    above: 0.2in,
    below: 0.15in,
    text(size: 12pt, weight: "bold")[
      #counter(heading).display("1.1.1") #h(0.4em) #it.body
    ]
  )
}

// Level 4: Paragraph headings
#show heading.where(level: 4): it => {
  v(0.15in)
  text(size: 11pt, weight: "bold", style: "italic")[#it.body.]
  h(0.5em)
}

// ============================================================================
// FIGURE STYLING - Clean Academic
// ============================================================================

#show figure: it => {
  set align(center)
  v(0.25in)
  block(
    width: 100%,
    breakable: false,
    {
      it.body
      v(0.12in)
      text(size: 10pt)[
        #text(weight: "bold")[#it.supplement #it.counter.display().]
        #h(0.3em)
        #it.caption.body
      ]
    }
  )
  v(0.25in)
}

// ============================================================================
// TABLE STYLING - Professional
// ============================================================================

#set table(
  stroke: none,
  inset: 8pt,
  align: left,
)

#show table: it => {
  set align(center)
  v(0.2in)
  block(width: 100%, {
    // Add horizontal rules for academic style
    set table(
      stroke: (x, y) => (
        top: if y == 0 { 1.5pt + black } else if y == 1 { 0.75pt + black } else { none },
        bottom: 1.5pt + black,
      )
    )
    it
  })
  v(0.2in)
}

// ============================================================================
// QUOTE STYLING - Academic Block Quotes
// ============================================================================

#show quote: it => {
  set par(first-line-indent: 0pt)
  v(0.15in)
  block(
    inset: (left: 2em, right: 1em, top: 0.5em, bottom: 0.5em),
    stroke: (left: 2pt + luma(160)),
    {
      text(style: "italic", it.body)
      if it.attribution != none {
        v(0.3em)
        align(right, text(size: 10pt)[— #it.attribution])
      }
    }
  )
  v(0.15in)
}

// ============================================================================
// LINK STYLING - Subtle
// ============================================================================

#show link: it => {
  text(fill: black, it)
  // Add subtle underline for external links
  if type(it.dest) == str {
    text(size: 8pt, baseline: -0.5pt)[↗]
  }
}

// ============================================================================
// FOOTNOTE STYLING
// ============================================================================

#set footnote.entry(
  separator: line(length: 30%, stroke: 0.5pt + luma(150)),
  indent: 0.5em,
  gap: 0.5em,
)

#show footnote.entry: it => {
  set text(size: 9pt)
  it
}

// ============================================================================
// OUTLINE STYLING - Table of Contents
// ============================================================================

#show outline.entry.where(level: 1): it => {
  v(0.4em, weak: true)
  strong(it)
}

// ============================================================================
// MATH STYLING
// ============================================================================

#set math.equation(
  numbering: "(1)",
  supplement: [Equation],
)

// ============================================================================
// LIST STYLING
// ============================================================================

#set enum(
  indent: 1.5em,
  body-indent: 0.5em,
  numbering: "1.a.i.",
)

#set list(
  indent: 1.5em,
  body-indent: 0.5em,
  marker: ([•], [◦], [▪]),
)

// ============================================================================
// IMPORT CUSTOM FUNCTIONS
// ============================================================================

#import "waft_functions.typ": callout, evidence, metric, definition, theorem, note, sidebar

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
    #line(length: 100%, stroke: 0.5pt + luma(180))
    #v(0.05in)
    #align(center)[
      #text(size: 10pt, fill: luma(100))[
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

// Technical Whitepaper (NEW - Academic deep-dive)
#include "sections/03_technical_whitepaper.typ"

// Breeding AI Introduction (NEW - Narrative intro)
#include "sections/05_breeding_ai_intro.typ"

// Table of Contents (auto-generated)
#pagebreak()
#outline(
  title: [Table of Contents],
  depth: 3,
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
  header: context {
    if counter(page).get().first() > 0 {
      text(size: 9pt, fill: luma(80))[
        #smallcaps[WAFT Framework: Evidence-Backed Technical Analysis]
        #h(1fr)
        #counter(page).display("1")
      ]
      v(0.05in)
      line(length: 100%, stroke: 0.5pt + luma(180))
    }
  },
  footer: context [
    #line(length: 100%, stroke: 0.5pt + luma(180))
    #v(0.05in)
    #align(center)[
      #text(size: 9pt, fill: luma(120), style: "italic")[
        Dr. Aria Vex #h(1em) | #h(1em) January 24, 2026
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

// Chapter 4: Scint Gym - Deep Dive (pages 14-28)
#include "sections/40_scint_gym.typ"

// Chapter 5: Genome Evolution System (pages 29-37)
#include "sections/50_genome_evolution.typ"

// Chapter 7: Scientist God - Research Management (pages 38-43)
#include "sections/70_scientist_god.typ"

// Chapter 8: Pantheon Architecture (pages 44-52)
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

// Study Guide (NEW - Educational materials)
#include "sections/E0_study_guide.typ"

// Project Proposal (NEW - Research justification)
#include "sections/F0_project_proposal.typ"

// Index
#include "sections/D2_index.typ"

// ============================================================================
// FINAL PAGE
// ============================================================================

#include "WAFT_FINAL_PAGE.typ"
