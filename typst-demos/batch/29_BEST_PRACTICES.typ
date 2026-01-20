// WAFT BEST PRACTICES
// Guidelines for Successful Evolution

#import "@preview/showybox:2.0.4": showybox

#set document(title: "Best Practices", author: "WAFT Development Team")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#let primary = rgb("#805ad5")

#align(center)[
  #rect(fill: gradient.linear(primary, primary.darken(30%)), width: 100%, inset: 2em)[
    #text(fill: white, size: 24pt, weight: "bold")[BEST PRACTICES]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 12pt)[WAFT | Guidelines for Successful Evolution]
  ]
]

#v(1em)

= Project Setup

#showybox(frame: (border-color: blue, body-color: blue.lighten(95%)), title: "DO")[
  - ✓ Use `waft new` to create projects
  - ✓ Run `waft verify` before starting
  - ✓ Configure version control (git)
  - ✓ Set up checkpointing early
]

#showybox(frame: (border-color: red, body-color: red.lighten(95%)), title: "DON'T")[
  - ✗ Manually create directory structure
  - ✗ Skip verification steps
  - ✗ Run evolution without backups
  - ✗ Ignore Flight Recorder setup
]

= Agent Design

#showybox(frame: (border-color: blue, body-color: blue.lighten(95%)), title: "DO")[
  - ✓ Start with simple base agents
  - ✓ Mark mutable regions clearly
  - ✓ Add error handling
  - ✓ Test agents before evolution
]

#showybox(frame: (border-color: red, body-color: red.lighten(95%)), title: "DON'T")[
  - ✗ Start with complex agents
  - ✗ Hard-code everything
  - ✗ Skip validation
  - ✗ Ignore Scint types
]

= Evolution Configuration

#showybox(frame: (border-color: blue, body-color: blue.lighten(95%)), title: "DO")[
  - ✓ Start with small populations (10-20)
  - ✓ Use conservative mutation rates (0.1)
  - ✓ Enable elitism (preserve best 2)
  - ✓ Run many generations (50+)
]

#showybox(frame: (border-color: red, body-color: red.lighten(95%)), title: "DON'T")[
  - ✗ Start with huge populations
  - ✗ Use extreme mutation (>0.3)
  - ✗ Disable elitism entirely
  - ✗ Expect results in 5 generations
]

= Monitoring

#showybox(frame: (border-color: blue, body-color: blue.lighten(95%)), title: "DO")[
  - ✓ Check fitness trends regularly
  - ✓ Review Flight Recorder logs
  - ✓ Watch for plateaus
  - ✓ Analyze mutation impact
]

#showybox(frame: (border-color: red, body-color: red.lighten(95%)), title: "DON'T")[
  - ✗ Run evolution blind
  - ✗ Ignore declining fitness
  - ✗ Let plateaus continue indefinitely
  - ✗ Skip post-evolution analysis
]

= Scientific Rigor

#showybox(frame: (border-color: primary, body-color: primary.lighten(95%)))[
  WAFT produces scientific data. Treat it accordingly:
  
  1. *Document everything* — Use Empirica sessions
  2. *Control variables* — Change one thing at a time
  3. *Replicate results* — Run experiments multiple times
  4. *Share findings* — Contribute to the community
]

#v(1em)

#align(center)[
  #rect(fill: primary, inset: 1em)[
    #text(fill: white)[BEST PRACTICES | Evolution Done Right]
  ]
]
