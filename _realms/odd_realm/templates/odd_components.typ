// ODD Components - Shared styling for Ontological Determinism Department documents
// Part of the ODD Realm for WAFT

#import "@preview/s6t5-page-bordering:1.0.0": s6t5-page-bordering

// =============================================================================
// COLOR PALETTE
// =============================================================================

#let odd-black = rgb("#1a1a1a")
#let odd-dark = rgb("#2d2d2d")
#let odd-gray = rgb("#4a4a4a")
#let odd-light = rgb("#e8e8e8")
#let odd-accent = rgb("#8b0000")  // Dark red for warnings/critical
#let odd-nexus = rgb("#1a1a2e")   // Deep blue-black for Nexus references

// =============================================================================
// CLASSIFICATION BADGES
// =============================================================================

#let classification-badge(level) = {
  let (bg, fg) = if level == "WITNESSED" {
    (odd-light, odd-dark)
  } else if level == "ARCHIVED" {
    (odd-gray, white)
  } else if level == "CONVERGENCE EYES ONLY" {
    (odd-accent, white)
  } else {
    (odd-light, odd-dark)
  }
  
  box(
    fill: bg,
    inset: (x: 8pt, y: 4pt),
    radius: 2pt,
    text(fill: fg, weight: "bold", size: 8pt)[#level]
  )
}

// =============================================================================
// REDACTION BLOCK
// =============================================================================

#let redacted(content: none, reason: "INFORMATION EXISTS OUTSIDE OBSERVER BANDWIDTH") = {
  if content != none {
    box(
      fill: odd-black,
      inset: (x: 4pt, y: 2pt),
      text(fill: odd-black, size: 10pt)[#content]
    )
  } else {
    box(
      fill: odd-light,
      inset: 8pt,
      width: 100%,
      stroke: (left: 3pt + odd-gray),
    )[
      #text(fill: odd-gray, style: "italic", size: 9pt)[
        \[#reason\]
      ]
    ]
  }
}

// =============================================================================
// CALLOUT BOXES
// =============================================================================

#let odd-warning(content) = {
  box(
    fill: odd-accent.lighten(90%),
    inset: 12pt,
    width: 100%,
    radius: 2pt,
    stroke: (left: 4pt + odd-accent),
  )[
    #text(fill: odd-accent, weight: "bold")[⚠ WARNING] \
    #content
  ]
}

#let odd-note(content) = {
  box(
    fill: odd-nexus.lighten(95%),
    inset: 12pt,
    width: 100%,
    radius: 2pt,
    stroke: (left: 4pt + odd-nexus),
  )[
    #text(fill: odd-nexus, weight: "bold")[📋 NOTE] \
    #content
  ]
}

#let odd-observation(content) = {
  box(
    fill: odd-gray.lighten(90%),
    inset: 12pt,
    width: 100%,
    radius: 2pt,
    stroke: (left: 4pt + odd-gray),
  )[
    #text(fill: odd-gray, weight: "bold")[👁 OBSERVATION] \
    #content
  ]
}

// =============================================================================
// ARCHIVE REFERENCE FOOTER
// =============================================================================

#let archive-ref(reference, stability: 0.94) = {
  align(center)[
    #line(length: 80%, stroke: 0.5pt + odd-gray)
    #v(4pt)
    #text(size: 8pt, fill: odd-gray)[
      \[Archive Reference: #reference | Reality Stability Index: #stability\]
    ]
  ]
}

// =============================================================================
// NEXUS TIMESTAMP
// =============================================================================

#let nexus-timestamp(delta: "∞", phi: 0.73) = {
  text(size: 9pt, fill: odd-gray)[
    \[Observation Point: Δt-#delta / ΦLC: #phi\]
  ]
}

// =============================================================================
// SPEAKER LABEL (for interviews)
// =============================================================================

#let speaker(id) = {
  v(8pt)
  text(weight: "bold", fill: odd-dark)[#id:]
  h(8pt)
}

// =============================================================================
// DOCUMENT TEMPLATES
// =============================================================================

// Case File Template
#let odd-case-file(
  case-id: "ODD-CF-XXX",
  classification: "WITNESSED",
  observer: "UNKNOWN",
  subject: "UNSPECIFIED",
  timestamp: none,
  doc,
) = {
  // Header
  let header = {
    set align(bottom)
    set text(weight: "bold", size: 9pt)
    table(
      stroke: (y: none),
      columns: (1fr, 1.5fr, 0.8fr),
      rows: 1fr,
      table.hline(),
      [#case-id],
      align(center)[ONTOLOGICAL DETERMINISM DEPARTMENT],
      align(right)[
        #context counter(page).display("1 / 1", both: true)
      ],
    )
  }

  // Footer
  let footer = {
    set text(size: 8pt, fill: odd-gray)
    table(
      stroke: (y: none),
      columns: (1fr, 1fr, 1fr),
      rows: 1fr,
      [Observer: #observer],
      align(center)[#classification-badge(classification)],
      align(right)[
        #if timestamp != none { timestamp } else { nexus-timestamp() }
      ],
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
    #text(size: 14pt, weight: "bold")[CASE FILE: #case-id]
    #v(4pt)
    #text(size: 11pt)[Subject: #subject]
    #v(12pt)
  ]

  doc
}

// Interview Template
#let odd-interview(
  interview-id: "ODD-INT-XXX",
  participants: (),
  classification: "WITNESSED",
  timestamp: none,
  doc,
) = {
  // Header
  let header = {
    set align(bottom)
    set text(weight: "bold", size: 9pt)
    table(
      stroke: (y: none),
      columns: (1fr, 1.5fr, 0.8fr),
      rows: 1fr,
      table.hline(),
      [#interview-id],
      align(center)[INTERVIEW TRANSCRIPT],
      align(right)[
        #context counter(page).display("1 / 1", both: true)
      ],
    )
  }

  // Footer
  let footer = {
    set text(size: 8pt, fill: odd-gray)
    table(
      stroke: (y: none),
      columns: (1fr, 1fr, 1fr),
      rows: 1fr,
      [Participants: #participants.join(", ")],
      align(center)[#classification-badge(classification)],
      align(right)[
        #if timestamp != none { timestamp } else { nexus-timestamp() }
      ],
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
    #text(size: 14pt, weight: "bold")[INTERVIEW: #interview-id]
    #v(4pt)
    #text(size: 10pt)[Participants: #participants.join(" • ")]
    #v(12pt)
  ]

  doc
}
