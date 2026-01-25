// ============================================================================
// TYPST VISUALIZATION PACKAGES SHOWCASE
// LIVE demonstrations using ACTUAL package APIs
// ============================================================================

#import "@preview/tablex:0.0.9": tablex, cellx, rowspanx, colspanx
#import "@preview/gentle-clues:1.2.0": *
#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge
#import "@preview/lilaq:0.5.0" as lq
#import "@preview/zero:0.5.0": num, zi

#set document(
  title: "Typst Visualization Packages Showcase",
  author: "WAFT Documentation",
  date: datetime.today(),
)

#set page(
  paper: "us-letter",
  margin: (top: 0.75in, bottom: 0.75in, left: 0.75in, right: 0.75in),
)

#set text(font: "New Computer Modern", size: 10pt)
#set par(justify: true)

// ============================================================================
// COVER PAGE
// ============================================================================

#align(center)[
  #v(1.5in)
  
  #text(size: 36pt, weight: "bold", fill: rgb("#1976d2"))[
    TYPST VISUALIZATION
  ]
  #v(0.1in)
  #text(size: 24pt, weight: "bold")[
    PACKAGES SHOWCASE
  ]
  
  #v(0.3in)
  
  #text(size: 14pt, fill: gray)[
    Live demonstrations using actual package APIs
  ]
  
  #v(0.5in)
  
  #rect(
    stroke: 2pt + rgb("#1976d2"),
    inset: 20pt,
    radius: 8pt,
    width: 70%,
  )[
    #align(left)[
      #text(size: 11pt)[
        *Packages ACTUALLY Demonstrated:*
        - gentle-clues 1.2.0 (callouts)
        - fletcher 0.5.8 (diagrams)
        - tablex 0.0.9 (tables)
        - lilaq 0.5.0 (scientific plots)
        - zero 0.5.0 (number formatting)
      ]
    ]
  ]
  
  #v(1in)
  
  #text(size: 10pt, fill: gray)[
    Every visualization in this PDF is generated \
    by the actual package — NOT simulated.
  ]
]

#pagebreak()

// ============================================================================
// TABLE OF CONTENTS
// ============================================================================

#outline(
  title: [Contents],
  indent: 2em,
)

#pagebreak()

// ============================================================================
// 1. GENTLE-CLUES
// ============================================================================

= 1. gentle-clues — Admonitions & Callouts

#text(size: 9pt, fill: gray)[
  `#import "@preview/gentle-clues:1.2.0": *`
]

#v(0.2in)

== Live Demonstrations

#info[
  *Info Box* — General information. Created with `#info[...]`
]

#success[
  *Success Box* — Confirmations. Created with `#success[...]`
]

#warning[
  *Warning Box* — Cautions. Created with `#warning[...]`
]

#error[
  *Error Box* — Critical errors. Created with `#error[...]`
]

#tip[
  *Tip Box* — Suggestions. Created with `#tip[...]`
]

#memo[
  *Memo Box* — Notes. Created with `#memo[...]`
]

#question[
  *Question Box* — Uncertainties. Created with `#question[...]`
]

#example[
  *Example Box* — Demonstrations. Created with `#example[...]`
]

#pagebreak()

// ============================================================================
// 2. ZERO - Scientific Number Formatting
// ============================================================================

= 2. zero — Scientific Number Formatting

#text(size: 9pt, fill: gray)[
  `#import "@preview/zero:0.5.0": num, zi`
]

#v(0.2in)

== Live Demonstrations

=== Basic Numbers with `num`

