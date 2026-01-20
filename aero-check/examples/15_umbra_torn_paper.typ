#import "@preview/aero-check:0.1.1": *
#import "@preview/umbra:0.1.1": shadow-path

#show: checklist.with(
  title: "Torn Paper Effect Checklist",
  disclaimer: "Using umbra to create torn paper edge effects.",
  style: 0,
)

// Torn paper effect at top
#align(center)[
  #shadow-path(
    (0%, 0%), (5%, 2%), (10%, 0%), (15%, 3%), (20%, 1%),
    (25%, 2%), (30%, 0%), (35%, 2%), (40%, 1%), (45%, 3%),
    (50%, 0%), (55%, 2%), (60%, 1%), (65%, 3%), (70%, 0%),
    (75%, 2%), (80%, 1%), (85%, 3%), (90%, 0%), (95%, 2%), (100%, 0%),
    closed: false,
    shadow-radius: 0.15cm,
    shadow-stops: (gray.darken(10%), white),
    correction: 2deg
  )
]

#v(0.5cm)

#topic("Paper Effects")[
  #section("Torn Edges")[
    #step("Create irregular vertex paths for torn look", "Check")
    #step("Use small shadow-radius for subtle effect", "Check")
    #step("Apply to top or bottom edges", "Check")
    #step("Combine with paper texture backgrounds", "Check")
  ]
  
  #section("Applications")[
    #step("Vintage document styling", "Check")
    #step("Handwritten note aesthetics", "Check")
    #step("Scrapbook design elements", "Check")
    #step("Artistic document borders", "Check")
  ]
]

#colbreak()

#topic("Advanced Techniques")[
  #section("Customization")[
    #step("Adjust vertex positions for different tear patterns", "Check")
    #step("Vary shadow-radius for depth", "Check")
    #step("Experiment with shadow-stops colors", "Check")
    #step("Use multiple shadow paths for layered effects", "Check")
  ]
]

// Torn edge at bottom
#v(2cm)
#align(center)[
  #shadow-path(
    (0%, 0%), (3%, 2%), (8%, 1%), (12%, 3%), (18%, 0%),
    (25%, 2%), (32%, 1%), (38%, 2%), (45%, 0%), (52%, 3%),
    (58%, 1%), (65%, 2%), (72%, 0%), (78%, 3%), (85%, 1%),
    (92%, 2%), (100%, 0%),
    closed: false,
    shadow-radius: 0.15cm,
    shadow-stops: (gray.darken(10%), white),
    correction: 2deg
  )
]
