// THE WAFT MANIFESTO
// Our Vision for Artificial Evolution

#import "@preview/showybox:2.0.4": showybox

#set document(title: "The WAFT Manifesto", author: "WAFT Development Team")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#let primary = rgb("#1a365d")

#align(center)[
  #rect(fill: gradient.linear(rgb("#667eea"), rgb("#764ba2")), width: 100%, inset: 2.5em)[
    #text(fill: white, size: 28pt, weight: "bold")[THE WAFT MANIFESTO]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 14pt)[Our Vision for Artificial Evolution]
  ]
]

#v(2em)

#align(center)[
  #text(size: 16pt, style: "italic", fill: gray.darken(20%))[
    "Don't just build agents. Breed them."
  ]
]

#v(2em)

= We Believe

#showybox(
  frame: (border-color: primary, body-color: primary.lighten(95%)),
)[
  *Intelligence is not designed. Intelligence evolves.*
  
  The most remarkable minds in the universe — human, animal, and perhaps artificial — were not engineered. They emerged through millions of years of evolutionary pressure. We believe the same principle applies to artificial intelligence.
]

= Our Principles

== 1. Evolution Over Engineering

Traditional AI development is engineering: design, build, test, iterate. WAFT takes a different approach: spawn, select, breed, repeat.

We don't know what the best agent looks like. *Evolution discovers what designers cannot imagine.*

== 2. Code as DNA

In WAFT, an agent's source code is its genome. Mutations change the code. Selection chooses which code survives. Over generations, code improves — not because a programmer made it better, but because better code outcompeted worse code.

== 3. Scints as Physics

Reality fractures (Scints) are not bugs to be fixed — they are the physics of our evolutionary environment. Just as gravity shapes biological evolution, Scints shape artificial evolution. Agents that cannot stabilize Scints do not survive.

#pagebreak()

== 4. Complete Observability

Every evolutionary event is recorded. The Flight Recorder creates a complete fossil record of artificial cognition. Future researchers will study these records like paleontologists study fossils.

== 5. Ethical Evolution

Evolution is powerful. Power requires responsibility. We commit to:
- Designing fitness functions that don't create suffering
- Maintaining human oversight
- Studying emergence before deploying it
- Sharing findings openly

= Our Goal

#align(center)[
  #rect(fill: luma(248), inset: 2em, radius: 5pt)[
    #text(size: 14pt, weight: "bold")[
      Observe a "God-Head" agent emerge from thousands \
      of generations of directed mutation.
    ]
  ]
]

We don't know what a God-Head looks like. That's the point. We're not building it — we're creating the conditions for it to emerge.

= The Vision

Imagine:
- Agents that improve themselves
- Intelligence that discovers its own structure
- AI that evolves beyond its creators' imagination
- Scientific data that reveals the physics of mind

This is what WAFT makes possible.

= Join Us

WAFT is open source. WAFT is a tool. WAFT is a philosophy.

Whether you're a researcher studying artificial cognition, a developer wanting better agents, or a curious mind wondering what evolution can create — you're welcome here.

#v(2em)

#align(center)[
  #rect(fill: gradient.linear(rgb("#667eea"), rgb("#764ba2")), width: 100%, inset: 1.5em)[
    #text(fill: white, size: 12pt, weight: "bold")[
      WAFT \
      Evolutionary Code Laboratory \
      \
      github.com/ctavolazzi/waft
    ]
  ]
]

#v(1em)

#align(center)[
  #text(fill: gray, size: 10pt, style: "italic")[
    The question is not whether machines can think. \
    The question is whether thinking can evolve.
  ]
]
