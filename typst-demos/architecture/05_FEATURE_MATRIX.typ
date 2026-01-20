// WAFT FEATURE MATRIX
// Complete Capability Reference

#import "@preview/showybox:2.0.4": showybox

#set document(title: "WAFT Feature Matrix", author: "WAFT Team")
#set page(paper: "us-letter", margin: 0.5in)
#set text(font: "New Computer Modern", size: 9pt)

#let primary = rgb("#553c9a")
#let yes = text(fill: green.darken(20%), weight: "bold")[✓]
#let no = text(fill: gray)[—]
#let partial = text(fill: orange)[◐]

#align(center)[
  #rect(fill: gradient.linear(primary, primary.darken(20%)), width: 100%, inset: 1.5em)[
    #text(fill: white, size: 22pt, weight: "bold")[FEATURE MATRIX]
    #v(0.2em)
    #text(fill: white.darken(10%), size: 11pt)[Complete Capability Reference]
  ]
]

#v(0.5em)

= Core Features

#table(
  columns: (2fr, auto, 1fr),
  stroke: 0.5pt,
  inset: 6pt,
  fill: (x, y) => if y == 0 { luma(230) } else { white },
  [*Feature*], [*Status*], [*Module*],
  [Being System (timeful agents)], [#yes], [`being.py`],
  [Being Lifecycle Management], [#yes], [`core/`],
  [Skills & Memories], [#yes], [`being.py`],
  [Personality & Goals], [#yes], [`being.py`],
  [Corporation Simulation], [#yes], [`core/corporations/`],
  [Financial Tracking], [#yes], [`corporations/financial_state.py`],
  [Department Management], [#yes], [`corporations/corporation.py`],
  [Employee Roster], [#yes], [`corporations/corporation.py`],
  [Reality/Realm System], [#yes], [`reality.py`, `core/bureaucracy_realm.py`],
  [Multi-Realm Support], [#yes], [`_realms/`],
  [Cross-Realm Transfer], [#partial], [Experimental],
)

= Evolution System

#table(
  columns: (2fr, auto, 1fr),
  stroke: 0.5pt,
  inset: 6pt,
  fill: (x, y) => if y == 0 { luma(230) } else { white },
  [*Feature*], [*Status*], [*Module*],
  [Genome Management], [#yes], [`evolution/styling_genome.py`],
  [Mutation Engine], [#yes], [`evolution/`],
  [Selection Algorithms], [#yes], [`evolution/`],
  [Tournament Selection], [#yes], [`evolution/`],
  [Elitism], [#yes], [`evolution/`],
  [Scint Detection], [#yes], [`evolution/scint_detector.py`],
  [SYNTAX_TEAR Detection], [#yes], [`evolution/scint_detector.py`],
  [LOGIC_FRACTURE Detection], [#yes], [`evolution/scint_detector.py`],
  [SAFETY_VOID Detection], [#yes], [`evolution/scint_detector.py`],
  [HALLUCINATION Detection], [#yes], [`evolution/scint_detector.py`],
  [Fitness Scoring], [#yes], [`evolution/`],
  [Flight Recorder], [#yes], [`core/tracing/`],
  [Emergence Detection], [#partial], [Research],
)

#pagebreak()

= Document Generation

#table(
  columns: (2fr, auto, 1fr),
  stroke: 0.5pt,
  inset: 6pt,
  fill: (x, y) => if y == 0 { luma(230) } else { white },
  [*Feature*], [*Status*], [*Module*],
  [Typst Templates], [#yes], [`templates/typst/`],
  [HTML Templates], [#yes], [`templates/`],
  [LaTeX Templates], [#yes], [`templates/latex/`],
  [PDF Generation], [#yes], [`pdf.py`],
  [Chronicler (auto-docs)], [#yes], [`core/chronicler/`],
  [Brief Generator], [#yes], [`brief.py`],
  [Report Generator], [#yes], [`core/chronicler/reports.py`],
  [TM Report Template], [#yes], [`templates/tm_report.py`],
  [Personal Memo Template], [#yes], [`templates/personal_memo.py`],
  [Invoice Template], [#yes], [`templates/invoice_contract.py`],
  [Academic Paper Template], [#yes], [`templates/academic_paper.py`],
  [D&D Character Sheet], [#yes], [`templates/`],
  [Storybook Template], [#yes], [`templates/storybook.py`],
  [Field Guide Template], [#yes], [`templates/field_guide.py`],
)

= Empirica Integration

#table(
  columns: (2fr, auto, 1fr),
  stroke: 0.5pt,
  inset: 6pt,
  fill: (x, y) => if y == 0 { luma(230) } else { white },
  [*Feature*], [*Status*], [*Module*],
  [Session Management], [#yes], [`core/empirica.py`],
  [Preflight Assessment], [#yes], [`core/empirica.py`],
  [Postflight Assessment], [#yes], [`core/empirica.py`],
  [Check Gates], [#yes], [`core/empirica.py`],
  [13 Epistemic Vectors], [#yes], [`core/empirica.py`],
  [Finding Logging], [#yes], [`core/empirica.py`],
  [Unknown Logging], [#yes], [`core/empirica.py`],
  [Dashboard], [#yes], [`core/empirica_dashboard.py`],
  [Gamification (XP/Karma)], [#yes], [`core/gamification.py`],
  [Character Sheet], [#yes], [`core/gamification.py`],
)

= RPG & Gaming

#table(
  columns: (2fr, auto, 1fr),
  stroke: 0.5pt,
  inset: 6pt,
  fill: (x, y) => if y == 0 { luma(230) } else { white },
  [*Feature*], [*Status*], [*Module*],
  [D&D 5e Character System], [#yes], [`core/dnd5e/character.py`],
  [Dice Rolling], [#yes], [`core/dnd5e/dice.py`],
  [Combat System], [#yes], [`core/dnd5e/combat.py`],
  [Stat Generation], [#yes], [`core/dnd5e/stats.py`],
  [Scenario Generation], [#yes], [`core/dnd_scenario/`],
  [Quest System], [#yes], [`core/dnd_scenario/`],
  [Encounter Generator], [#yes], [`core/dnd_scenario/encounter_generator.py`],
  [Lore Builder], [#yes], [`core/dnd_scenario/lore_builder.py`],
  [Party Management], [#yes], [`core/dnd_scenario/party_manager.py`],
)

#pagebreak()

= API & Integration

#table(
  columns: (2fr, auto, 1fr),
  stroke: 0.5pt,
  inset: 6pt,
  fill: (x, y) => if y == 0 { luma(230) } else { white },
  [*Feature*], [*Status*], [*Module*],
  [REST API], [#yes], [`api/`],
  [FastAPI Framework], [#yes], [`api/`],
  [Authentication], [#yes], [`api/routes/auth.py`],
  [Being API], [#yes], [`api/routes/being.py`],
  [Project API], [#yes], [`api/routes/projects.py`],
  [Quest API], [#yes], [`api/routes/quests.py`],
  [Oracle API], [#yes], [`api/routes/oracle.py`],
  [WebSocket Support], [#partial], [`api/`],
  [LLM Integration], [#yes], [`core/`],
  [OpenAI Support], [#yes], [`core/`],
  [Local Model Support], [#yes], [`core/`],
  [RAG Integration], [#yes], [`rag/`],
)

= Pantheon (Entity Gods)

#table(
  columns: (2fr, auto, 1fr),
  stroke: 0.5pt,
  inset: 6pt,
  fill: (x, y) => if y == 0 { luma(230) } else { white },
  [*Feature*], [*Status*], [*Module*],
  [Bureaucracy God], [#yes], [`pantheon/bureaucracy_god.py`],
  [GitHub God], [#yes], [`pantheon/github_god.py`],
  [Paperwork God], [#yes], [`pantheon/paperwork_god.py`],
  [Storyteller], [#yes], [`pantheon/storyteller.py`],
  [Judge], [#yes], [`pantheon/judge.py`],
  [Librarian], [#yes], [`pantheon/library/librarian.py`],
  [Mission Control], [#yes], [`pantheon/mission_control.py`],
  [Reasoner], [#yes], [`pantheon/reasoner.py`],
  [Financial Documents], [#yes], [`pantheon/financial_documents.py`],
  [The Village (AI Town)], [#yes], [`pantheon/the_village.py`],
)

= Advanced Features

#table(
  columns: (2fr, auto, 1fr),
  stroke: 0.5pt,
  inset: 6pt,
  fill: (x, y) => if y == 0 { luma(230) } else { white },
  [*Feature*], [*Status*], [*Module*],
  [Self-Engineering], [#yes], [`core/self_engineering/`],
  [Problem Detection], [#yes], [`core/self_engineering/problem_detector.py`],
  [Self Modification], [#yes], [`core/self_engineering/self_modification.py`],
  [AI Town Simulation], [#yes], [`ai_town/`],
  [Multi-Agent Coordination], [#yes], [`ai_town/`],
  [Karma System], [#yes], [`karma.py`, `karma_system.py`],
  [Prime Directive], [#yes], [`prime_directive/`],
  [Tracing/Observability], [#yes], [`core/tracing/`],
  [Worldbuilding], [#yes], [`worldbuild.py`],
)

#v(0.5em)

#align(center)[
  #showybox(frame: (border-color: primary))[
    *Legend:* #yes Implemented | #partial Partial/Experimental | #no Not Available
  ]
]

#v(0.5em)

#align(center)[
  #rect(fill: primary, inset: 1em)[
    #text(fill: white, size: 10pt)[
      FEATURE MATRIX | 100+ Features, Infinite Possibilities
    ]
  ]
]
