// dialectic_components.typ - Shared styling for DIALECTIC documents
// Part of DIALECTIC Engine Tools
//
// Based on the ODD Realm components pattern
// Philosophy: Hegelian Dialectics - Thesis, Antithesis, Synthesis

#import "@preview/s6t5-page-bordering:1.0.0": s6t5-page-bordering

// =============================================================================
// COLOR PALETTE
// =============================================================================

#let dialectic-black = rgb("#0d1117")
#let dialectic-dark = rgb("#161b22")
#let dialectic-gray = rgb("#30363d")
#let dialectic-light = rgb("#c9d1d9")

// Phase colors
#let thesis-blue = rgb("#1f6feb")
#let antithesis-red = rgb("#da3633")
#let synthesis-purple = rgb("#a371f7")

// Status colors
#let status-success = rgb("#3fb950")
#let status-warning = rgb("#f0883e")
#let status-error = rgb("#f85149")

// =============================================================================
// PHASE BADGES
// =============================================================================

#let phase-badge(phase) = {
  let (bg, fg, label) = if phase == "thesis" {
    (thesis-blue, white, "THESIS")
  } else if phase == "antithesis" {
    (antithesis-red, white, "ANTITHESIS")
  } else if phase == "synthesis" {
    (synthesis-purple, white, "SYNTHESIS")
  } else {
    (dialectic-gray, white, upper(phase))
  }
  
  box(
    fill: bg,
    inset: (x: 10pt, y: 5pt),
    radius: 4pt,
    text(fill: fg, weight: "bold", size: 9pt)[#label]
  )
}

// =============================================================================
// VERIFICATION BADGES
// =============================================================================

#let verification-badge(status) = {
  let (bg, fg, label) = if status == "proven" {
    (status-success.lighten(80%), status-success.darken(20%), "✓ PROVEN")
  } else if status == "refuted" {
    (status-error.lighten(80%), status-error.darken(20%), "✗ REFUTED")
  } else if status == "unknown" {
    (status-warning.lighten(80%), status-warning.darken(20%), "? UNKNOWN")
  } else {
    (dialectic-gray.lighten(80%), dialectic-gray, upper(status))
  }
  
  box(
    fill: bg,
    inset: (x: 8pt, y: 4pt),
    radius: 3pt,
    text(fill: fg, weight: "bold", size: 8pt)[#label]
  )
}

// =============================================================================
// CALLOUT BOXES
// =============================================================================

#let thesis-callout(content) = {
  block(
    fill: thesis-blue.lighten(90%),
    inset: 12pt,
    width: 100%,
    radius: 4pt,
    stroke: (left: 4pt + thesis-blue),
  )[
    #text(fill: thesis-blue, weight: "bold")[📚 THESIS] \
    #content
  ]
}

#let antithesis-callout(content) = {
  block(
    fill: antithesis-red.lighten(90%),
    inset: 12pt,
    width: 100%,
    radius: 4pt,
    stroke: (left: 4pt + antithesis-red),
  )[
    #text(fill: antithesis-red, weight: "bold")[🔍 ANTITHESIS] \
    #content
  ]
}

#let synthesis-callout(content) = {
  block(
    fill: synthesis-purple.lighten(90%),
    inset: 12pt,
    width: 100%,
    radius: 4pt,
    stroke: (left: 4pt + synthesis-purple),
  )[
    #text(fill: synthesis-purple, weight: "bold")[✨ SYNTHESIS] \
    #content
  ]
}

// Generic callout
#let dialectic-note(content, title: "Note") = {
  block(
    fill: dialectic-gray.lighten(90%),
    inset: 12pt,
    width: 100%,
    radius: 4pt,
    stroke: (left: 4pt + dialectic-gray),
  )[
    #text(fill: dialectic-gray, weight: "bold")[📋 #title] \
    #content
  ]
}

// =============================================================================
// EVIDENCE BLOCKS
// =============================================================================

#let evidence-block(status, evidence, source: none) = {
  let color = if status == "proven" { status-success }
              else if status == "refuted" { status-error }
              else { status-warning }
  
  block(
    fill: color.lighten(90%),
    inset: 10pt,
    width: 100%,
    radius: 4pt,
    stroke: (left: 3pt + color),
  )[
    #verification-badge(status)
    #v(0.3em)
    #evidence
    #if source != none [
      #v(0.2em)
      #text(8pt, fill: gray)[Source: #source]
    ]
  ]
}

// =============================================================================
// PHASE TRANSITION INDICATOR
// =============================================================================

#let phase-transition(from-phase, to-phase) = {
  let from-color = if from-phase == "thesis" { thesis-blue }
                   else if from-phase == "antithesis" { antithesis-red }
                   else { synthesis-purple }
  
  let to-color = if to-phase == "thesis" { thesis-blue }
                 else if to-phase == "antithesis" { antithesis-red }
                 else { synthesis-purple }
  
  align(center)[
    #v(1em)
    #box(
      inset: 10pt,
      radius: 4pt,
      fill: luma(248),
    )[
      #text(fill: from-color, weight: "bold")[#upper(from-phase)]
      #h(1em)
      #text(fill: luma(150))[→]
      #h(1em)
      #text(fill: to-color, weight: "bold")[#upper(to-phase)]
    ]
    #v(1em)
  ]
}

// =============================================================================
// DIALECTIC FOOTER
// =============================================================================

#let dialectic-footer(port: 2112, realm: "dialectic_realm") = {
  align(center)[
    #line(length: 80%, stroke: 0.5pt + dialectic-gray)
    #v(0.3em)
    #text(size: 8pt, fill: dialectic-gray)[
      DIALECTIC Engine // Port: #port // Realm: #realm \\
      "The truth is the whole." - G.W.F. Hegel
    ]
  ]
}

// =============================================================================
// DIALECTIC DOCUMENT TEMPLATE
// =============================================================================

#let dialectic-doc(
  title: "",
  phase: "synthesis",
  timestamp: datetime.today().display(),
  classification: "INTERNAL",
  doc,
) = {
  let phase-color = if phase == "thesis" { thesis-blue }
                    else if phase == "antithesis" { antithesis-red }
                    else { synthesis-purple }

  // Header
  let header = {
    set align(bottom)
    set text(weight: "bold", size: 9pt)
    table(
      stroke: (y: none),
      columns: (1fr, 2fr, 0.8fr),
      rows: 1fr,
      table.hline(),
      [DIALECTIC // #upper(phase)],
      align(center)[#title],
      align(right)[
        #context counter(page).display("1 / 1", both: true)
      ],
    )
  }

  // Footer
  let footer = {
    set text(size: 8pt, fill: dialectic-gray)
    table(
      stroke: (y: none),
      columns: (1fr, 1fr, 1fr),
      rows: 1fr,
      [Port: 2112],
      align(center)[#phase-badge(phase)],
      align(right)[#timestamp],
      table.hline(),
    )
  }

  // Apply page bordering
  show: s6t5-page-bordering.with(
    margin: (left: 45pt, right: 45pt, top: 75pt, bottom: 75pt),
    expand: 15pt,
    space-top: 15pt,
    space-bottom: 15pt,
    stroke-header: none,
    stroke-footer: none,
    header: header,
    footer: footer,
  )

  set text(font: "New Computer Modern", size: 11pt)
  set par(justify: true)

  // Title block
  align(center)[
    #text(size: 16pt, weight: "bold")[DIALECTIC ENGINE]
    #v(0.3em)
    #text(size: 14pt, fill: phase-color)[#title]
    #v(0.5em)
    #phase-badge(phase)
    #v(1em)
  ]

  doc
  
  v(2em)
  dialectic-footer()
}
