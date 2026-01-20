// TELEPORT MASSIVE D&D CAMPAIGN ONE-PAGER
// Quick Start Guide for Game Masters

#import "@preview/showybox:2.0.4": showybox

#set document(title: "D&D Campaign One-Pager", author: "Teleport Massive Games Division")
#set page(paper: "us-letter", margin: 0.75in)
#set text(font: "New Computer Modern", size: 9pt)

#let tm-blue = rgb("#1a365d")
#let danger = rgb("#c53030")
#let magic = rgb("#805ad5")

#align(center)[
  #rect(fill: gradient.linear(tm-blue, magic), width: 100%, inset: 1.5em)[
    #text(fill: white, size: 20pt, weight: "bold")[TELEPORT MASSIVE]
    #v(0.2em)
    #text(fill: white.darken(10%), size: 12pt)[D&D 5e Campaign Setting | One-Pager]
  ]
]

#v(0.5em)

#grid(
  columns: 2,
  gutter: 1em,
  [
    = The Premise
    
    Players are employees of *Teleport Massive*, a corporation on the cutting edge of quantum teleportation technology. When experiments go wrong, reality itself fractures—and it's up to the team to stabilize the Scints before everything unravels.
    
    = Setting: Site-Delta-9
    
    A sprawling underground research facility where the laws of physics are more like guidelines.
    
    #showybox(frame: (border-color: tm-blue, body-color: tm-blue.lighten(95%)))[
      *Key Locations:*
      - Quantum Chamber 7 (where it happened)
      - The Cafeteria (suspiciously normal)
      - Executive Floor (restricted)
      - The Void Room (don't ask)
    ]
    
    = Starting Adventure
    
    *"The Quantum Incident"*
    
    During a routine teleportation test, researcher Sarah Chen vanishes—and reappears in three places at once. The Scint alarms are screaming. Reality is fracturing. The players have 1 hour before the fracture becomes permanent.
    
    *Objectives:*
    1. Find all three Sarah Chens
    2. Determine which one is "real"
    3. Stabilize the Scint
    4. Survive whatever's coming through
    
    = Key NPCs
    
    #table(
      columns: (auto, 1fr),
      stroke: 0.5pt,
      inset: 6pt,
      [*Dr. Elena Voss*], [CEO. Knows more than she says.],
      [*Dr. Marcus Chen*], [CTO. Obsessed with the science.],
      [*Sarah Chen*], [Test subject. Traumatized. Multiple.],
      [*Aziah Calderon*], [Head of R&D. Pragmatic.],
    )
  ],
  [
    = Character Options
    
    #showybox(frame: (border-color: magic, body-color: magic.lighten(92%)))[
      *Backgrounds:*
      - Quantum Researcher (INT)
      - Security Officer (STR)
      - Corporate Spy (DEX)
      - Ethics Board Member (WIS)
      - IT Specialist (INT)
      - Cafeteria Worker (CHA)
    ]
    
    = Scint Mechanics
    
    When players encounter a Scint, roll a d20:
    
    #table(
      columns: (auto, 1fr),
      stroke: 0.5pt,
      inset: 5pt,
      [*1-5*], [SYNTAX_TEAR: Environment glitches],
      [*6-10*], [LOGIC_FRACTURE: Paradox spawns],
      [*11-15*], [HALLUCINATION: False memories],
      [*16-19*], [Minor stabilization],
      [*20*], [Perfect collapse—bonus loot],
    )
    
    *SAFETY_VOID* (nat 1): Something comes through. Roll initiative.
    
    = Unique Items
    
    - *Quantum Badge* (+1 Persuasion with TM employees)
    - *Scint Detector* (Alerts within 30 ft)
    - *Stabilization Syringe* (One-use Scint fix)
    - *Chen's Journal* (Plot device)
    
    = The Big Secret
    
    #showybox(frame: (border-color: danger, body-color: danger.lighten(92%)))[
      *GM EYES ONLY*
      
      The Quantum Incident wasn't an accident. Someone—or something—is using Teleport Massive's technology to punch holes in reality. The Scints are getting worse. And whatever's on the other side is trying to get in.
    ]
    
    = Campaign Hooks
    
    1. The CEO is receiving messages from "future self"
    2. Employees are reporting memory loss
    3. The cafeteria food is too good (why?)
    4. Someone's been living in the Void Room
    5. The LHC connection (September 10, 2008)
  ],
)

#v(0.5em)

#align(center)[
  #rect(fill: tm-blue, inset: 0.8em)[
    #text(fill: white, size: 10pt)[
      *TELEPORT MASSIVE* | "Making Distance Irrelevant" | Site-Delta-9 Campaign Setting
    ]
  ]
]
