#import "@preview/s6t5-page-bordering:1.0.0": s6t5-page-bordering

// Cover page design
#set page(margin: 0cm)
#set text(font: "New Computer Modern", size: 10.5pt)

#align(center)[
  #v(3cm)
  
  // Main title area with gradient-like effect
  #block(
    fill: rgb("#1a237e"),
    radius: 0pt,
    inset: 0pt,
    width: 100%,
    height: 8cm,
  )[
    #align(center)[
      #v(2cm)
      #text(
        size: 3.5em,
        weight: "bold",
        fill: white,
      )[Teleport Massive]
      #v(0.5cm)
      #text(
        size: 1.8em,
        fill: rgb("#e3f2fd"),
        style: "italic",
      )[Founding Opportunity]
      #v(0.3cm)
      #text(
        size: 1.2em,
        fill: rgb("#bbdefb"),
      )[Seeking Founding Team & Seed Funding]
    ]
  ]
  
  #v(2cm)
  
  // Subtitle and call to action
  #text(
    size: 1.4em,
    weight: "bold",
    fill: rgb("#1a237e"),
  )[We're Looking for the Initial Group]
  
  #v(0.8cm)
  
  #block(
    fill: rgb("#fff3e0"),
    stroke: (thickness: 2pt, paint: rgb("#ff6f00")),
    radius: 8pt,
    inset: 1cm,
    width: 85%,
  )[
    #align(center)[
      #text(
        size: 1.2em,
        weight: "bold",
        fill: rgb("#e65100"),
      )[Help Us Get This Off the Ground]
      #v(0.5cm)
      #text(
        size: 1em,
        fill: rgb("#424242"),
      )[We're seeking founding team members and seed funding]
      #linebreak()
      #text(
        size: 1em,
        fill: rgb("#424242"),
      )[to scale quantum teleportation from laboratory to reality]
    ]
  ]
  
  #v(0.8cm)
  
  #text(
    size: 1em,
    fill: rgb("#616161"),
    style: "italic",
  )[The Scientific Foundation That Inspires Our Vision]
  
  #v(1.5cm)
  
  // Visual representation of scaling
  #block(
    fill: rgb("#f5f5f5"),
    stroke: (thickness: 2pt, paint: rgb("#1a237e")),
    radius: 8pt,
    inset: 1.2cm,
    width: 80%,
  )[
    #text(weight: "bold", size: 1.1em, fill: rgb("#1a237e"))[Scaling Pathway]
    #v(0.6cm)
    
    #grid(
      columns: 5,
      gutter: 0.4cm,
      [
        #block(
          fill: rgb("#fff3e0"),
          stroke: (thickness: 1.5pt, paint: rgb("#ff6f00")),
          radius: 6pt,
          inset: 0.5cm,
          width: 100%,
        )[
          #align(center)[
            #text(weight: "bold", size: 0.9em)[Particles]
            #v(0.2cm)
            #text(size: 0.75em)[✓ Proven]
          ]
        ]
      ],
      [
        #block(
          fill: rgb("#e8f5e9"),
          stroke: (thickness: 1.5pt, paint: rgb("#2e7d32")),
          radius: 6pt,
          inset: 0.5cm,
          width: 100%,
        )[
          #align(center)[
            #text(weight: "bold", size: 0.9em)[Atoms]
            #v(0.2cm)
            #text(size: 0.75em)[Research]
          ]
        ]
      ],
      [
        #block(
          fill: rgb("#e3f2fd"),
          stroke: (thickness: 1.5pt, paint: rgb("#1976d2")),
          radius: 6pt,
          inset: 0.5cm,
          width: 100%,
        )[
          #align(center)[
            #text(weight: "bold", size: 0.9em)[Chips]
            #v(0.2cm)
            #text(size: 0.75em)[✓ 2026]
          ]
        ]
      ],
      [
        #block(
          fill: rgb("#f3e5f5"),
          stroke: (thickness: 1.5pt, paint: rgb("#7b1fa2")),
          radius: 6pt,
          inset: 0.5cm,
          width: 100%,
        )[
          #align(center)[
            #text(weight: "bold", size: 0.9em)[Devices]
            #v(0.2cm)
            #text(size: 0.75em)[Future]
          ]
        ]
      ],
      [
        #block(
          fill: rgb("#fff9c4"),
          stroke: (thickness: 1.5pt, paint: rgb("#f57f17")),
          radius: 6pt,
          inset: 0.5cm,
          width: 100%,
        )[
          #align(center)[
            #text(weight: "bold", size: 0.9em)[Macro]
            #v(0.2cm)
            #text(size: 0.75em)[Vision]
          ]
        ]
      ]
    )
    
    #v(0.5cm)
    
    #align(center)[
      #text(size: 0.85em, style: "italic", fill: rgb("#616161"))[
        Current State: 64m chip-to-chip teleportation | 78.3% fidelity
      ]
    ]
  ]
  
  #v(1.5cm)
  
  // What we're looking for
  #block(
    fill: rgb("#e8f5e9"),
    stroke: (thickness: 1.5pt, paint: rgb("#2e7d32")),
    radius: 8pt,
    inset: 0.8cm,
    width: 85%,
  )[
    #text(weight: "bold", size: 1em, fill: rgb("#1b5e20"))[We're Looking For:]
    #v(0.4cm)
    #grid(
      columns: 2,
      gutter: 0.6cm,
      [
        #text(size: 0.9em, fill: rgb("#424242"))[
          #text(weight: "bold")[Founding Team Members:]
          #linebreak()
          • Quantum physicists & engineers
          #linebreak()
          • Business & operations leaders
          #linebreak()
          • Legal & compliance experts
          #linebreak()
          • Marketing & brand strategists
        ]
      ],
      [
        #text(size: 0.9em, fill: rgb("#424242"))[
          #text(weight: "bold")[Seed Funding:]
          #linebreak()
          • Pre-seed / Seed stage investors
          #linebreak()
          • Deep tech VCs
          #linebreak()
          • Strategic partners
          #linebreak()
          • Angel investors
        ]
      ]
    )
  ]
  
  #v(1.5cm)
  
  // Footer information
  #block(
    fill: rgb("#f5f5f5"),
    radius: 0pt,
    inset: 0.8cm,
    width: 100%,
  )[
    #align(center)[
      #text(size: 1em, weight: "bold")[Teleport Massive]
      #v(0.3cm)
      #text(size: 0.9em)[Pre-Incorporation | January 2026]
      #linebreak()
      #text(size: 0.9em)[San Francisco, California]
      #v(0.4cm)
      #text(size: 0.85em, style: "italic", fill: rgb("#757575"))[
        Seeking Founding Team & Seed Funding
        #linebreak()
        Confidential - For Prospective Founders & Investors
      ]
    ]
  ]
]
