#import "@preview/aero-check:0.1.1": *

#show: checklist.with(
  title: "Production Deployment Checklist",
  disclaimer: "All items must be verified before deployment. No exceptions.",
  style: 1,
)

#topic("Pre-Deployment")[
  #section("Code Quality")[
    #step("All tests passing (unit, integration, e2e)", "Check")
    #step("Code review approved by 2+ reviewers", "Check")
    #step("Linter checks passed", "Check")
    #step("Security scan completed (no critical issues)", "Check")
    #step("Performance benchmarks met", "Check")
  ]
  
  #section("Environment Preparation")[
    #step("Database migrations tested in staging", "Check")
    #step("Environment variables documented", "Check")
    #step("Backup of production database created", "Check")
    #step("Rollback plan documented and tested", "Check")
    #step("Monitoring alerts configured", "Check")
  ]
]

#colbreak()

#topic("Deployment")[
  #section("Staging Verification")[
    #step("Deploy to staging environment", "Check")
    #step("Smoke tests pass in staging", "Check")
    #step("Load testing completed", "Check")
    #step("Stakeholder approval received", "Check")
  ]
  
  #section("Production Release")[
    #step("Deploy during maintenance window", "Check")
    #step("Monitor deployment logs", "Check")
    #step("Verify health checks passing", "Check")
    #step("Check error rates (should be < 0.1%)", "Check")
    #step("Confirm feature flags enabled correctly", "Check")
  ]
]

#topic("Post-Deployment")[
  #section("Verification")[
    #step("Key user flows tested", "Check")
    #step("Performance metrics within normal range", "Check")
    #step("No critical errors in logs", "Check")
    #step("Customer support notified of changes", "Check")
    #step("Deployment documentation updated", "Check")
  ]
]
