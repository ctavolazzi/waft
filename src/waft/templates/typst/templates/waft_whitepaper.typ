// WAFT White Paper Template
// A professional white paper template for WAFT publications
// Based on academic paper templates with WAFT-specific styling
// Following Typst template tutorial: https://typst.app/docs/tutorial/making-a-template/

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
  // PAGE SETUP
  // ============================================================================

  #set page(
    paper: "us-letter",
    margin: (
      top: 1in,
      bottom: 1in,
      left: 1.25in,
      right: 1.25in,
    ),
  )

  // ============================================================================
  // TYPOGRAPHY
  // ============================================================================

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

  // ============================================================================
  // CODE BLOCK STYLING
  // ============================================================================

  #show raw.where(block: true): it => {
    set text(font: "Liberation Mono", size: 9pt)
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
      text(font: "Liberation Mono", size: 10pt, it)
    )
  }

  // ============================================================================
  // HEADING STYLING
  // ============================================================================

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

  #show heading.where(level: 3): it => {
    v(0.15in)
    text(fill: rgb("#555555"), size: 14pt, weight: "bold")[
      #counter(heading).display() #it.body
    ]
    v(0.1in)
  }

  // ============================================================================
  // TITLE PAGE
  // ============================================================================

  align(center)[
    #v(2in)
    #text(size: 28pt, weight: "bold", fill: rgb("#1976d2"))[#title]

    #if subtitle != none [
      #v(0.3in)
      #text(size: 16pt, fill: rgb("#666666"), style: "italic")[#subtitle]
    ]

    #if authors.len() > 0 [
      #v(0.5in)
      #for author in authors [
        #text(size: 12pt)[
          #author.name
          #if "affiliation" in author [
            \ #text(style: "italic", size: 10pt)[#author.affiliation]
          ]
        ]
        #v(0.1in)
      ]
    ]

    #v(0.3in)
    #text(size: 10pt, fill: rgb("#999999"))[
      #date.display()
    ]

    #v(1in)
  ]

  #pagebreak()

  // ============================================================================
  // ABSTRACT
  // ============================================================================

  #if abstract != [] [
    #align(center)[
      #text(size: 14pt, weight: "bold")[Abstract]
    ]
    #v(0.2in)

    #block(
      fill: rgb("#f8f9fa"),
      stroke: 1pt + rgb("#dee2e6"),
      radius: 4pt,
      inset: 16pt,
      width: 100%,
      abstract
    )

    #if keywords.len() > 0 [
      #v(0.2in)
      #text(size: 10pt, fill: rgb("#666666"))[
        *Keywords:* #keywords.join(", ")
      ]
    ]

    #pagebreak()
  ]

  // ============================================================================
  // TABLE OF CONTENTS
  // ============================================================================

  #align(center)[
    #text(size: 16pt, weight: "bold")[Table of Contents]
  ]
  #v(0.3in)
  #outline(depth: 3)
  #pagebreak()

  // ============================================================================
  // MAIN CONTENT
  // ============================================================================

  #set page(
    numbering: "1",
    header: context [
      #text(size: 10pt, fill: rgb("#666666"))[
        #title
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
          WAFT Framework | #date.display()
        ]
      ]
    ],
  )

  #counter(page).update(1)

  #doc
]
