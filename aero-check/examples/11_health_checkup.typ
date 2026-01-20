#import "@preview/aero-check:0.1.1": *

#show: checklist.with(
  title: "Annual Health Checkup Preparation",
  disclaimer: "Complete before appointment. Bring insurance card and ID.",
  style: 0,
)

#topic("Pre-Appointment")[
  #section("Information Gathering")[
    #step("List current medications and dosages", "Check")
    #step("Note any new symptoms or concerns", "Check")
    #step("Review family medical history updates", "Check")
    #step("Prepare questions for doctor", "Check")
    #step("Gather previous test results", "Check")
  ]
]

#topic("Day Before")[
  #section("Preparation")[
    #step("Confirm appointment time", "Check")
    #step("Fast if blood work scheduled (12 hours)", "Check")
    #step("Avoid alcohol 24 hours before", "Check")
    #step("Get good night's sleep", "Check")
  ]
]

#colbreak()

#topic("Day Of Appointment")[
  #section("What to Bring")[
    #step("Insurance card", "Check")
    #step("Photo ID", "Check")
    #step("List of medications", "Check")
    #step("List of questions/concerns", "Check")
    #step("Previous medical records (if new doctor)", "Check")
  ]
  
  #section("During Appointment")[
    #step("Discuss all concerns openly", "Check")
    #step("Ask about recommended screenings", "Check")
    #step("Understand any new prescriptions", "Check")
    #step("Schedule follow-up if needed", "Check")
    #step("Get copy of visit summary", "Check")
  ]
]

#topic("After Appointment")[
  #section("Follow-Up")[
    #step("Schedule recommended tests", "Check")
    #step("Fill any new prescriptions", "Check")
    #step("Update personal health records", "Check")
    #step("Schedule next annual appointment", "Check")
  ]
]
