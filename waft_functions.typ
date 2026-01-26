// Custom functions and styling for WAFT whitepaper
// Style: Clean Academic - No Colors

// ============================================================================
// CALLOUT BOXES - Clean with left border only
// ============================================================================

#let callout(type: "info", title: none, body) = {
  // All types use same clean styling - differentiated by icon/title only
  let icons = (
    info: "ℹ",
    warning: "⚠",
    danger: "⛔",
    success: "✓",
    note: "✎",
  )

  let icon = icons.at(type, default: "•")

  v(0.2in)
  block(
    fill: luma(252),
    stroke: (left: 3pt + black),
    radius: 0pt,
    inset: (left: 16pt, top: 12pt, bottom: 12pt, right: 12pt),
    width: 100%,
    [
      #if title != none [
        #text(weight: "bold", size: 11pt)[#icon #h(0.3em) #title]
        #v(0.08in)
      ]
      #body
    ]
  )
  v(0.2in)
}

// ============================================================================
// EVIDENCE BOX - For code/file references
// ============================================================================

#let evidence(location, content) = {
  v(0.2in)
  block(
    fill: luma(250),
    stroke: 0.75pt + luma(180),
    radius: 2pt,
    inset: 12pt,
    width: 100%,
    [
      #text(weight: "bold", size: 10pt, font: "JetBrains Mono")[#location]
      #v(0.1in)
      #content
    ]
  )
  v(0.2in)
}

// ============================================================================
// METRIC DISPLAY - Clean numerical highlight
// ============================================================================

#let metric(label, value, unit: "") = {
  box(
    stroke: 1pt + luma(180),
    radius: 2pt,
    inset: 10pt,
    [
      #text(size: 9pt, fill: luma(100))[#label]
      #v(0.03in)
      #text(size: 16pt, weight: "bold")[#value]
      #if unit != "" [
        #text(size: 11pt, fill: luma(80))[ #unit]
      ]
    ]
  )
}

// ============================================================================
// DEFINITION ENVIRONMENT - Academic style
// ============================================================================

#let definition(term, body, number: none) = {
  v(0.15in)
  block(
    width: 100%,
    inset: (left: 0pt, right: 0pt, top: 0pt, bottom: 0pt),
    [
      #text(weight: "bold")[Definition#if number != none [ #number]: #term.]
      #h(0.5em)
      #emph(body)
    ]
  )
  v(0.15in)
}

// ============================================================================
// THEOREM ENVIRONMENT - Academic style
// ============================================================================

#let theorem(title: none, body, number: none, kind: "Theorem") = {
  v(0.15in)
  block(
    width: 100%,
    stroke: (top: 0.75pt + luma(150), bottom: 0.75pt + luma(150)),
    inset: (x: 0pt, y: 10pt),
    [
      #text(weight: "bold")[#kind#if number != none [ #number]#if title != none [ (#title)].]
      #h(0.3em)
      #emph(body)
    ]
  )
  v(0.15in)
}

// ============================================================================
// NOTE / ASIDE - Margin-style note
// ============================================================================

#let note(body) = {
  text(size: 10pt, style: "italic", fill: luma(80))[
    [#body]
  ]
}

// ============================================================================
// SIDEBAR - Extended aside block
// ============================================================================

#let sidebar(title: none, body) = {
  v(0.15in)
  block(
    fill: luma(248),
    stroke: (y: 0.5pt + luma(180)),
    inset: 12pt,
    width: 100%,
    [
      #if title != none [
        #text(weight: "bold", size: 10pt, tracking: 0.05em, upper(title))
        #v(0.08in)
      ]
      #set text(size: 10pt)
      #body
    ]
  )
  v(0.15in)
}

// ============================================================================
// KEY-VALUE PAIR - For specifications
// ============================================================================

#let keyval(key, value) = {
  grid(
    columns: (auto, 1fr),
    gutter: 1em,
    text(weight: "bold")[#key:],
    value,
  )
}

// ============================================================================
// PROGRESS BAR - Text-based percentage display
// ============================================================================

