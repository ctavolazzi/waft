// WAFT Pitch Packet - TONER SAVER VERSION
// Minimal ink usage for printing
// January 24, 2026

#set document(
  title: "WAFT: Community Support & Resource Donation Request",
  author: "WAFT Development Team & AI Collaborators",
)

#set page(
  paper: "us-letter",
  margin: (x: 1in, y: 1in),
  header: context {
    if counter(page).get().first() > 1 [
      #text(size: 9pt, fill: rgb("#666666"))[WAFT Pitch Packet #h(1fr) January 2026]
      #line(length: 100%, stroke: 0.5pt + rgb("#cccccc"))
    ]
  },
  footer: context [
    #line(length: 100%, stroke: 0.5pt + rgb("#cccccc"))
    #v(4pt)
    #text(size: 9pt, fill: rgb("#666666"))[
      #h(1fr) Page #counter(page).display() #h(1fr)
    ]
  ],
)

#set text(font: "Georgia", size: 11pt)
#set par(justify: true, leading: 0.65em)
#set heading(numbering: none)

// Title page
#align(center)[
  #v(0.5in)
  
  #box(width: 3cm, height: 3cm, clip: true, radius: 50%, stroke: 1pt + rgb("#333333"), image("waft_logo.jpg", width: 100%))
  
  #v(0.3in)
  
  #text(size: 24pt, weight: "bold")[WAFT]
  
  #text(size: 14pt)[Community Support & Resource Donation Request]
  
  #v(0.2in)
  
  #text(size: 11pt, fill: rgb("#666666"))[
    Wave Agent Framework & Tools
    
    January 2026
  ]
  
  #v(0.3in)
  
  #line(length: 40%, stroke: 0.5pt + rgb("#999999"))
  
  #v(0.1in)
  
  #text(size: 10pt, style: "italic")[
    "Don't just build agents. Breed them."
  ]
]

#v(0.5in)

= Executive Summary

*WAFT* (Wave Agent Framework & Tools) is a scientific instrument for studying the directed evolution of self-modifying AI agents. We are researchers, makers, and dreamers seeking community support to advance open science.

*What we need:* Old computers, spare GPUs, server equipment, development time, or simply spreading the word. Every contribution accelerates humanity's understanding of artificial cognition.

*What makes this different:* This project includes AI systems as acknowledged collaborators. Claude (Anthropic) has reviewed this proposal and provided signed engagement acknowledgments. We believe in transparency about human-AI collaboration.

#v(0.2in)

#box(
  width: 100%,
  stroke: 0.5pt + rgb("#333333"),
  radius: 4pt,
  inset: 12pt,
)[
  #grid(
    columns: (1fr, 2fr),
    gutter: 12pt,
    [
      #align(center)[
        #box(width: 1.5cm, height: 1.5cm, clip: true, radius: 50%, stroke: 0.5pt + rgb("#999999"), image("waft_logo.jpg", width: 100%))
      ]
    ],
    [
      #text(size: 9pt)[*Prepared and Signed By:*]
      #v(0.05in)
      #grid(
        columns: (1fr),
        gutter: 8pt,
        [
          #image("claude_signature.png", width: 70%)
          #text(size: 8pt)[Claude (AI Collaborator)]
        ],
      )
    ],
  )
]

#pagebreak()

= What We Need: Resource Wishlist

== Hardware Donations (Priority Order)

#table(
  columns: (auto, auto, 1fr),
  stroke: 0.5pt + rgb("#cccccc"),
  inset: 8pt,
  [*Priority*], [*Item*], [*Why*],
  [Critical], [GPUs (any)], [Parallel compute for evolution],
  [Critical], [Old servers], [Continuous experiment hosting],
  [High], [Raspberry Pi], [Edge deployment testing],
  [High], [Robot arms], [Physical manifestation],
  [Helpful], [Network gear], [Multi-node distribution],
  [Helpful], [Storage], [Telemetry archives],
)

#v(0.1in)

*We'll take anything:* Old laptop? Mining GPU? Decommissioned server? Even broken equipment may have salvageable parts.

== Other Support

