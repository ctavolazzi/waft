// =============================================================================
// WAFT Work Effort Architecture Template
// =============================================================================
// A reusable template for documenting architectural designs in WAFT work efforts.
// 
// Usage:
//   #import "work_effort_architecture.typ": *
//   #show: waft-architecture.with(
//     title: "The Tribunal",
//     subtitle: "WAFT Court System",
//     work-effort-id: "WE-260121-1f3l",
//     author: "Terry (AI Assistant)",
//     version: "1.0.0",
//   )
//
// Created: 2026-01-21
// Template Version: 1.0.0
// =============================================================================

// Color palette - WAFT Brand
#let waft-primary = rgb("#2c3e50")      // Dark slate
#let waft-secondary = rgb("#3498db")    // Blue accent
#let waft-success = rgb("#27ae60")      // Green
#let waft-warning = rgb("#f39c12")      // Orange
#let waft-danger = rgb("#e74c3c")       // Red
#let waft-light = rgb("#ecf0f1")        // Light gray
#let waft-dark = rgb("#1a252f")         // Darker slate

// Main template function
#let waft-architecture(
  title: "Architecture Document",
  subtitle: none,
  work-effort-id: none,
  author: "WAFT Team",
  date: datetime.today().display("[year]-[month]-[day]"),
  version: "1.0.0",
  realm: none,
  port: none,
  status: "Draft",
  abstract: none,
  doc,
) = {
  // Page setup
  set page(
    paper: "us-letter",
    margin: (top: 1.25in, bottom: 1in, left: 1in, right: 1in),
    header: context {
      if counter(page).get().first() > 1 [
        #set text(size: 9pt, fill: waft-primary)
        #grid(
          columns: (1fr, 1fr),
          align(left)[#title],
          align(right)[#if work-effort-id != none [#work-effort-id] else [WAFT Architecture]]
        )
        #line(length: 100%, stroke: 0.5pt + waft-light)
      ]
    },
    footer: context {
      set text(size: 9pt, fill: waft-primary)
      grid(
        columns: (1fr, 1fr, 1fr),
        align(left)[v#version],
        align(center)[#counter(page).display("1 of 1", both: true)],
        align(right)[#date]
      )
    },
  )
  
  // Typography
  set text(font: "Libertinus Serif", size: 11pt)
  set par(justify: true, leading: 0.65em)
  
  // Headings
  set heading(numbering: "1.1.")
  show heading.where(level: 1): it => {
    pagebreak(weak: true)
    v(0.5em)
    block(
      fill: waft-primary,
      inset: (x: 12pt, y: 8pt),
      radius: 4pt,
      width: 100%,
      text(fill: white, weight: "bold", size: 14pt)[
        #counter(heading).display() #it.body
      ]
    )
    v(0.5em)
  }
  
  show heading.where(level: 2): it => {
    v(0.8em)
    text(fill: waft-primary, weight: "bold", size: 12pt)[
      #counter(heading).display() #it.body
    ]
    v(0.3em)
    line(length: 100%, stroke: 0.5pt + waft-light)
    v(0.3em)
  }
  
  show heading.where(level: 3): it => {
    v(0.5em)
    text(fill: waft-secondary, weight: "bold", size: 11pt)[
      #counter(heading).display() #it.body
    ]
    v(0.2em)
  }
  
  // Code blocks
  show raw.where(block: true): it => {
    block(
      fill: rgb("#f8f9fa"),
      inset: 10pt,
      radius: 4pt,
      width: 100%,
      it
    )
  }
  
  // Inline code
  show raw.where(block: false): box.with(
    fill: rgb("#f0f0f0"),
    inset: (x: 3pt, y: 0pt),
    outset: (y: 3pt),
    radius: 2pt,
  )
  
  // Links
  show link: it => {
    text(fill: waft-secondary, it)
  }
  
  // =========================================================================
  // TITLE PAGE
  // =========================================================================
  
  v(2in)
  
  align(center)[
    #block(
      fill: waft-primary,
      inset: 16pt,
      radius: 8pt,
      width: 90%,
    )[
      #text(fill: white, size: 28pt, weight: "bold")[#title]
      #if subtitle != none [
        #v(0.3em)
        #text(fill: waft-light, size: 16pt)[#subtitle]
      ]
    ]
  ]
  
  v(1em)
  
  align(center)[
    #if work-effort-id != none [
      #block(
        fill: waft-secondary,
        inset: 8pt,
        radius: 4pt,
      )[
        #text(fill: white, weight: "bold")[Work Effort: #work-effort-id]
      ]
    ]
    
    #v(0.5em)
    
    #grid(
      columns: 2,
      gutter: 2em,
      [
        #if realm != none [
          #text(weight: "bold")[Realm:] #realm \
        ]
        #if port != none [
          #text(weight: "bold")[Port:] #port \
        ]
        #text(weight: "bold")[Status:] #status
      ],
      [
        #text(weight: "bold")[Author:] #author \
        #text(weight: "bold")[Date:] #date \
        #text(weight: "bold")[Version:] #version
      ]
    )
  ]
  
  if abstract != none [
    #v(1em)
    #align(center)[
      #block(
        width: 85%,
        inset: 12pt,
        stroke: 1pt + waft-light,
        radius: 4pt,
      )[
        #text(weight: "bold", size: 11pt)[Abstract]
        #v(0.3em)
        #text(size: 10pt, style: "italic")[#abstract]
      ]
    ]
  ]
  
  v(2em)
  
  align(center)[
    #text(size: 32pt, fill: waft-primary, weight: "bold")[WAFT]
    
    #v(0.5em)
    #text(size: 9pt, fill: waft-primary)[
      _"Don't just build agents. Breed them."_
    ]
  ]
  
  pagebreak()
  
  // =========================================================================
  // TABLE OF CONTENTS
  // =========================================================================
  
  outline(
    title: [Table of Contents],
    depth: 3,
    indent: 1.5em,
  )
  
  pagebreak()
  
  // =========================================================================
  // DOCUMENT CONTENT
  // =========================================================================
  
  doc
}