#table(
  columns: (1fr, 1fr),
  stroke: 0.5pt + gray,
  
  table.header([*Code*], [*Live Output*]),
  
  [`#num[1234567]`], [#num[1234567]],
  [`#num[3.14159265]`], [#num[3.14159265]],
  [`#num[6.022e23]`], [#num[6.022e23]],
  [`#num[1.38e-23]`], [#num[1.38e-23]],
  [`#num[299792458]`], [#num[299792458]],
)

=== Uncertainties

#table(
  columns: (1fr, 1fr),
  stroke: 0.5pt + gray,
  
  table.header([*Code*], [*Live Output*]),
  
  [`#num("9.81+-0.02")`], [#num("9.81+-0.02")],
  [`#num("1.602+-0.001e-19")`], [#num("1.602+-0.001e-19")],
  [`#num("2.998(1)e8")`], [#num("2.998(1)e8")],
)

=== Units with `zi` module

#table(
  columns: (1fr, 1fr),
  stroke: 0.5pt + gray,
  
  table.header([*Code*], [*Live Output*]),
  
  [`#zi.s[9.58]`], [#zi.s[9.58]],
  [`#zi.m[100]`], [#zi.m[100]],
  [`#zi.kg[75.5]`], [#zi.kg[75.5]],
  [`#zi.Hz[440]`], [#zi.Hz[440]],
)

=== In-Context Examples

The speed of light is #num[299792458] m/s.

Planck's constant: #num("6.626e-34") J·s

Usain Bolt's 100m record: #zi.s[9.58]

#pagebreak()

// ============================================================================
// 3. LILAQ - Scientific Plotting
// ============================================================================

= 3. lilaq — Scientific Plotting

#text(size: 9pt, fill: gray)[
  `#import "@preview/lilaq:0.5.0" as lq`
]

#v(0.2in)

== Live Demonstrations

=== Basic Line Plot

#align(center)[
  #lq.diagram(
    lq.plot((0, 1, 2, 3, 4, 5), (0, 1, 4, 9, 16, 25))
  )
]

=== Plot with Title and Labels

#let xs = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
#let fitness_best = (0.1, 0.15, 0.25, 0.4, 0.55, 0.65, 0.72, 0.78, 0.82, 0.85, 0.87)
#let fitness_avg = (0.05, 0.08, 0.12, 0.18, 0.25, 0.32, 0.40, 0.48, 0.55, 0.60, 0.64)

#align(center)[
  #lq.diagram(
    title: [Agent Fitness Over Generations],
    xlabel: [Generation],
    ylabel: [Fitness Score],
    lq.plot(xs, fitness_best, label: [Best Agent]),
    lq.plot(xs, fitness_avg, label: [Average]),
  )
]

#pagebreak()

=== Scatter Plot

#let scatter_x = (1, 2, 2.5, 3, 4, 4.5, 5, 6, 7, 8)
#let scatter_y = (2.1, 3.5, 2.8, 5.2, 4.1, 6.3, 5.8, 7.2, 6.5, 8.1)

#align(center)[
  #lq.diagram(
    title: [Parameter Space Exploration],
    xlabel: [Learning Rate],
    ylabel: [Performance],
    lq.scatter(scatter_x, scatter_y),
  )
]

=== Bar Chart

#align(center)[
  #lq.diagram(
    title: [Component Completion],
    xlabel: [Component],
    ylabel: [Completion (%)],
    lq.bar((0, 1, 2, 3, 4), (100, 95, 90, 50, 0)),
  )
]

=== Multiple Series with Legend

#let epochs = (0, 1, 2, 3, 4, 5)
#let loss = (0.9, 0.7, 0.5, 0.35, 0.25, 0.2)
#let accuracy = (0.5, 0.65, 0.75, 0.82, 0.88, 0.91)
#let validation = (0.4, 0.55, 0.68, 0.76, 0.81, 0.84)

#align(center)[
  #lq.diagram(
    title: [Training Metrics],
    xlabel: [Epoch],
    ylabel: [Value],
    lq.plot(epochs, loss, label: [Loss]),
    lq.plot(epochs, accuracy, label: [Accuracy]),
    lq.plot(epochs, validation, label: [Validation]),
  )
]

#pagebreak()

// ============================================================================
// 4. TABLEX - Advanced Tables
// ============================================================================

= 4. tablex — Advanced Tables

#text(size: 9pt, fill: gray)[
  `#import "@preview/tablex:0.0.9": tablex, cellx, rowspanx, colspanx`
]

#v(0.2in)

== Live Demonstrations

=== Styled Header Table

#figure(
  tablex(
    columns: (auto, 1fr, auto, auto),
    align: (center, left, right, center),
    auto-vlines: false,
    
    cellx(fill: rgb("#1976d2"))[#text(fill: white, weight: "bold")[ID]],
    cellx(fill: rgb("#1976d2"))[#text(fill: white, weight: "bold")[Component]],
    cellx(fill: rgb("#1976d2"))[#text(fill: white, weight: "bold")[Value]],
    cellx(fill: rgb("#1976d2"))[#text(fill: white, weight: "bold")[Status]],
    
    [1], [Genome System], [95%], [✅],
    [2], [Flight Recorder], [85%], [✅],
    [3], [Multi-Agent], [50%], [⚠️],
    [4], [Evolutionary Cycle], [0%], [❌],
  ),
  caption: [Component Status Table]
)

=== Row and Column Spans

#figure(
  tablex(
    columns: (auto, auto, auto, auto),
    align: center,
    
    cellx(fill: rgb("#e3f2fd"), colspan: 4)[#text(weight: "bold")[WAFT Framework Components]],
    
    cellx(fill: rgb("#f5f5f5"), rowspan: 2)[*Core*],
    [Genome], [SHA-256], [✅],
    [Pantheon], [Beings], [✅],
    
    cellx(fill: rgb("#f5f5f5"), rowspan: 2)[*Tools*],
    [Empirica], [External], [✅],
    [Flight Rec], [Telemetry], [✅],
  ),
  caption: [Table with Spans]
)

#pagebreak()

// ============================================================================
// 5. FLETCHER - Diagrams
// ============================================================================

= 5. fletcher — Diagrams with Nodes & Edges

#text(size: 9pt, fill: gray)[
  `#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge`
]

#v(0.2in)

== Live Demonstrations

=== Simple Flowchart

#align(center)[
  #diagram(
    node-stroke: 1pt,
    edge-stroke: 1pt,
    node((0, 0), [Input], shape: rect, fill: rgb("#e3f2fd")),
    edge("->"),
    node((1, 0), [Process], shape: rect, fill: rgb("#fff3e0")),
    edge("->"),
    node((2, 0), [Output], shape: rect, fill: rgb("#e8f5e9")),
  )
]

