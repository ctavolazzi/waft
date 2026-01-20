#import "@preview/aero-check:0.1.1": *
#import "@preview/umbra:0.1.1": shadow-path

#show: checklist.with(
  title: "Enhanced Checklist with Umbra Shadows",
  disclaimer: "This example demonstrates umbra package integration for visual depth.",
  style: 0,
)

// Create a shadowed box around the title area
#align(center)[
  #shadow-path(
    (5%, 5%), (5%, 95%), (95%, 95%), (95%, 5%),
    closed: true,
    shadow-radius: 0.3cm,
    shadow-stops: (gray.darken(20%), white),
    correction: 5deg
  )
  #pad(x: 2cm, y: 1cm)[
    #text(size: 24pt, weight: "bold")[Visual Enhancement Demo]
    #v(0.5cm)
    #text(size: 12pt)[Umbra shadows add depth and visual interest]
  ]
]

#v(1cm)

#topic("Enhanced Sections")[
  #section("Shadow Effects")[
    #step("Umbra provides gradient shadows along path edges", "Check")
    #step("Shadows can be customized with radius and colors", "Check")
    #step("Perfect for creating depth in flat designs", "Check")
    #step("Works with any closed path shape", "Check")
  ]
  
  #section("Visual Applications")[
    #step("Highlight important sections", "Check")
    #step("Create neumorphic design elements", "Check")
    #step("Add depth to borders and frames", "Check")
    #step("Enhance readability with subtle shadows", "Check")
  ]
]

#colbreak()

#topic("Technical Details")[
  #section("Configuration")[
    #step("shadow-radius: Controls shadow size (default 0.5cm)", "Check")
    #step("shadow-stops: Gradient colors (default gray to white)", "Check")
    #step("correction: Corner rounding factor (default 5deg)", "Check")
    #step("Vertex order defines shadow direction", "Check")
  ]
]

// Example shadowed callout box
#v(1cm)
#align(center)[
  #shadow-path(
    (10%, 10%), (10%, 90%), (90%, 90%), (90%, 10%),
    closed: true,
    shadow-radius: 0.4cm,
    shadow-stops: (blue.lighten(20%), white),
    correction: 5deg
  )
  #pad(x: 1.5cm, y: 1cm)[
    #text(size: 14pt, weight: "bold", fill: blue)[💡 Tip]
    #v(0.3cm)
    #text(size: 11pt)[
      Umbra shadows work best with closed paths.
      Reverse vertex order if shadow appears on wrong side.
    ]
  ]
]
