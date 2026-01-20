#import "@preview/aero-check:0.1.1": *

#show: checklist.with(
  title: "Cessna 172 Pre-Flight Inspection",
  disclaimer: "Complete all items before engine start. Do not skip steps.",
  style: 0,
)

#topic("Exterior Inspection")[
  #section("Fuselage & Control Surfaces")[
    #step("Check for visible damage or loose panels", "Check")
    #step("Verify all control surfaces move freely", "Check")
    #step("Inspect landing gear for proper extension", "Check")
    #step("Check tire pressure and condition", "Check")
    #step("Verify pitot tube cover removed", "Check")
  ]
  
  #section("Engine & Propeller")[
    #step("Check oil level (6-8 quarts)", "Check")
    #step("Inspect propeller for nicks or damage", "Check")
    #step("Check fuel sump for water/contamination", "Check")
    #step("Verify fuel caps secure and vented", "Check")
    #step("Check engine cowling secure", "Check")
  ]
]

#colbreak()

#topic("Cockpit Preparation")[
  #section("Pre-Start Checks")[
    #step("Set parking brake", "Check")
    #step("Master switch ON", "Check")
    #step("Check fuel quantity (both tanks)", "Check")
    #step("Verify circuit breakers in", "Check")
    #step("Set altimeter to field elevation", "Check")
  ]
  
  #section("Engine Start")[
    #step("Mixture RICH", "Check")
    #step("Throttle 1/4 inch", "Check")
    #step("Master ON, Starter ON", "Check")
    #step("Verify oil pressure within 10 seconds", "Check")
    #step("Check ammeter shows charge", "Check")
  ]
]

#topic("Before Takeoff")[
  #section("Runup Checks")[
    #step("Magnetos check (max 150 RPM drop)", "Check")
    #step("Carb heat check (100-150 RPM drop)", "Check")
    #step("Flight controls free and correct", "Check")
    #step("Trim set for takeoff", "Check")
    #step("Seatbelts and harnesses secure", "Check")
  ]
]
