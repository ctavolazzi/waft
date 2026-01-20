#import "@preview/aero-check:0.1.1": *
#import "@preview/umbra:0.1.1": shadow-path

// Premium checklist with layered shadows and enhanced visual hierarchy
#set page(margin: 1.5cm, paper: "a4")

// Premium header with multiple shadow layers
#align(center)[
  // Outer shadow
  #shadow-path(
    (0%, 0%), (0%, 100%), (100%, 100%), (100%, 0%),
    closed: true,
    shadow-radius: 0.6cm,
    shadow-stops: (rgb("1a1a2e").lighten(10%), rgb("1a1a2e")),
    correction: 5deg
  )
  #pad(x: 0.3cm, y: 0.3cm)[
    // Inner content box
    #shadow-path(
      (0%, 0%), (0%, 100%), (100%, 100%), (100%, 0%),
      closed: true,
      shadow-radius: 0.3cm,
      shadow-stops: (rgb("16213e"), rgb("0f3460")),
      correction: 5deg
    )
    #pad(x: 2.8cm, y: 1.6cm)[
      #text(size: 36pt, weight: "bold", fill: white)[
        Premium Checklist
      ]
      #v(0.4cm)
      #text(size: 14pt, fill: rgb("e94560"))[
        Professional Design with Enhanced Visual Depth
      ]
    ]
  ]
]

#v(1.8cm)

// Use aero-check structure
#show: checklist.with(
  title: "",
  disclaimer: "Premium template combining structure and aesthetics",
  style: 0,
)

#topic("Strategic Planning")[
  // Shadowed section header
  #align(left)[
    #shadow-path(
      (0%, 0%), (0%, 100%), (85%, 100%), (85%, 0%),
      closed: true,
      shadow-radius: 0.2cm,
      shadow-stops: (rgb("e94560").lighten(15%), rgb("e94560")),
      correction: 3deg
    )
    #pad(x: 1.2cm, y: 0.5cm)[
      #text(size: 18pt, weight: "bold", fill: white)[
        Phase 1: Foundation
      ]
    ]
  ]
  #v(0.6cm)
  
  #section("Analysis")[
    #step("Market research and analysis", "Check")
    #step("Competitive landscape review", "Check")
    #step("SWOT analysis completion", "Check")
    #step("Stakeholder identification", "Check")
  ]
  
  #section("Strategy")[
    #step("Define strategic objectives", "Check")
    #step("Develop action plan", "Check")
    #step("Allocate resources", "Check")
    #step("Set key performance indicators", "Check")
  ]
]

#colbreak()

#topic("Execution")[
  #align(left)[
    #shadow-path(
      (0%, 0%), (0%, 100%), (85%, 100%), (85%, 0%),
      closed: true,
      shadow-radius: 0.2cm,
      shadow-stops: (rgb("0f3460").lighten(20%), rgb("0f3460")),
      correction: 3deg
    )
    #pad(x: 1.2cm, y: 0.5cm)[
      #text(size: 18pt, weight: "bold", fill: white)[
        Phase 2: Implementation
      ]
    ]
  ]
  #v(0.6cm)
  
  #section("Development")[
    #step("Execute planned activities", "Check")
    #step("Monitor progress regularly", "Check")
    #step("Adjust strategy as needed", "Check")
    #step("Maintain team alignment", "Check")
  ]
  
  #section("Quality")[
    #step("Conduct quality reviews", "Check")
    #step("Gather stakeholder feedback", "Check")
    #step("Implement improvements", "Check")
    #step("Document lessons learned", "Check")
  ]
]

#topic("Completion")[
  #align(left)[
    #shadow-path(
      (0%, 0%), (0%, 100%), (85%, 100%), (85%, 0%),
      closed: true,
      shadow-radius: 0.2cm,
      shadow-stops: (rgb("533483").lighten(20%), rgb("533483")),
      correction: 3deg
    )
    #pad(x: 1.2cm, y: 0.5cm)[
      #text(size: 18pt, weight: "bold", fill: white)[
        Phase 3: Delivery
      ]
    ]
  ]
  #v(0.6cm)
  
  #section("Finalization")[
    #step("Complete all deliverables", "Check")
    #step("Final quality assurance", "Check")
    #step("Prepare presentation materials", "Check")
    #step("Schedule review meeting", "Check")
  ]
]

// Premium footer
#v(2cm)
#align(center)[
  #shadow-path(
    (2%, 2%), (2%, 98%), (98%, 98%), (98%, 2%),
    closed: true,
    shadow-radius: 0.4cm,
    shadow-stops: (rgb("1a1a2e").lighten(15%), rgb("1a1a2e")),
    correction: 5deg
  )
  #pad(x: 2.5cm, y: 1.2cm)[
    #text(size: 13pt, weight: "bold", fill: rgb("e94560"))[
      ✓ Premium Template Ready
    ]
    #v(0.4cm)
    #text(size: 10pt, fill: white.lighten(30%))[
      Combining aero-check's structured checklist system
      with umbra's sophisticated shadow effects
    ]
  ]
]
