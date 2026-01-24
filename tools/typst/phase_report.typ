// phase_report.typ - Template for DIALECTIC Phase Reports
// Part of DIALECTIC Engine Tools
//
// Usage:
//   #import "phase_report.typ": phase-report, thesis-header, antithesis-header, synthesis-header

// Color definitions for each phase
#let thesis-color = rgb("#1f6feb")      // Blue
#let antithesis-color = rgb("#da3633")  // Red
#let synthesis-color = rgb("#a371f7")   // Purple

// Phase header component
#let phase-header(phase-name, phase-type, color) = {
  block(
    fill: color.lighten(90%),
    inset: 15pt,
    radius: 6pt,
    width: 100%,
    stroke: (top: 4pt + color),
  )[
    #align(center)[
      #text(20pt, weight: "bold", fill: color)[#phase-name]
      #v(0.3em)
      #text(12pt, fill: color.darken(20%))[Phase: #phase-type]
    ]
  ]
}

// Specific phase headers
#let thesis-header() = phase-header("THESIS", "Assembly", thesis-color)
#let antithesis-header() = phase-header("ANTITHESIS", "Sanity Check", antithesis-color)
#let synthesis-header() = phase-header("SYNTHESIS", "Problem Description", synthesis-color)

// Evidence block
#let evidence-block(status, content) = {
  let (icon, color) = if status == "proven" {
    ("✓", rgb("#3fb950"))
  } else if status == "refuted" {
    ("✗", rgb("#f85149"))
  } else {
    ("?", rgb("#f0883e"))
  }
  
  block(
    fill: color.lighten(90%),
    inset: 10pt,
    radius: 4pt,
    width: 100%,
    stroke: (left: 3pt + color),
  )[
    #text(weight: "bold", fill: color)[#icon #status.slice(0, 1).to-upper() + status.slice(1)]
    #v(0.3em)
    #content
  ]
}

// Assumption validation table
#let assumption-table(assumptions) = {
  table(
    columns: (auto, 2fr, auto, 1fr),
    fill: (_, y) => if y == 0 { luma(230) } else { none },
    [*ID*], [*Assumption*], [*Status*], [*Evidence*],
    ..assumptions.map(a => (
      [#a.id],
      [#a.assumption],
      [#if a.status == "proven" { text(fill: rgb("#3fb950"))[✓ Proven] } 
       else if a.status == "refuted" { text(fill: rgb("#f85149"))[✗ Refuted] }
       else { text(fill: rgb("#f0883e"))[? Unknown] }],
      [#a.evidence],
    )).flatten(),
  )
}

// Progress indicator
#let progress-indicator(current, total, color: thesis-color) = {
  let percentage = calc.round(current / total * 100)
  
  block(
    inset: 10pt,
    width: 100%,
  )[
    #text(10pt)[Progress: #current / #total (#percentage%)]
    #v(0.3em)
    #box(
      width: 100%,
      height: 8pt,
      fill: luma(230),
      radius: 4pt,
    )[
      #box(
        width: percentage * 1%,
        height: 8pt,
        fill: color,
        radius: 4pt,
      )
    ]
  ]
}

// Phase summary box
#let phase-summary(title, items, color: thesis-color) = {
  block(
    fill: color.lighten(95%),
    inset: 15pt,
    radius: 6pt,
    width: 100%,
    stroke: 1pt + color.lighten(50%),
  )[
    #text(14pt, weight: "bold", fill: color)[#title]
    #v(0.5em)
    #for item in items [
      - #item
    ]
  ]
}

// Phase transition arrow
#let phase-transition(from-phase, to-phase) = {
  align(center)[
    #v(1em)
    #text(fill: luma(150))[
      #from-phase #h(1em) → #h(1em) #to-phase
    ]
    #v(1em)
  ]
}

// Full phase report template
#let phase-report(
  phase: "thesis",
  title: "Phase Report",
  timestamp: datetime.today().display(),
  body
) = {
  let color = if phase == "thesis" { thesis-color }
              else if phase == "antithesis" { antithesis-color }
              else { synthesis-color }
  
  set page(
    paper: "us-letter",
    margin: 1in,
    header: [
      #set text(8pt)
      DIALECTIC Engine // #upper(phase) Phase
      #h(1fr)
      #timestamp
    ],
    footer: [
      #set text(8pt)
      #h(1fr)
      #context counter(page).display("1 / 1", both: true)
      #h(1fr)
    ],
  )
  
  set text(font: "New Computer Modern", size: 11pt)
  
  // Title
  align(center)[
    #text(18pt, weight: "bold")[DIALECTIC - #title]
    #v(0.3em)
    #text(14pt, fill: color)[PHASE: #upper(phase)]
    #v(0.3em)
    #text(10pt)[#timestamp]
  ]
  
  line(length: 100%, stroke: 0.5pt)
  v(1em)
  
  body
}
