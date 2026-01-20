#import "@preview/aero-check:0.1.1": *
#import "@preview/umbra:0.1.1": shadow-path

// Neumorphic checklist template - soft, modern design
#set page(margin: 2.5cm, paper: "a4", fill: rgb("f0f0f0"))

// Neumorphic title
#align(center)[
  #shadow-path(
    (3%, 3%), (3%, 97%), (97%, 97%), (97%, 3%),
    closed: true,
    shadow-radius: 0.15cm,
    shadow-stops: (rgb("e0e0e0"), rgb("ffffff")),
    correction: 2deg
  )
  #pad(x: 3.5cm, y: 1.8cm)[
    #text(size: 28pt, weight: "bold", fill: rgb("4a4a4a"))[
      Neumorphic Checklist
    ]
    #v(0.3cm)
    #text(size: 12pt, fill: rgb("888888"))[
      Soft shadows, modern design
    ]
  ]
]

#v(1.2cm)

// Use aero-check with custom styling
#show: checklist.with(
  title: "",
  disclaimer: "",
  style: 1,
)

#topic("Daily Routine")[
  #section("Morning")[
    #step("Wake up and hydrate", "Check")
    #step("Morning meditation or exercise", "Check")
    #step("Healthy breakfast", "Check")
    #step("Review daily goals", "Check")
  ]
  
  #section("Work Focus")[
    #step("Prioritize top 3 tasks", "Check")
    #step("Deep work session (2-3 hours)", "Check")
    #step("Take regular breaks", "Check")
    #step("Review progress mid-day", "Check")
  ]
]

#colbreak()

#topic("Evening")[
  #section("Wind Down")[
    #step("Complete remaining tasks", "Check")
    #step("Plan tomorrow's priorities", "Check")
    #step("Evening routine (dinner, relax)", "Check")
    #step("Prepare for next day", "Check")
  ]
  
  #section("Reflection")[
    #step("Journal or reflect on day", "Check")
    #step("Gratitude practice", "Check")
    #step("Quality sleep preparation", "Check")
  ]
]

// Neumorphic info boxes
#v(1.5cm)

#grid(
  columns: 2,
  gutter: 1cm,
  [
    #align(center)[
      #shadow-path(
        (5%, 5%), (5%, 95%), (95%, 95%), (95%, 5%),
        closed: true,
        shadow-radius: 0.2cm,
        shadow-stops: (rgb("d0d0d0"), rgb("ffffff")),
        correction: 3deg
      )
      #pad(x: 1.2cm, y: 0.8cm)[
        #text(size: 11pt, weight: "bold", fill: rgb("555555"))[💡 Tip]
        #v(0.2cm)
        #text(size: 9pt, fill: rgb("777777"))[
          Neumorphism uses soft shadows to create depth without harsh lines.
        ]
      ]
    ]
  ],
  [
    #align(center)[
      #shadow-path(
        (5%, 5%), (5%, 95%), (95%, 95%), (95%, 5%),
        closed: true,
        shadow-radius: 0.2cm,
        shadow-stops: (rgb("d0d0d0"), rgb("ffffff")),
        correction: 3deg
      )
      #pad(x: 1.2cm, y: 0.8cm)[
        #text(size: 11pt, weight: "bold", fill: rgb("555555"))[✨ Design]
        #v(0.2cm)
        #text(size: 9pt, fill: rgb("777777"))[
          Light backgrounds work best for neumorphic effects.
        ]
      ]
    ]
  ]
)