=== Agent Architecture

#align(center)[
  #diagram(
    node-stroke: 1pt,
    edge-stroke: 1pt,
    spacing: (15pt, 20pt),
    
    node((1, 0), [*Orchestrator*], shape: rect, fill: rgb("#1976d2"), stroke: rgb("#1976d2")),
    
    node((0, 1), [Agent A], shape: rect, fill: rgb("#e3f2fd")),
    node((1, 1), [Agent B], shape: rect, fill: rgb("#e3f2fd")),
    node((2, 1), [Agent C], shape: rect, fill: rgb("#e3f2fd")),
    
    node((1, 2), [*Shared Memory*], shape: rect, fill: rgb("#fff3e0")),
    
    edge((1, 0), (0, 1), "->"),
    edge((1, 0), (1, 1), "->"),
    edge((1, 0), (2, 1), "->"),
    
    edge((0, 1), (1, 2), "<->"),
    edge((1, 1), (1, 2), "<->"),
    edge((2, 1), (1, 2), "<->"),
  )
]

=== Data Pipeline

#align(center)[
  #diagram(
    node-stroke: 1pt,
    edge-stroke: 1pt,
    
    node((0, 0), [Raw Data], shape: rect, fill: rgb("#ffcdd2")),
    edge("->", label: "clean"),
    node((1, 0), [Cleaned], shape: rect, fill: rgb("#fff9c4")),
    edge("->", label: "transform"),
    node((2, 0), [Features], shape: rect, fill: rgb("#c8e6c9")),
    edge("->", label: "train"),
    node((3, 0), [Model], shape: rect, fill: rgb("#bbdefb")),
  )
]

#pagebreak()

=== Decision Tree

#align(center)[
  #diagram(
    node-stroke: 1pt,
    edge-stroke: 1pt,
    spacing: (12pt, 25pt),
    
    node((1, 0), [Start], shape: circle, fill: rgb("#e8f5e9")),
    node((1, 1), [Condition?], shape: rect, fill: rgb("#fff3e0")),
    node((0, 2), [Yes Path], shape: rect, fill: rgb("#e3f2fd")),
    node((2, 2), [No Path], shape: rect, fill: rgb("#e3f2fd")),
    node((1, 3), [End], shape: circle, fill: rgb("#ffcdd2")),
    
    edge((1, 0), (1, 1), "->"),
    edge((1, 1), (0, 2), "->", label: "Yes"),
    edge((1, 1), (2, 2), "->", label: "No"),
    edge((0, 2), (1, 3), "->"),
    edge((2, 2), (1, 3), "->"),
  )
]

=== WAFT Evolution Cycle

#align(center)[
  #diagram(
    node-stroke: 1pt,
    edge-stroke: 1pt,
    spacing: (20pt, 15pt),
    
    node((0, 0), [*Population*], shape: rect, fill: rgb("#e3f2fd")),
    edge("->", label: "evaluate"),
    node((1, 0), [*Fitness*], shape: rect, fill: rgb("#fff3e0")),
    edge("->", label: "select"),
    node((2, 0), [*Parents*], shape: rect, fill: rgb("#e8f5e9")),
    
    edge((2, 0), (2, 1), "->", label: "mutate"),
    node((2, 1), [*Offspring*], shape: rect, fill: rgb("#fce4ec")),
    edge((2, 1), (0, 1), "->", label: "replace"),
    node((0, 1), [*New Pop*], shape: rect, fill: rgb("#e3f2fd")),
    edge((0, 1), (0, 0), "->", label: "repeat"),
  )
]

#pagebreak()

// ============================================================================
// 6. COMBINED EXAMPLE
// ============================================================================

= 6. Combined Example — All Packages Together

