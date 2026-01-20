#import "@preview/aero-check:0.1.1": *

#show: checklist.with(
  title: "Emergency Response Protocol",
  disclaimer: "Follow in order. Safety first. Call 911 if life-threatening.",
  style: 1,
)

#topic("Immediate Response")[
  #section("Assess Situation")[
    #step("Ensure personal safety first", "Check")
    #step("Assess severity of emergency", "Check")
    #step("Identify immediate hazards", "Check")
    #step("Determine if evacuation needed", "Check")
    #step("Call 911 if life-threatening", "Check")
  ]
]

#topic("Fire Emergency")[
  #section("Actions")[
    #step("Pull nearest fire alarm", "Check")
    #step("Evacuate immediately (don't use elevators)", "Check")
    #step("Close doors behind you", "Check")
    #step("Go to designated assembly point", "Check")
    #step("Account for all personnel", "Check")
    #step("Do not re-enter until cleared", "Check")
  ]
]

#colbreak()

#topic("Medical Emergency")[
  #section("Medical Response")[
    #step("Assess victim's condition", "Check")
    #step("Call 911 or medical emergency number", "Check")
    #step("Send someone to meet responders", "Check")
    #step("Provide first aid if trained", "Check")
    #step("Stay with victim until help arrives", "Check")
    #step("Document incident details", "Check")
  ]
]

#topic("Natural Disaster")[
  #section("Severe Weather")[
    #step("Move to designated safe area", "Check")
    #step("Stay away from windows", "Check")
    #step("Monitor emergency communications", "Check")
    #step("Follow evacuation orders if issued", "Check")
    #step("Account for all personnel", "Check")
  ]
]

#topic("Post-Emergency")[
  #section("Aftermath")[
    #step("Ensure all personnel accounted for", "Check")
    #step("Document incident details", "Check")
    #step("Notify management/authorities", "Check")
    #step("Secure area if safe to do so", "Check")
    #step("Conduct post-incident review", "Check")
  ]
]
