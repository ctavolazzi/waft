#import "@preview/s6t5-page-bordering:1.0.0": s6t5-page-bordering

// Custom header/footer setup
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true, first-line-indent: 0.5cm)
#set heading(numbering: "1.")

= WAFT Menu of Options and Examples

#v(0.5cm)

#align(center)[
  #text(size: 16pt, weight: "bold")[Wave Agent Framework & Tools]
  #linebreak()
  #text(size: 12pt, style: "italic")[A Python framework for directed evolution of self-modifying AI agents]
  #linebreak()
  #text(size: 10pt)["Don't just build agents. Breed them."]
]

#v(1cm)

== Core Commands

=== Project Management

#block(
  fill: rgb("#f5f5f5"),
  stroke: 1pt,
  radius: 4pt,
  inset: 12pt,
  width: 100%,
)[
  #text(weight: "bold")[`waft new <name>`]
  #v(6pt)
  #text[Creates a new evolutionary laboratory with uv project structure, `_pyrite` memory, and Empirica tracking.]
  
  #v(8pt)
  #text(weight: "bold")[`waft verify`]
  #v(6pt)
  #text[Verifies project structure and configuration.]
  
  #v(8pt)
  #text(weight: "bold")[`waft evolve --agent <name>`]
  #v(6pt)
  #text[Run evolutionary cycle: Spawn variants → Evaluate in Gym → Select fittest.]
]

=== Documentation Generation

#block(
  fill: rgb("#f5f5f5"),
  stroke: 1pt,
  radius: 4pt,
  inset: 12pt,
  width: 100%,
)[
  #text(weight: "bold")[`waft-docs field-guide`]
  #v(6pt)
  #text[Generate field guide PDFs (layman, professional, scientist levels).]
  
  #v(8pt)
  #text(weight: "bold")[`waft-docs booklet`]
  #v(6pt)
  #text[Assemble complete booklet with all field guides.]
  
  #v(8pt)
  #text(weight: "bold")[`waft-docs session-summary`]
  #v(6pt)
  #text[Generate comprehensive session summary PDF.]
  
  #v(8pt)
  #text(weight: "bold")[`waft-docs all`]
  #v(6pt)
  #text[Generate everything: field guides, booklets, printer-friendly versions.]
]

=== Evolution & Gym

#block(
  fill: rgb("#f5f5f5"),
  stroke: 1pt,
  radius: 4pt,
  inset: 12pt,
  width: 100%,
)[
  #text(weight: "bold")[`waft spawn --agent <name> --mutation <file>`]
  #v(6pt)
  #text[Create agent variant with genetic mutations.]
  
  #v(8pt)
  #text(weight: "bold")[`waft eval --agent <name>`]
  #v(6pt)
  #text[Evaluate agent fitness in Scint Gym (Reality Fracture Detection).]
  
  #v(8pt)
  #text(weight: "bold")[`waft evolve --agent <name> --generations <n>`]
  #v(6pt)
  #text[Run full evolutionary cycle for multiple generations.]
]

=== Pantheon (Higher Beings)

#block(
  fill: rgb("#f5f5f5"),
  stroke: 1pt,
  radius: 4pt,
  inset: 12pt,
  width: 100%,
)[
  #text(weight: "bold")[Magistrate]
  #v(6pt)
  #text[God of Precedent and Body of Proof. Organizes proof cases into precedents.]
  
  #v(8pt)
  #text(weight: "bold")[Judge]
  #v(6pt)
  #text[God of Judgment and Evaluation. Evaluates claims against Body of Proof.]
  
  #v(8pt)
  #text(weight: "bold")[The Reasoner]
  #v(6pt)
  #text[God of Reasoning Traces. Maintains traceable reasoning chains.]
  
  #v(8pt)
  #text(weight: "bold")[GitHub God]
  #v(6pt)
  #text[God of Repository Management. Generates rollups and tracks operations.]
  
  #v(8pt)
  #text(weight: "bold")[Paperwork God]
  #v(6pt)
  #text[God of Paperwork and Documentation. Manages forms and bureaucratic processes.]
  
  #v(8pt)
  #text(weight: "bold")[Typist God]
  #v(6pt)
  #text[God of Typst Document Generation. Tracks compilations, templates, and usage statistics.]
]

== Key Features

=== The Three Pillars

#block(
  fill: rgb("#e3f2fd"),
  stroke: 2pt,
  radius: 4pt,
  inset: 16pt,
  width: 100%,
)[
  #text(size: 13pt, weight: "bold")[1. The Substrate (Code as DNA)]
  #v(8pt)
  #text[
    Agents write their own Python source code. Every agent has a unique genome ID (SHA-256 hash).
    Mutations are code changes. Evolution is hot-swapping better genomes.
  ]
  
  #v(12pt)
  #text(size: 13pt, weight: "bold")[2. The Physics (Scint System)]
  #v(8pt)
  #text[
    Reality Fracture Detection acts as natural selection. Agents face quests testing ability to handle:
    SYNTAX_TEAR, LOGIC_FRACTURE, SAFETY_VOID, HALLUCINATION. Fitness measured by stability, efficiency, safety.
  ]
  
  #v(12pt)
  #text(size: 13pt, weight: "bold")[3. The Flight Recorder]
  #v(8pt)
  #text[
    Rigorous telemetry for phylogenetic trees. Every evolutionary action recorded with complete context:
    Genome ID, Parent ID, Generation, Event Type, Payload, Fitness Metrics.
  ]
]

== Template System

=== Typst Templates

