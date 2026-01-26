// WAFT White Paper Template
// Professional, toner-friendly, minimal black & white design
// Optimized for high text density and minimal ink usage

#let waft-whitepaper(
  title: "WAFT White Paper",
  subtitle: none,
  authors: (),
  date: datetime.today(),
  abstract: [],
  keywords: (),
  doc,
) = [
  // ============================================================================
  // PAGE SETUP - Optimized margins for maximum text area
  // ============================================================================

  #set page(
    paper: "us-letter",
    margin: (
      top: 0.75in,
      bottom: 0.75in,
      left: 1in,
      right: 1in,
    ),
  )

  // ============================================================================
  // TYPOGRAPHY - Clean, readable, dense
  // ============================================================================

  #set text(
    font: "Times New Roman",
    size: 10pt,
    fill: black,
    hyphenate: true,
  )

  #set par(
    justify: true,
    leading: 0.15em,
    spacing: 0.5em,
  )

  #set heading(
    numbering: "1.1",
  )

  // ============================================================================
  // CODE BLOCK STYLING - Minimal ink, maximum readability
  // ============================================================================

  #show raw.where(block: true): it => {
    set text(font: "Courier New", size: 8.5pt)
    block(
      fill: white,
      stroke: 0.5pt + black,
      radius: 0pt,
      inset: 8pt,
      width: 100%,
      it
    )
  }

  #show raw.where(block: false): it => {
    text(font: "Courier New", size: 9pt, it)
  }

  // ============================================================================
  // TABLE STYLING - Minimal borders, maximum density
  // ============================================================================

  #show table: it => {
    set align(center)
    v(0.1in)
    block(
      width: 100%,
      it
    )
    v(0.1in)
  }

  #show table.cell.where(kind: header): it => {
    set text(weight: "bold", size: 10pt)
    set fill(black)
    set align(center)
    set stroke(bottom: 0.5pt + black)
    it
  }

  #show table.cell: it => {
    set text(size: 9.5pt)
    set stroke(bottom: 0.3pt + black)
    set stroke(left: none, right: none, top: none)
    it
  }

  // ============================================================================
  // FIGURE STYLING - Minimal captions
  // ============================================================================

  #show figure: it => {
    set align(center)
    v(0.1in)
    it.body
    v(0.05in)
    text(size: 9pt, style: "italic")[
      *Figure #counter(figure).display()*: #it.caption
    ]
    v(0.1in)
  }

  // ============================================================================
  // LIST STYLING - Compact, efficient
  // ============================================================================

  #show enum: it => {
    v(0.05in)
    it
    v(0.05in)
  }

  #show list: it => {
    v(0.05in)
    it
    v(0.05in)
  }

  // ============================================================================
  // QUOTE STYLING - Minimal border
  // ============================================================================

  #show quote: it => {
    v(0.1in)
    block(
      inset: (left: 12pt),
      stroke: (left: 2pt + black),
      width: 100%,
      it.body
    )
    v(0.1in)
  }

  // ============================================================================
  // FOOTNOTE STYLING - Compact
  // ============================================================================

  #set footnote(numbering: "1")

  #show footnote: it => {
    super(text(size: 7pt, it.body))
  }

  // ============================================================================
  // HEADING STYLING - Clean, minimal, no fills
  // ============================================================================

  #show heading.where(level: 1): it => {
    pagebreak(weak: true)
    v(0.2in)
    text(size: 14pt, weight: "bold")[
      #counter(heading).display() #it.body
    ]
    line(length: 100%, stroke: 0.5pt + black)
    v(0.15in)
  }

  #show heading.where(level: 2): it => {
    v(0.15in)
    text(size: 12pt, weight: "bold")[
      #counter(heading).display() #it.body
    ]
    v(0.1in)
  }

  #show heading.where(level: 3): it => {
    v(0.1in)
    text(size: 11pt, weight: "bold", style: "italic")[
      #counter(heading).display() #it.body
    ]
    v(0.08in)
  }

  #show heading.where(level: 4): it => {
    v(0.08in)
    text(size: 10pt, weight: "bold")[
      #counter(heading).display() #it.body
    ]
    v(0.06in)
  }

  // ============================================================================
  // TITLE PAGE - Minimal, professional, compact
  // ============================================================================

  align(center)[
    #v(2in)
    #text(size: 16pt, weight: "bold")[#title]

    #if subtitle != none [
      #v(0.15in)
      #text(size: 11pt, style: "italic")[#subtitle]
    ]

    #if authors.len() > 0 [
      #v(0.3in)
      #for author in authors [
        #text(size: 10pt)[
          #author.name
          #if "affiliation" in author [
            \ #text(style: "italic", size: 9pt)[#author.affiliation]
          ]
        ]
        #v(0.06in)
      ]
    ]

    #v(0.2in)
    #text(size: 9pt)[
      #date.display()
    ]

    #v(1.2in)
  ]

  #pagebreak()

  // ============================================================================
  // ABSTRACT - Minimal border, no fill, compact
  // ============================================================================

  #if abstract != [] [
    #text(size: 11pt, weight: "bold")[Abstract]
    #v(0.08in)

    #block(
      fill: white,
      stroke: 0.5pt + black,
      inset: 8pt,
      width: 100%,
      abstract
    )

    #if keywords.len() > 0 [
      #v(0.08in)
      #text(size: 9pt)[
        *Keywords:* #keywords.join(", ")
      ]
    ]

    #v(0.15in)
  ]

  // ============================================================================
  // TABLE OF CONTENTS - Compact, efficient
  // ============================================================================

  #text(size: 11pt, weight: "bold")[Table of Contents]
  #v(0.08in)
  #outline(depth: 4, indent: 0.15in)
  #pagebreak()

  // ============================================================================
  // MAIN CONTENT - Minimal headers/footers (toner-friendly)
  // ============================================================================

  #set page(
    numbering: "1",
    header: context [
      #align(right)[
        #text(size: 9pt)[
          #counter(page).display("1")
        ]
      ]
    ],
    footer: none,
  )

  #counter(page).update(1)

  #doc
]
