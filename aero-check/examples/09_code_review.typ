#import "@preview/aero-check:0.1.1": *

#show: checklist.with(
  title: "Code Review Checklist",
  disclaimer: "Review thoroughly. Quality over speed. Be constructive.",
  style: 0,
)

#topic("Functionality")[
  #section("Correctness")[
    #step("Code solves the stated problem", "Check")
    #step("Edge cases are handled", "Check")
    #step("Error handling is appropriate", "Check")
    #step("No obvious bugs or logic errors", "Check")
    #step("Tests cover new functionality", "Check")
  ]
]

#topic("Code Quality")[
  #section("Structure")[
    #step("Code follows project style guide", "Check")
    #step("Functions are focused and single-purpose", "Check")
    #step("Variable names are clear and descriptive", "Check")
    #step("No commented-out code or debug statements", "Check")
    #step("Complex logic is well-documented", "Check")
  ]
]

#colbreak()

#topic("Performance & Security")[
  #section("Optimization")[
    #step("No obvious performance issues", "Check")
    #step("Database queries are efficient", "Check")
    #step("No security vulnerabilities introduced", "Check")
    #step("Sensitive data handled appropriately", "Check")
    #step("Input validation present where needed", "Check")
  ]
]

#topic("Testing")[
  #section("Coverage")[
    #step("Unit tests added/updated", "Check")
    #step("Integration tests pass", "Check")
    #step("Edge cases are tested", "Check")
    #step("Tests are maintainable", "Check")
  ]
]

#topic("Documentation")[
  #section("Clarity")[
    #step("PR description explains changes", "Check")
    #step("Complex code has comments", "Check")
    #step("API changes documented", "Check")
    #step("Breaking changes noted", "Check")
  ]
]
