#import "@preview/aero-check:0.1.1": *
#import "@preview/umbra:0.1.1": shadow-path

#show: checklist.with(
  title: "Neumorphic Design Checklist",
  disclaimer: "Demonstrating neumorphic design patterns with umbra shadows.",
  style: 1,
)

// Neumorphic title box
#align(center)[
  #shadow-path(
    (2%, 2%), (2%, 98%), (98%, 98%), (98%, 2%),
    closed: true,
    shadow-radius: 0.2cm,
    shadow-stops: (gray.lighten(40%), gray.lighten(60%)),
    correction: 3deg
  )
  #pad(x: 3cm, y: 1.5cm)[
    #text(size: 28pt, weight: "bold", fill: gray.darken(30%))[
      Neumorphic Design
    ]
  ]
]

#v(1.5cm)

#topic("Design Principles")[
  #section("Visual Depth")[
    #step("Use subtle shadows to create elevation", "Check")
    #step("Combine light and dark gradients", "Check")
    #step("Maintain soft, rounded edges", "Check")
    #step("Keep contrast minimal for soft appearance", "Check")
  ]
]

#colbreak()

#topic("Implementation")[
  #section("Umbra Integration")[
    #step("Import umbra package", "Check")
    #step("Define shadow paths with closed shapes", "Check")
    #step("Adjust shadow-radius for depth", "Check")
    #step("Set shadow-stops for gradient colors", "Check")
    #step("Use correction for smooth corners", "Check")
  ]
]

// Neumorphic info boxes
#v(1cm)

#align(center)[
  #shadow-path(
    (5%, 5%), (5%, 95%), (95%, 95%), (95%, 5%),
    closed: true,
    shadow-radius: 0.25cm,
    shadow-stops: (gray.lighten(50%), gray.lighten(70%)),
    correction: 4deg
  )
  #pad(x: 2cm, y: 1cm)[
    #text(size: 12pt, weight: "bold")[Neumorphism]
    #v(0.2cm)
    #text(size: 10pt)[
      A design trend that uses soft shadows to create
      the illusion of depth in flat interfaces.
    ]
  ]
]
