// WAFT Framework: Evidence-Backed Technical Analysis
// COVER PAGE
// Professional Publication Design

#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge

// Remove all default page settings for cover
#set page(
  paper: "us-letter",
  margin: 0pt,
  header: none,
  footer: none,
  numbering: none,
)

// Full-bleed gradient background
#place(
  top + left,
  dx: 0pt,
  dy: 0pt,
)[
  #rect(
    width: 8.5in,
    height: 11in,
    fill: gradient.linear(
      rgb("#1976d2"),
      rgb("#e3f2fd"),
      angle: 135deg,
    ),
  )
]

// Top section - Logo/branding area
#place(
  top + center,
  dy: 1.5in,
)[
  #text(
    size: 48pt,
    weight: "black",
    fill: white,
    font: "Helvetica Neue",
  )[WAFT]
  
  #v(0.2in)
  
  #text(
    size: 18pt,
    weight: "light",
    fill: white,
    style: "italic",
  )[Wave Agent Framework & Tools]
]

// Main title section
#place(
  top + center,
  dy: 3.5in,
)[
  #rect(
    width: 7in,
    fill: white,
    stroke: none,
    radius: 8pt,
    inset: 24pt,
  )[
    #align(center)[
      #text(
        size: 32pt,
        weight: "bold",
        fill: rgb("#1976d2"),
        font: "Helvetica Neue",
      )[Evidence-Backed]
      
      #v(0.1in)
      
      #text(
        size: 32pt,
        weight: "bold",
        fill: rgb("#1976d2"),
        font: "Helvetica Neue",
      )[Technical Analysis]
      
      #v(0.3in)
      
      #line(length: 4in, stroke: 2pt + rgb("#1976d2"))
      
      #v(0.3in)
      
      #text(
        size: 14pt,
        fill: rgb("#333333"),
        style: "italic",
      )[A Comprehensive Investigation with Source Code Verification]
    ]
  ]
]

// Topology diagram (simplified for cover)
#place(
  top + center,
  dy: 6.5in,
)[
  #diagram(
    spacing: (12mm, 8mm),
    node-stroke: 2pt + rgb("#1976d2"),
    edge-stroke: 2pt + rgb("#1976d2"),
    node-fill: white,
    
    node((0, 0), [*Meta-Framework*], corner-radius: 5pt, width: 30mm),
    
    node((-1, 1), [Genome\ 95%], shape: rect, width: 22mm, fill: rgb("#c8e6c9")),
    node((0, 1), [Pantheon\ 90%], shape: rect, width: 22mm, fill: rgb("#fff9c4")),
    node((1, 1), [Narrative\ 85%], shape: rect, width: 22mm, fill: rgb("#f8bbd0")),
    
    edge((0, 0), (-1, 1), "->"),
    edge((0, 0), (0, 1), "->"),
    edge((0, 0), (1, 1), "->"),
    
    node((0, 2), [Empirica 100%], shape: rect, width: 25mm, fill: rgb("#d1c4e9")),
    
    edge((-1, 1), (0, 2), "->"),
    edge((0, 1), (0, 2), "->"),
    edge((1, 1), (0, 2), "->"),
  )
  
  #v(0.2in)
  
  #align(center)[
    #text(size: 8pt, fill: white)[\* External dependency]
  ]
]

// Bottom section - Author and stats
#place(
  bottom + center,
  dy: -1.5in,
)[
  #rect(
    width: 7in,
    fill: rgb("#333333"),
    stroke: none,
    radius: 8pt,
    inset: 20pt,
  )[
    #align(center)[
      #text(size: 16pt, weight: "bold", fill: white)[
        Dr. Aria Vex
      ]
      
      #v(0.05in)
      
      #text(size: 12pt, fill: rgb("#e0e0e0"))[
        Systems Architecture Analyst
      ]
      
      #v(0.2in)
      
      #text(size: 10pt, fill: white)[
        January 24, 2026
      ]
    ]
  ]
]

// Stats bar at very bottom
#place(
  bottom + left,
  dx: 0.5in,
  dy: -0.5in,
)[
  #grid(
    columns: (1.5in, 1.5in, 1.5in, 1.5in, 1.5in),
    gutter: 0.1in,
    
    // Stat 1
    align(center)[
      #text(size: 24pt, weight: "bold", fill: white)[380]
      #v(-0.1in)
      #text(size: 8pt, fill: white)[Tests Verified]
    ],
    
    // Stat 2
    align(center)[
      #text(size: 24pt, weight: "bold", fill: white)[964]
      #v(-0.1in)
      #text(size: 8pt, fill: white)[Lines Telemetry]
    ],
    
    // Stat 3
    align(center)[
      #text(size: 24pt, weight: "bold", fill: white)[2,876]
      #v(-0.1in)
      #text(size: 8pt, fill: white)[Files Analyzed]
    ],
    
    // Stat 4
    align(center)[
      #text(size: 24pt, weight: "bold", fill: white)[5/5]
      #v(-0.1in)
      #text(size: 8pt, fill: white)[Tests Passing]
    ],
    
    // Stat 5
    align(center)[
      #text(size: 24pt, weight: "bold", fill: white)[0.78]
      #v(-0.1in)
      #text(size: 8pt, fill: white)[Stability Index]
    ],
  )
]

// Version badge (top right corner)
#place(
  top + right,
  dx: -0.5in,
  dy: 0.5in,
)[
  #rect(
    fill: rgb("#4caf50"),
    stroke: none,
    radius: 4pt,
    inset: 8pt,
  )[
    #text(size: 10pt, weight: "bold", fill: white)[
      v2.0 CORRECTED
    ]
  ]
]
