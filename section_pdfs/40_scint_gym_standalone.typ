// Standalone compilation wrapper for Section 4: Scint Gym
#import "waft_functions.typ": callout, evidence, metric

#set document(
  title: "WAFT Analysis - Scint Gym Section",
  author: "Dr. Aria Vex",
)

#set page(
  paper: "us-letter",
  margin: (x: 1.25in, y: 1in),
  numbering: "1",
  header: context [
    #text(size: 10pt, fill: rgb("#666666"))[
      Section 4: Scint Gym
      #h(1fr)
      #counter(page).display("1")
    ]
    #v(0.05in)
    #line(length: 100%, stroke: 0.5pt + rgb("#cccccc"))
  ],
)

#set text(
  font: "New Computer Modern",
  size: 11pt,
  fill: rgb("#333333"),
)

#set par(justify: true, leading: 0.65em)
#set heading(numbering: "1.1")

#show raw.where(block: true): it => {
  set text(font: "JetBrains Mono", size: 9pt)
  block(
    fill: rgb("#f5f5f5"),
    stroke: 1pt + rgb("#cccccc"),
    radius: 4pt,
    inset: 12pt,
    width: 100%,
    it
  )
}

#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  block(
    width: 100%,
    fill: rgb("#1976d2"),
    inset: 16pt,
    radius: 4pt,
    text(fill: white, size: 20pt, weight: "bold", it.body)
  )
  v(0.3in)
}

#show heading.where(level: 2): it => {
  v(0.2in)
  block(
    width: 100%,
    text(fill: rgb("#1976d2"), size: 16pt, weight: "bold")[
      #counter(heading).display() #it.body
    ]
  )
  line(length: 100%, stroke: 2pt + rgb("#1976d2"))
  v(0.1in)
}

// Load section content
#include "sections/40_scint_gym.typ"
