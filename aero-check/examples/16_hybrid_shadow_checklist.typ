#import "@preview/aero-check:0.1.1": *
#import "@preview/umbra:0.1.1": shadow-path

// Custom hybrid template combining aero-check structure with umbra shadows
#set page(margin: 2cm, paper: "a4")

// Enhanced title with shadowed header
#align(center)[
  #shadow-path(
    (0%, 0%), (0%, 100%), (100%, 100%), (100%, 0%),
    closed: true,
    shadow-radius: 0.5cm,
    shadow-stops: (blue.darken(15%), blue.lighten(30%)),
    correction: 5deg
  )
  #pad(x: 3cm, y: 1.5cm)[
    #text(size: 32pt, weight: "bold", fill: white)[
      Hybrid Shadow Checklist
    ]
    #v(0.4cm)
    #text(size: 14pt, fill: white.lighten(20%))[
      Combining Aero-Check Structure with Umbra Visual Depth
    ]
  ]
]

#v(1.5cm)

// Use aero-check's checklist system
#show: checklist.with(
  title: "",
  disclaimer: "Enhanced with gradient shadows for visual hierarchy",
  style: 0,
)

// Shadowed topic boxes
#topic("Project Kickoff")[
  // Shadowed section header
  #align(center)[
    #shadow-path(
      (2%, 2%), (2%, 98%), (98%, 98%), (98%, 2%),
      closed: true,
      shadow-radius: 0.25cm,
      shadow-stops: (gray.lighten(40%), gray.lighten(60%)),
      correction: 3deg
    )
    #pad(x: 2cm, y: 0.6cm)[
      #text(size: 16pt, weight: "bold", fill: gray.darken(30%))[
        Initial Planning Phase
      ]
    ]
  ]
  #v(0.5cm)
  
  #section("Team Setup")[
    #step("Assemble core team members", "Check")
    #step("Define roles and responsibilities", "Check")
    #step("Schedule kickoff meeting", "Check")
    #step("Set up communication channels", "Check")
    #step("Establish project timeline", "Check")
  ]
  
  #section("Scope Definition")[
    #step("Document project objectives", "Check")
    #step("Identify key deliverables", "Check")
    #step("Define success criteria", "Check")
    #step("Outline project constraints", "Check")
  ]
]

#colbreak()

#topic("Development Phase")[
  #align(center)[
    #shadow-path(
      (2%, 2%), (2%, 98%), (98%, 98%), (98%, 2%),
      closed: true,
      shadow-radius: 0.25cm,
      shadow-stops: (green.lighten(30%), green.lighten(50%)),
      correction: 3deg
    )
    #pad(x: 2cm, y: 0.6cm)[
      #text(size: 16pt, weight: "bold", fill: green.darken(30%))[
        Active Development
      ]
    ]
  ]
  #v(0.5cm)
  
  #section("Implementation")[
    #step("Set up development environment", "Check")
    #step("Create initial project structure", "Check")
    #step("Implement core features", "Check")
    #step("Write unit tests", "Check")
    #step("Code review and refactoring", "Check")
  ]
  
  #section("Quality Assurance")[
    #step("Run automated test suite", "Check")
    #step("Perform manual testing", "Check")
    #step("Fix identified bugs", "Check")
    #step("Performance optimization", "Check")
  ]
]

#topic("Launch Preparation")[
  #align(center)[
    #shadow-path(
      (2%, 2%), (2%, 98%), (98%, 98%), (98%, 2%),
      closed: true,
      shadow-radius: 0.25cm,
      shadow-stops: (orange.lighten(20%), orange.lighten(40%)),
      correction: 3deg
    )
    #pad(x: 2cm, y: 0.6cm)[
      #text(size: 16pt, weight: "bold", fill: orange.darken(20%))[
        Pre-Launch Checklist
      ]
    ]
  ]
  #v(0.5cm)
  
  #section("Final Checks")[
    #step("Complete documentation", "Check")
    #step("Prepare deployment package", "Check")
    #step("Notify stakeholders", "Check")
    #step("Schedule launch window", "Check")
  ]
]

// Footer with shadowed completion box
#v(2cm)
#align(center)[
  #shadow-path(
    (5%, 5%), (5%, 95%), (95%, 95%), (95%, 5%),
    closed: true,
    shadow-radius: 0.3cm,
    shadow-stops: (purple.lighten(25%), white),
    correction: 5deg
  )
  #pad(x: 2.5cm, y: 1cm)[
    #text(size: 12pt, weight: "bold", fill: purple.darken(25%))[
      ✓ Template Integration Complete
    ]
    #v(0.3cm)
    #text(size: 10pt, fill: gray.darken(20%))[
      This template demonstrates seamless integration of
      aero-check structure with umbra visual enhancements.
    ]
  ]
]
