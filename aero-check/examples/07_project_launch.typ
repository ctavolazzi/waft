#import "@preview/aero-check:0.1.1": *

#show: checklist.with(
  title: "New Product Launch Checklist",
  disclaimer: "Coordinate with all teams. Launch date: [DATE]",
  style: 0,
)

#topic("Pre-Launch (4 Weeks)")[
  #section("Product Readiness")[
    #step("Final QA testing completed", "Check")
    #step("Beta user feedback incorporated", "Check")
    #step("Performance benchmarks met", "Check")
    #step("Security audit passed", "Check")
    #step("Documentation finalized", "Check")
  ]
  
  #section("Marketing")[
    #step("Launch announcement drafted", "Check")
    #step("Press kit prepared", "Check")
    #step("Social media content scheduled", "Check")
    #step("Email campaign prepared", "Check")
    #step("Landing page live and tested", "Check")
  ]
]

#colbreak()

#topic("Launch Week")[
  #section("Technical")[
    #step("Production infrastructure scaled", "Check")
    #step("Monitoring and alerts configured", "Check")
    #step("Support team briefed", "Check")
    #step("On-call engineer assigned", "Check")
  ]
  
  #section("Communication")[
    #step("Internal team announcement sent", "Check")
    #step("Customer communication prepared", "Check")
    #step("Press release distributed", "Check")
    #step("Social media posts go live", "Check")
  ]
]

#topic("Launch Day")[
  #section("Go-Live")[
    #step("Final system health check", "Check")
    #step("Feature flags enabled", "Check")
    #step("Monitor error rates and metrics", "Check")
    #step("Support team ready for inquiries", "Check")
    #step("Celebrate with team!", "Check")
  ]
]