#let progress(percent, label: none) = {
  let filled = calc.round(percent / 5)
  let empty = 20 - filled
  box(
    inset: (x: 4pt, y: 2pt),
    [
      #if label != none [#text(size: 9pt)[#label] ]
      #text(font: "JetBrains Mono", size: 9pt)[
        [#("█" * filled)#("░" * empty)] #percent%
      ]
    ]
  )
}

// ============================================================================
// STATUS INDICATOR - Simple text badges
// ============================================================================

#let status(state) = {
  let (symbol, label) = (
    verified: ("✓", "Verified"),
    partial: ("◐", "Partial"),
    unverified: ("○", "Unverified"),
    failed: ("✗", "Failed"),
  ).at(state, default: ("?", state))

  box(
    stroke: 0.5pt + luma(150),
    radius: 2pt,
    inset: (x: 6pt, y: 3pt),
    text(size: 9pt)[#symbol #label]
  )
}

// ============================================================================
// SECTION DIVIDER - Clean horizontal rule with optional label
// ============================================================================

#let divider(label: none) = {
  v(0.3in)
  if label != none {
    align(center)[
      #line(length: 30%, stroke: 0.5pt + luma(180))
      #h(1em)
      #text(size: 9pt, fill: luma(120), tracking: 0.1em, upper(label))
      #h(1em)
      #line(length: 30%, stroke: 0.5pt + luma(180))
    ]
  } else {
    line(length: 100%, stroke: 0.5pt + luma(180))
  }
  v(0.3in)
}

// ============================================================================
// COMPARISON TABLE - Side by side comparison
// ============================================================================

#let comparison(left-title, left-content, right-title, right-content) = {
  v(0.15in)
  grid(
    columns: (1fr, 1fr),
    gutter: 1em,
    block(
      stroke: (top: 2pt + black),
      inset: (top: 8pt),
      width: 100%,
      [
        #text(weight: "bold", size: 10pt)[#left-title]
        #v(0.1in)
        #left-content
      ]
    ),
    block(
      stroke: (top: 2pt + luma(150)),
      inset: (top: 8pt),
      width: 100%,
      [
        #text(weight: "bold", size: 10pt)[#right-title]
        #v(0.1in)
        #right-content
      ]
    ),
  )
  v(0.15in)
}

// ============================================================================
// CHECKLIST ITEM - Clean checkbox display
// ============================================================================

#let check(done: false, body) = {
  let box-char = if done { "☑" } else { "☐" }
  [#box-char #body]
}

// ============================================================================
// EPIGRAPH - Chapter opening quote
// ============================================================================

#let epigraph(quote, author: none) = {
  v(0.3in)
  align(right, block(
    width: 70%,
    [
      #text(style: "italic")[#quote]
      #if author != none {
        v(0.2em)
        text(size: 10pt)[— #author]
      }
    ]
  ))
  v(0.4in)
}

// ============================================================================
// CODE WITH FILENAME - Labeled code block
// ============================================================================

#let codefile(filename, code) = {
  v(0.15in)
  block(
    width: 100%,
    [
      #block(
        fill: luma(230),
        stroke: (x: 0.5pt + luma(180), top: 0.5pt + luma(180)),
        inset: (x: 10pt, y: 6pt),
        width: 100%,
        text(font: "JetBrains Mono", size: 9pt, weight: "medium")[#filename]
      )
      #block(
        fill: luma(250),
        stroke: (x: 0.5pt + luma(180), bottom: 0.5pt + luma(180)),
        inset: 0pt,
        width: 100%,
        code
      )
    ]
  )
  v(0.15in)
}

// ============================================================================
// INLINE TAG - Small label/badge
// ============================================================================

#let tag(label) = {
  box(
    fill: luma(240),
    radius: 2pt,
    inset: (x: 4pt, y: 2pt),
    text(size: 8pt, font: "JetBrains Mono")[#label]
  )
}

// ============================================================================
// TIMELINE ENTRY - For historical/sequential events
// ============================================================================

#let timeline-entry(date, title, body) = {
  grid(
    columns: (auto, 1fr),
    gutter: 1em,
    align(right, text(weight: "bold", size: 10pt)[#date]),
    [
      #text(weight: "bold")[#title]
      #linebreak()
      #body
    ]
  )
  v(0.1in)
}
