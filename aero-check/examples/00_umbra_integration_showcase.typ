#import "@preview/aero-check:0.1.1": *
#import "@preview/umbra:0.1.1": shadow-path

#show: checklist.with(
  title: "Package Integration Showcase: Umbra",
  disclaimer: "Demonstrating umbra package for gradient shadows in aero-check templates.",
  style: 0,
)

// Header with shadow effect
#align(center)[
  #shadow-path(
    (5%, 5%), (5%, 95%), (95%, 95%), (95%, 5%),
    closed: true,
    shadow-radius: 0.4cm,
    shadow-stops: (blue.lighten(10%), white),
    correction: 5deg
  )
  #pad(x: 2.5cm, y: 1.2cm)[
    #text(size: 22pt, weight: "bold", fill: blue.darken(20%))[
      Umbra Package Integration
    ]
    #v(0.3cm)
    #text(size: 11pt, fill: gray.darken(30%))[
      Gradient shadows for enhanced visual depth
    ]
  ]
]

#v(1cm)

#topic("Package Overview")[
  #section("What is Umbra?")[
    #step("Library for drawing gradient shadows in Typst", "Check")
    #step("Creates shadows along path edges", "Check")
    #step("Supports custom shadow radius and colors", "Check")
    #step("Perfect for adding depth to flat designs", "Check")
  ]
  
  #section("Key Features")[
    #step("shadow-radius: Controls shadow size (default 0.5cm)", "Check")
    #step("shadow-stops: Gradient colors (default gray to white)", "Check")
    #step("correction: Corner rounding factor (default 5deg)", "Check")
    #step("Works with any closed or open path", "Check")
  ]
]

#colbreak()

#topic("Integration Examples")[
  #section("Basic Shadows")[
    #step("Simple rectangular shadows for boxes", "Check")
    #step("Highlight important sections", "Check")
    #step("Create visual hierarchy", "Check")
  ]
  
  #section("Advanced Effects")[
    #step("Neumorphic design patterns", "Check")
    #step("Torn paper edge effects", "Check")
    #step("Custom decorative borders", "Check")
    #step("Layered shadow compositions", "Check")
  ]
]

#topic("Usage Tips")[
  #section("Best Practices")[
    #step("Use subtle shadows for professional look", "Check")
    #step("Match shadow colors to document theme", "Check")
    #step("Adjust radius based on document size", "Check")
    #step("Reverse vertex order if shadow wrong direction", "Check")
  ]
]

// Example callout with shadow
#v(1cm)
#align(center)[
  #shadow-path(
    (10%, 10%), (10%, 90%), (90%, 90%), (90%, 10%),
    closed: true,
    shadow-radius: 0.3cm,
    shadow-stops: (green.lighten(20%), white),
    correction: 5deg
  )
  #pad(x: 1.8cm, y: 1cm)[
    #text(size: 13pt, weight: "bold", fill: green.darken(30%))[✓ Integration Complete]
    #v(0.3cm)
    #text(size: 10pt)[
      Umbra is now integrated and ready to use!
      See examples 13-15 for more demonstrations.
    ]
  ]
]