// =============================================================================
// HELPER COMPONENTS
// =============================================================================

// Status badge
#let status-badge(status, color: waft-secondary) = {
  box(
    fill: color,
    inset: (x: 8pt, y: 4pt),
    radius: 3pt,
    text(fill: white, weight: "bold", size: 9pt)[#status]
  )
}

// Info box
#let info-box(title: none, content) = {
  block(
    fill: rgb("#e8f4fd"),
    inset: 12pt,
    radius: 4pt,
    stroke: 1pt + waft-secondary,
    width: 100%,
  )[
    #if title != none [
      #text(fill: waft-secondary, weight: "bold")[#title]
      #v(0.3em)
    ]
    #content
  ]
}

// Warning box
#let warning-box(title: none, content) = {
  block(
    fill: rgb("#fef9e7"),
    inset: 12pt,
    radius: 4pt,
    stroke: 1pt + waft-warning,
    width: 100%,
  )[
    #if title != none [
      #text(fill: waft-warning, weight: "bold")[⚠️ #title]
      #v(0.3em)
    ]
    #content
  ]
}

// Success box
#let success-box(title: none, content) = {
  block(
    fill: rgb("#e8f8f0"),
    inset: 12pt,
    radius: 4pt,
    stroke: 1pt + waft-success,
    width: 100%,
  )[
    #if title != none [
      #text(fill: waft-success, weight: "bold")[✅ #title]
      #v(0.3em)
    ]
    #content
  ]
}

// Philosophy quote
#let philosophy-quote(quote, attribution: none) = {
  v(0.5em)
  block(
    fill: waft-light,
    inset: 16pt,
    radius: 4pt,
    width: 100%,
  )[
    #text(style: "italic", size: 12pt)[
      "#quote"
    ]
    #if attribution != none [
      #align(right)[
        #text(size: 10pt, fill: waft-primary)[— #attribution]
      ]
    ]
  ]
  v(0.5em)
}

// Component card
#let component-card(name, description, features: ()) = {
  block(
    stroke: 1pt + waft-light,
    inset: 12pt,
    radius: 4pt,
    width: 100%,
  )[
    #text(fill: waft-primary, weight: "bold", size: 12pt)[#name]
    #v(0.3em)
    #text(size: 10pt)[#description]
    #if features.len() > 0 [
      #v(0.3em)
      #for feature in features [
        - #feature
      ]
    ]
  ]
}

// API endpoint
#let api-endpoint(method, path, description: none) = {
  let method-color = if method == "GET" { waft-success } 
    else if method == "POST" { waft-secondary }
    else if method == "DELETE" { waft-danger }
    else { waft-warning }
  
  block(
    fill: rgb("#f8f9fa"),
    inset: 8pt,
    radius: 4pt,
    width: 100%,
  )[
    #box(
      fill: method-color,
      inset: (x: 6pt, y: 2pt),
      radius: 2pt,
      text(fill: white, weight: "bold", size: 9pt)[#method]
    )
    #h(0.5em)
    #raw(path)
    #if description != none [
      #h(1em)
      #text(size: 9pt, fill: gray)[#description]
    ]
  ]
}

// Realm port table
#let realm-ports(..ports) = {
  let data = ports.pos()
  table(
    columns: (auto, auto, auto),
    inset: 8pt,
    align: (left, center, left),
    stroke: 0.5pt + waft-light,
    fill: (_, y) => if y == 0 { waft-primary } else { none },
    [#text(fill: white, weight: "bold")[Realm]], 
    [#text(fill: white, weight: "bold")[Port]], 
    [#text(fill: white, weight: "bold")[Purpose]],
    ..data.flatten()
  )
}

// Mermaid-style diagram placeholder
#let diagram-placeholder(title, description) = {
  block(
    fill: rgb("#f0f0f0"),
    inset: 16pt,
    radius: 4pt,
    width: 100%,
  )[
    #align(center)[
      #text(fill: waft-primary, weight: "bold")[📊 #title]
      #v(0.5em)
      #text(size: 10pt, style: "italic")[#description]
      #v(0.3em)
      #text(size: 9pt, fill: gray)[(Diagram would render here in final output)]
    ]
  ]
}

// Task checklist
#let task-list(..tasks) = {
  for task in tasks.pos() {
    let (status, text) = task
    let symbol = if status == "done" { "✅" } 
      else if status == "progress" { "🔄" }
      else if status == "pending" { "⬜" }
      else { "❌" }
    [#symbol #text \ ]
  }
}

// Version history entry
#let version-entry(version, date, changes) = {
  block(
    inset: (left: 12pt),
    stroke: (left: 2pt + waft-secondary),
  )[
    #text(weight: "bold")[v#version] #h(1em) #text(fill: gray, size: 9pt)[#date]
    #v(0.2em)
    #for change in changes [
      - #change
    ]
  ]
  v(0.5em)
}
