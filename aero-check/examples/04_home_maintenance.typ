#import "@preview/aero-check:0.1.1": *

#show: checklist.with(
  title: "Seasonal Home Maintenance Checklist",
  disclaimer: "Regular maintenance prevents costly repairs. Complete quarterly.",
  style: 1,
)

#topic("Spring Maintenance")[
  #section("Exterior")[
    #step("Inspect roof for winter damage", "Check")
    #step("Clean gutters and downspouts", "Check")
    #step("Check siding for cracks or damage", "Check")
    #step("Service air conditioning unit", "Check")
    #step("Inspect and repair window screens", "Check")
  ]
  
  #section("Interior")[
    #step("Test smoke and CO detectors", "Check")
    #step("Change HVAC filters", "Check")
    #step("Deep clean carpets and rugs", "Check")
    #step("Check for water leaks under sinks", "Check")
    #step("Inspect electrical outlets", "Check")
  ]
]

#colbreak()

#topic("Summer Maintenance")[
  #section("Outdoor")[
    #step("Service lawn mower and equipment", "Check")
    #step("Inspect deck/patio for rot or damage", "Check")
    #step("Check irrigation system", "Check")
    #step("Trim trees near house", "Check")
    #step("Seal driveway cracks", "Check")
  ]
]

#topic("Fall Maintenance")[
  #section("Preparation")[
    #step("Service heating system", "Check")
    #step("Clean chimney and fireplace", "Check")
    #step("Drain and winterize sprinklers", "Check")
    #step("Check weatherstripping on doors", "Check")
    #step("Store outdoor furniture", "Check")
  ]
]

#topic("Winter Maintenance")[
  #section("Protection")[
    #step("Check insulation in attic", "Check")
    #step("Test sump pump if applicable", "Check")
    #step("Inspect pipes for freezing risk", "Check")
    #step("Stock emergency supplies", "Check")
    #step("Review home insurance policy", "Check")
  ]
]