#info[
  This section demonstrates using *multiple packages together* in a single document.
]

== WAFT Framework Status Report

#figure(
  tablex(
    columns: (auto, 1fr, auto, auto),
    align: (center, left, right, center),
    auto-vlines: false,
    
    cellx(fill: rgb("#1976d2"))[#text(fill: white, weight: "bold")[ID]],
    cellx(fill: rgb("#1976d2"))[#text(fill: white, weight: "bold")[Component]],
    cellx(fill: rgb("#1976d2"))[#text(fill: white, weight: "bold")[Completion]],
    cellx(fill: rgb("#1976d2"))[#text(fill: white, weight: "bold")[Status]],
    
    [1], [Empirica Integration], [#num[100]%], [✅],
    [2], [Genome System], [#num[95]%], [✅],
    [3], [RPG Gym (Scint)], [#num[90]%], [✅],
    [4], [Pantheon Architecture], [#num[90]%], [✅],
    [5], [Flight Recorder], [#num[85]%], [✅],
    [6], [Multi-Agent], [#num[50]%], [⚠️],
    [7], [Mutation Operators], [#num[40]%], [⚠️],
    [8], [Evolutionary Cycle], [#num[0]%], [❌],
  ),
  caption: [WAFT Implementation Status (with zero formatting)]
)

#v(0.2in)

== Progress Visualization (lilaq)

#let components = (0, 1, 2, 3, 4, 5, 6, 7)
#let completion = (100, 95, 90, 90, 85, 50, 40, 0)

#align(center)[
  #lq.diagram(
    title: [WAFT Component Completion],
    xlabel: [Component Index],
    ylabel: [Completion (%)],
    lq.bar(components, completion),
  )
]

#pagebreak()

== System Architecture (fletcher)

#align(center)[
  #diagram(
    node-stroke: 1pt,
    edge-stroke: 1pt,
    spacing: (18pt, 18pt),
    
    // Top: User
    node((1, 0), [*User*], shape: circle, fill: rgb("#e8f5e9")),
    
    // Middle: WAFT Core
    node((1, 1), [*WAFT Core*], shape: rect, fill: rgb("#1976d2"), stroke: rgb("#1976d2")),
    
    // Components
    node((0, 2), [Genome], shape: rect, fill: rgb("#e3f2fd")),
    node((1, 2), [Pantheon], shape: rect, fill: rgb("#e3f2fd")),
    node((2, 2), [Scint Gym], shape: rect, fill: rgb("#e3f2fd")),
    
    // Bottom: External
    node((0, 3), [Empirica], shape: rect, fill: rgb("#fff3e0")),
    node((2, 3), [Flight Rec], shape: rect, fill: rgb("#fff3e0")),
    
    // Connections
    edge((1, 0), (1, 1), "<->"),
    edge((1, 1), (0, 2), "->"),
    edge((1, 1), (1, 2), "->"),
    edge((1, 1), (2, 2), "->"),
    edge((0, 2), (0, 3), "<->"),
    edge((2, 2), (2, 3), "<->"),
  )
]

#v(0.2in)

#success[
  *All visualizations above are LIVE* — generated by the actual Typst packages, not screenshots or simulations.
]

#pagebreak()

// ============================================================================
// 7. CODE REFERENCE
// ============================================================================

= 7. Import Cheatsheet

```typst
// Callouts
#import "@preview/gentle-clues:1.2.0": *

// Scientific numbers and units
#import "@preview/zero:0.5.0": num, zi

// Scientific plotting
#import "@preview/lilaq:0.5.0" as lq

// Diagrams
#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge

// Advanced tables
#import "@preview/tablex:0.0.9": tablex, cellx, rowspanx, colspanx
```

== Quick Examples

=== zero
```typst
#num[299792458]        // formatted number
#num("9.81+-0.02")     // with uncertainty
#zi.s[9.58]            // with unit (seconds)
```

=== lilaq
```typst
#lq.diagram(
  title: [My Plot],
  xlabel: [X], ylabel: [Y],
  lq.plot((0,1,2,3), (0,1,4,9), label: [Data]),
)
```

=== fletcher
```typst
#diagram(
  node((0,0), [A], shape: rect),
  edge("->"),
  node((1,0), [B], shape: rect),
)
```

#v(0.5in)

#align(center)[
  #rect(fill: rgb("#1976d2"), inset: 20pt, radius: 8pt)[
    #text(fill: white, size: 12pt, weight: "bold")[
      Every visualization in this PDF is REAL.
    ]
  ]
]

#align(center)[
  #text(size: 9pt, fill: gray)[
    Generated: #datetime.today().display() \
    Source: Typst Universe (typst.app/universe)
  ]
]
