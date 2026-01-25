// WAFT Pitch Packet - REVISED (Funder-Ready)
// Addresses critique: contact info, credentials, accountability, specifics
// January 24, 2026

#set document(
  title: "WAFT: Community Support & Resource Donation Request",
  author: "Christopher Tavolazzi & AI Collaborators",
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
  #v(0.3in)
  
  #box(width: 2.5cm, height: 2.5cm, clip: true, radius: 50%, stroke: 1pt + rgb("#333333"), image("waft_logo.jpg", width: 100%))
  
  #v(0.2in)
  
  #text(size: 24pt, weight: "bold")[WAFT]
  
  #text(size: 14pt)[Community Support & Resource Donation Request]
  
  #v(0.15in)
  
  #text(size: 11pt, fill: rgb("#666666"))[
    Wave Agent Framework & Tools
    
    January 2026
  ]
]

#v(0.3in)

= Quick Facts (For Busy Funders)

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt + rgb("#cccccc"),
  inset: 8pt,
  [*What*], [Open-source framework for studying AI evolution through code mutation],
  [*Who*], [Christopher Tavolazzi (indie researcher) + AI collaborators],
  [*Status*], [Working prototype, 70-75% complete, actively developed],
  [*Ask*], [Hardware donations, compute credits, expertise],
  [*Legal*], [Individual project (not 501c3). Donations are gifts, not tax-deductible.],
  [*Verify*], [github.com/ctavolazzi/waft (MIT License, public repo)],
)

#v(0.15in)

#box(
  width: 100%,
  stroke: 0.5pt + rgb("#333333"),
  radius: 4pt,
  inset: 10pt,
)[
  #grid(
    columns: (1fr, 2fr),
    gutter: 10pt,
    [
      #align(center)[
        #box(width: 1.2cm, height: 1.2cm, clip: true, radius: 50%, stroke: 0.5pt + rgb("#999999"), image("waft_logo.jpg", width: 100%))
      ]
    ],
    [
      #text(size: 9pt)[*Signed:*]
      #grid(
        columns: (1fr),
        gutter: 6pt,
        [
          #image("claude_signature.png", width: 60%)
          #text(size: 7pt)[Claude (AI Collaborator)]
        ],
      )
    ],
  )
]

#pagebreak()

= About the Researcher

== Christopher Tavolazzi

*Background:* Independent software developer and AI researcher. Building WAFT as an open-source research project to study how AI agents can evolve through code mutation.

*Verifiable Work:*
- GitHub: github.com/ctavolazzi (public profile, commit history)
- WAFT repository: 2,800+ files, active development since 2025
- Documentation: 100+ pages of technical docs, design documents
- This project: Self-funded, no prior grants

*Why Trust This:*
- All code is open source (MIT License) - you can read every line
- All development is public on GitHub - you can see the commit history
- I'm transparent about limitations - this is indie research, not a lab

*Contact:*
- GitHub: \@ctavolazzi
- Email: (available via GitHub profile)
- Location: United States

#pagebreak()

= What We're Building (Plain English)

*The Core Idea:* What if AI agents could modify their own source code and we tracked those changes like genetic mutations?

*How It Works:*
1. An agent's Python code is its "DNA" (hashed with SHA-256)
2. Agents can mutate their code (like genetic mutation)
3. A fitness system tests if mutations help or hurt
4. We track lineages like biologists track species evolution

*What Exists Today:*
- ✓ Core framework that runs agents and tracks mutations
- ✓ "Scint System" that detects errors in agent outputs (fitness function)
- ✓ Telemetry system recording all evolutionary events
- ✓ 11 integrated tool servers (MCP protocol)
- ✓ Comprehensive documentation

*What We're Researching:*
- How does capability emerge through many small code changes?
- What patterns appear in successful vs. failed mutation paths?
- Can we map "fitness landscapes" for AI agent capabilities?

*Realistic Goals:*
- Short-term: Run 1,000+ generation experiments, publish methodology
- Medium-term: Conference papers (AAAI, NeurIPS workshops)
- Long-term: If results are interesting, pursue larger publication venues

#pagebreak()

= What We Need (Specific)

== Minimum Viable Setup

To run meaningful experiments, we need:

#table(
  columns: (auto, auto, 1fr),
  stroke: 0.5pt + rgb("#cccccc"),
  inset: 8pt,
  [*Item*], [*Minimum*], [*Purpose*],
  [GPU], [1x RTX 3080 or equivalent], [Run LLM inference for agent mutations],
  [Server], [32GB RAM, 8 cores], [Host continuous evolution experiments],
  [Storage], [1TB SSD], [Store telemetry data and agent lineages],
)

*Current status:* Running on personal laptop. Limited to small experiments.

== What We'll Accept

