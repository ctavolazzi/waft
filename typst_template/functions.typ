// Custom functions and styling for WAFT whitepaper

// ============================================================================
// CALLOUT BOXES
// ============================================================================

#let callout(type: "info", title: none, body) = {
  let colors = (
    info: (bg: rgb("#e3f2fd"), border: rgb("#1976d2")),
    warning: (bg: rgb("#fff3e0"), border: rgb("#f57c00")),
    danger: (bg: rgb("#ffebee"), border: rgb("#d32f2f")),
    success: (bg: rgb("#e8f5e9"), border: rgb("#388e3c")),
    note: (bg: rgb("#f3e5f5"), border: rgb("#7b1fa2")),
  )
  
  let color = colors.at(type, default: colors.info)
  
  v(0.15in)
  block(
    fill: color.bg,
    stroke: 2pt + color.border,
    radius: 4pt,
    inset: 16pt,
    width: 100%,
    [
      #if title != none [
        #text(weight: "bold", size: 12pt, fill: color.border)[#title]
        #v(0.05in)
      ]
      #body
    ]
  )
  v(0.15in)
}

// ============================================================================
// EVIDENCE BOX
// ============================================================================

#let evidence(location, content) = {
  callout(
    type: "success",
    title: [📁 Evidence: #location],
    content
  )
}

// ============================================================================
// METRIC DISPLAY
// ============================================================================

#let metric(label, value, unit: "") = {
  block(
    fill: rgb("#f5f5f5"),
    stroke: 1pt + rgb("#1976d2"),
    radius: 4pt,
    inset: 12pt,
    [
      #text(size: 10pt, fill: rgb("#666666"))[#label]
      #v(0.05in)
      #text(size: 18pt, weight: "bold", fill: rgb("#1976d2"))[#value]
      #if unit != "" [
        #text(size: 12pt, fill: rgb("#666666"))[ #unit]
      ]
    ]
  )
}