#block(
  fill: rgb("#fff3e0"),
  stroke: 1pt,
  radius: 4pt,
  inset: 12pt,
  width: 100%,
)[
  #text(weight: "bold")[Available Templates:]
  #v(8pt)
  #text[• Appreciated Letter - Business/personal letters]
  #text[• Brilliant CV - Professional CV/resume]
  #text[• Worldbuild ISO - ISO 7010 safety symbols]
  #text[• Worldbuild Quill - Quantum circuit diagrams]
  #text[• Worldbuild Yagenda - Event schedules and agendas]
  #text[• Flow Way - Academic papers]
  #text[• Arkheion - Research papers]
  #text[• Wonderous Book - Book formatting]
  #text[• And many more...]
  
  #v(8pt)
  #text(weight: "bold")[Usage:]
  #v(6pt)
  #text[All templates auto-discovered via TypstTemplateRegistry. Use wrapper functions or direct TypstCompiler.]
]

=== LaTeX Templates

#block(
  fill: rgb("#fff3e0"),
  stroke: 1pt,
  radius: 4pt,
  inset: 12pt,
  width: 100%,
)[
  #text[Comprehensive LaTeX template library including academic papers, CVs, letters, and more.]
  #text[Integrated with WAFT's document generation system.]
]

== Examples & Showcases

=== Interactive Demos

#block(
  fill: rgb("#f1f8e9"),
  stroke: 1pt,
  radius: 4pt,
  inset: 12pt,
  width: 100%,
)[
  #text(weight: "bold")[`examples/interactive_demo.py`]
  #v(6pt)
  #text[Experience WAFT documenting itself in real-time with ASCII art and animations.]
  
  #v(8pt)
  #text(weight: "bold")[`examples/advanced_demo/advanced_demo.py`]
  #v(6pt)
  #text[Advanced demo showcasing self-documentation, PDF organization, and meta-cognitive integration.]
  
  #v(8pt)
  #text(weight: "bold")[`examples/generate_waft_intro_one_pager.py`]
  #v(6pt)
  #text[Generate one-pager introduction to WAFT using evolution tools.]
]

=== Document Generation

#block(
  fill: rgb("#f1f8e9"),
  stroke: 1pt,
  radius: 4pt,
  inset: 12pt,
  width: 100%,
)[
  #text(weight: "bold")[`scripts/generate_waft_docs.py`]
  #v(6pt)
  #text[Unified CLI for generating field guides, booklets, and session summaries.]
  
  #v(8pt)
  #text(weight: "bold")[`examples/generate_session_recap_pdf_waft.py`]
  #v(6pt)
  #text[Generate session recap PDFs using ChatDistiller, StylingGenome, and TwoPageGenerator.]
  
  #v(8pt)
  #text(weight: "bold")[`examples/generate_feature_showcase.py`]
  #v(6pt)
  #text[Comprehensive feature showcase demonstrating all WAFT capabilities.]
]

== Integration Points

=== Empirica (Epistemic Tracking)

#text[WAFT integrates with Empirica for epistemic self-assessment and learning tracking.]

=== Karma System

#text[Complete karma economy with KarmaMarket, KarmaCollector, and Afterlife Market (Treasure Tavern).]

=== Being System

#text[Timeful agents that learn skills, evolve, and pass memories upward through ancestral chains.]

=== Reality System

#text[Spin up simulation environments where beings can learn and evolve.]

== Quick Reference

#grid(
  columns: 2,
  gutter: 1cm,
  [
    #block(
      fill: rgb("#fafafa"),
      stroke: 1pt,
      radius: 4pt,
      inset: 10pt,
    )[
      #text(weight: "bold")[Installation]
      #v(6pt)
      #text[`uv tool install waft`]
    ]
  ],
  [
    #block(
      fill: rgb("#fafafa"),
      stroke: 1pt,
      radius: 4pt,
      inset: 10pt,
    )[
      #text(weight: "bold")[New Project]
      #v(6pt)
      #text[`waft new my_lab`]
    ]
  ],
  [
    #block(
      fill: rgb("#fafafa"),
      stroke: 1pt,
      radius: 4pt,
      inset: 10pt,
    )[
      #text(weight: "bold")[Verify Setup]
      #v(6pt)
      #text[`waft verify`]
    ]
  ],
  [
    #block(
      fill: rgb("#fafafa"),
      stroke: 1pt,
      radius: 4pt,
      inset: 10pt,
    )[
      #text(weight: "bold")[Help]
      #v(6pt)
      #text[`waft help`]
    ]
  ],
)

#pagebreak()

== Additional Resources

=== Documentation

#text[• README.md - Main project documentation]
#text[• AGENTS.md - AI agent instructions]
#text[• WAFT_CONTEXT_DUMP.md - Comprehensive system overview]
#text[• docs/ - Detailed documentation directory]

=== Work Efforts

#text[• `_work_efforts/` - Johnny Decimal organized work tracking]
#text[• Uses work-efforts MCP server for management]

=== Pantheon

#text[• `_pantheon/` - Higher Beings (Gods) system]
#text[• Timeless Forces that Bind Reality Together]

=== Realms

#text[• `_realms/` - Simulation environments]
#text[• Bureaucracy Realm, PDFme Realm, and more]

#v(2cm)

#align(center)[
  #text(size: 10pt, style: "italic")[
    Generated: #datetime.today().display()
    #linebreak()
    WAFT - Wave Agent Framework & Tools
    #linebreak()
    "Don't just build agents. Breed them."
  ]
]