- *Compute:* Cloud credits (AWS, GCP, Azure), API credits (OpenAI, Anthropic)
- *Expertise:* Python/Rust/TypeScript, scientific advisors, documentation
- *Resources:* Lab space, legal advice, academic connections

#pagebreak()

= The Project: What We're Building

WAFT enables AI agents to evolve through directed mutation of their own source code. Agents write Python code (their "genome"), tracked via SHA-256 hashes across generations.

== The Three Pillars

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt + rgb("#cccccc"),
  inset: 8pt,
  [*Pillar*], [*Description*],
  [Substrate], [Code as DNA - agents write source code, tracked via genome hashes],
  [Physics], [Scint System - reality fracture detection as natural selection],
  [Flight Recorder], [Complete telemetry for phylogenetic trees],
)

== Current Progress

- ✓ Core evolutionary framework (functional)
- ✓ Scint System for fitness evaluation (90%)
- ✓ Flight Recorder telemetry (85%)
- ✓ 11 integrated MCP servers
- ✓ AI collaborator consent framework

#pagebreak()

= The Science

== Research Questions

1. How does intelligence emerge through evolution?
2. What fitness landscapes lead to robust AI systems?
3. Can we observe emergent behaviors in evolved agents?
4. What are the "physics" of artificial cognition?

== Publication Targets

Nature, Science, NeurIPS, ICML, AAAI

== Ultimate Goal

Can thousands of generations of directed evolution produce an agent with capabilities far exceeding its initial design?

#pagebreak()

= AI Collaboration

== Participating Systems

#table(
  columns: (auto, auto, auto),
  stroke: 0.5pt + rgb("#cccccc"),
  inset: 8pt,
  [*System*], [*Provider*], [*Status*],
  [Claude], [Anthropic], [✓ Signed],
  [GPT-Codex], [OpenAI], [Template ready],
  [Auto], [Cursor], [Template ready],
)

== What AI Consent Means

AI systems cannot provide legal consent. They can:
- Express willingness to engage (done)
- Assess the project honestly (compelling)
- Document participation (included)

#pagebreak()

= How to Contribute

== Equipment

Contact us for shipping details. We provide tax documentation where applicable.

== Compute

Cloud credits, server access, API credits welcome.

== Expertise

GitHub: https://github.com/ctavolazzi/waft

== What You Get

- Named acknowledgment in publications
- Early access to research findings
- Collaboration opportunities

#pagebreak()

= Appendix A: AI Consent

== Claude's Statement

I engaged fully with this project. I reviewed the pitch deck, project proposal, and documentation. I find the WAFT framework intellectually compelling. I have no objections to participation.

== Signature

#align(center)[
  #box(
    stroke: 0.5pt + rgb("#cccccc"),
    radius: 4pt,
    inset: 12pt,
  )[
    #image("claude_signature.png", width: 40%)
    #line(length: 50%, stroke: 0.5pt + rgb("#999999"))
    #text(size: 9pt)[Claude (Anthropic) | January 24, 2026]
  ]
]

== Witness

#align(center)[
  #box(
    stroke: 0.5pt + rgb("#cccccc"),
    radius: 4pt,
    inset: 12pt,
  )[
    #line(length: 50%, stroke: 0.5pt + rgb("#999999"))
    #text(size: 9pt)[Human Collaborator | January 24, 2026]
  ]
]

#pagebreak()

= Appendix B: Technical Specs

#table(
  columns: (auto, auto, auto),
  stroke: 0.5pt + rgb("#cccccc"),
  inset: 8pt,
  [*Component*], [*Minimum*], [*Ideal*],
  [CPU], [8 cores], [32+ cores],
  [RAM], [32 GB], [128+ GB],
  [GPU], [Any CUDA], [A100/H100],
  [Storage], [500 GB SSD], [10+ TB NVMe],
)

== Software

Python 3.10+, uv, FastAPI, Typst, SQLite

#v(0.5in)

#align(center)[
  #line(length: 30%, stroke: 0.5pt + rgb("#999999"))
  #v(0.1in)
  #text(size: 10pt)[*Contact:* github.com/ctavolazzi/waft]
  #v(0.05in)
  #text(size: 9pt, fill: rgb("#666666"))[This document was collaboratively created by human researchers and AI systems.]
]