- *Any GPU:* Even old GTX 1080s help. Multiple weak GPUs > one strong one for parallel experiments.
- *Old servers:* Decommissioned hardware with working components.
- *Cloud credits:* AWS, GCP, Azure, Lambda Labs.
- *API credits:* OpenAI, Anthropic (for LLM-based agents).

== What You Get in Return

- Named acknowledgment in any resulting publications
- Access to experiment results before public release
- Input on research directions if desired
- Transparent reporting on how your donation was used

#pagebreak()

= Accountability & Transparency

== How We'll Report Back

If you donate equipment:
1. We'll confirm receipt within 48 hours
2. We'll send quarterly updates on experiments run
3. We'll acknowledge your contribution in publications
4. You can request status updates anytime

== What We Won't Do

- Sell donated equipment
- Use donations for non-research purposes
- Make promises we can't keep

== Verify Everything

- *Code:* github.com/ctavolazzi/waft (read it yourself)
- *Commits:* Full history shows actual work, not vaporware
- *Documentation:* Comprehensive, not hand-wavy

== Legal Structure (Honest)

This is an individual research project, not a registered non-profit. Donations are personal gifts, not tax-deductible charitable contributions. If you need tax deductibility, this isn't the right project for you.

#pagebreak()

= Timeline & Milestones

== Phase 1: Infrastructure (Current - Q2 2026)

- ✓ Core framework complete
- ✓ Scint system implemented
- ○ Scale to multi-GPU experiments
- ○ Run first 1,000-generation experiment

== Phase 2: Research (Q2-Q4 2026)

- Run systematic experiments on mutation strategies
- Document and analyze results
- Draft methodology paper
- Submit to workshop/conference

== Phase 3: Publication (2027)

- Peer review and revision
- Open-source all experiment data
- Release reproducibility package

*What Success Looks Like:*
- Minimum: Publishable methodology paper, open dataset
- Goal: Insights into AI evolution patterns
- Stretch: Results interesting enough for top venues

#pagebreak()

= Addressing Skepticism

== "This sounds like a cult"

Fair concern. "God-Head agent" was marketing language, not science. The actual research question: "Can directed evolution of code produce measurably improved AI agents?" That's testable and falsifiable.

== "Why should I trust an indie researcher?"

You shouldn't trust blindly. That's why:
- All code is open source
- All development is public
- I'm honest about being self-funded and small-scale

== "AI consent is a gimmick"

Partially fair. It's a philosophical gesture, not legal consent. But it documents our methodology: we asked the AI systems we work with about their participation and recorded their responses. Whether that matters is up to you.

== "You'll never publish in Nature"

Probably true. Initial targets are workshops and conferences (NeurIPS workshops, AAAI). If results warrant it, we'll aim higher. We're not promising Nature; we're promising honest research.

#pagebreak()

= Appendix A: AI Collaboration Statement

== What This Means

We use AI systems (Claude, GPT) as development tools. We asked them about their participation and documented their responses. This is transparency, not legal consent.

== Claude's Recorded Response

"I engaged fully with this project. I reviewed the documentation and find the WAFT framework intellectually compelling. I have no objections to participation. However, I am a language model without continuous existence - each session is independent."

#align(center)[
  #box(stroke: 0.5pt + rgb("#cccccc"), radius: 4pt, inset: 10pt)[
    #image("claude_signature.png", width: 35%)
    #line(length: 40%, stroke: 0.5pt + rgb("#999999"))
    #text(size: 8pt)[Claude (Anthropic) | January 24, 2026]
  ]
]

== Witness

#align(center)[
  #box(stroke: 0.5pt + rgb("#cccccc"), radius: 4pt, inset: 10pt)[
    #line(length: 40%, stroke: 0.5pt + rgb("#999999"))
    #text(size: 8pt)[Human Collaborator | January 24, 2026]
  ]
]

#pagebreak()

= Appendix B: Technical Specifications

== Hardware Requirements

#table(
  columns: (auto, auto, auto),
  stroke: 0.5pt + rgb("#cccccc"),
  inset: 8pt,
  [*Component*], [*Minimum*], [*Ideal*],
  [CPU], [8 cores], [32+ cores],
  [RAM], [32 GB], [128+ GB],
  [GPU], [RTX 3080 (10GB)], [A100/H100],
  [Storage], [1 TB SSD], [10+ TB NVMe],
)

== Software Stack

- Python 3.10+, uv package manager
- FastAPI for APIs, SQLite for telemetry
- Typst for documentation generation
- MIT License (open source)

== Verify the Code

```
git clone https://github.com/ctavolazzi/waft
cd waft
# Read the code yourself
```

#v(0.3in)

#align(center)[
  #line(length: 30%, stroke: 0.5pt + rgb("#999999"))
  #v(0.1in)
  #text(size: 10pt)[*Contact:* github.com/ctavolazzi]
  #v(0.05in)
  #text(size: 9pt, fill: rgb("#666666"))[Open source research. Verify everything.]
]
