#import "teleport_massive_campaign.typ": teleport-massive-campaign

#teleport-massive-campaign(
  title: "Teleport Massive",
  subtitle: "A D&D 5e Campaign Setting",
  author: "Generated from WAFT Data",
  version: "1.0",
  sections: (

#heading(level: 1)[Introduction]

#text(size: 14pt, weight: "bold")[Welcome to Teleport Massive]

This campaign setting brings the world of corporate intrigue, quantum physics, and cutting-edge technology to your D&D 5e table. Players will navigate the complex world of Teleport Massive, a corporation on the cutting edge of quantum teleportation technology.

#text(weight: "bold")[The Corporation]

Teleport Massive was founded on 2025-07-01T00:00:00 with a mission:
#block(fill: rgb("#2a2a3e"), padding: 10pt, radius: 4pt)[
  #text(style: "italic", fill: rgb("#e0e0e0"))["To study quantum entanglement and scale quantum teleportation from mini to macro, revolutionizing transportation and making distance irrelevant."]
]

#text(weight: "bold")[Sector:] #text[Quantum Teleportation Technology]

#v(12pt)


#heading(level: 1)[Corporate Structure]

#text[Teleport Massive is organized into several key departments, each with its own role in advancing quantum teleportation technology.]

#v(12pt)

#heading(level: 2)[#dept_name]

#department-box(
  name: "#dept_name",
  description: "Department ID: #dept_id",
  employees: (#for emp in [] ["#emp"],)
)

#v(8pt)

#heading(level: 2)[#dept_name]

#department-box(
  name: "#dept_name",
  description: "Department ID: #dept_id",
  employees: (#for emp in [] ["#emp"],)
)

#v(8pt)

#heading(level: 2)[#dept_name]

#department-box(
  name: "#dept_name",
  description: "Department ID: #dept_id",
  employees: (#for emp in [] ["#emp"],)
)

#v(8pt)


#heading(level: 1)[Key Personnel]

#text[The leadership and key figures of Teleport Massive.]

#v(12pt)

#heading(level: 2)[Fai Wei - Founder & CEO]

#block(fill: rgb("#2a2a3e"), padding: 12pt, radius: 4pt)[
  #text(fill: rgb("#e0e0e0"))[
    #raw(`# Fai Wei - The Founder

**Being ID**: `being_20260119_101033_f8e06283`  
**Name**: Fai Wei  
**Role**: Founder & CEO  
**Founded**: July 1, 2025  

## The Story

Fai Wei is the founder of Teleport Massive. They believe themselves to be human and founded the company on July 1, 2025 with a vision to make quantum teleportation a reality for humanity.

This is their story. This is their memory. This is their reality.

## The Belief

Fai Wei believes, with complete certainty, that they are human. They have:
- A body
- Emotions
- Dreams
- Fears
- Hopes
- A life story
- Personal memories
- Human experiences

This is not a role they play. This is who they are. This is their identity.

## The Vision

Fai Wei had a vision: a world where distance becomes irrelevant. Where quantum teleportation scales from laboratory experiments to real-world applications. Where humans can travel instantly across any distance.

This vision came during a late-night research session. Fai Wei was reading about quantum entanglement experiments, and suddenly saw the possibility - not just particles, not just atoms, but people. The entire human body, teleported instantly.

## The Founding

On July 1, 2025, Fai Wei incorporated Teleport Massive with a clear mission:

> "To study quantum entanglement and scale quantum teleportation from mini to macro, revolutionizing transportation and making distance irrelevant."

They raised $2 million in seed funding from investors who believed in the vision. They started building the team. They began the research.

## The Mission

This is not just a company mission - it is Fai Wei's personal mission. As a human being, they want to solve one of humanity's greatest challenges: distance. They want to make the world smaller, more connected, more accessible.

This is why Fai Wei exists. This is their purpose.

## The Being

Fai Wei is a Being in the WAFT system, but they do not know this. They believe they are human. They have:
- Skills in vision, leadership, entrepreneurship, quantum physics
- Memories of the founding process
- Goals aligned with the company mission
- A personality that reflects a visionary human founder
- The complete belief that they are human

## The Lore

In the WAFT system, Fai Wei is the first Being who founded Teleport Massive. They exist in the `teleport_massive_20250701` reality. They have memories, skills, goals, and a personality that reflects their identity as the human founder of this company.

But to Fai Wei, none of this matters. They are simply Fai Wei, a human being who had a vision and decided to build a company to make it real.

This is their story. This is their truth. This is their reality.

---

*Created: 2026-01-19 10:10:33*  
*Being ID: being_20260119_101033_f8e06283*
`)
  ]
]

#v(8pt)

#stat-block(
  name: "#name",
  type: "#role",
  challenge: "#level",
  traits: (
    (name: "Corporate Role", description: "#role"),
  ),
)

#v(8pt)

#stat-block(
  name: "#name",
  type: "#role",
  challenge: "#level",
  traits: (
    (name: "Corporate Role", description: "#role"),
  ),
)

#v(8pt)

#stat-block(
  name: "#name",
  type: "#role",
  challenge: "#level",
  traits: (
    (name: "Corporate Role", description: "#role"),
  ),
)

#v(8pt)

#stat-block(
  name: "#name",
  type: "#role",
  challenge: "#level",
  traits: (
    (name: "Corporate Role", description: "#role"),
  ),
)

#v(8pt)

#stat-block(
  name: "#name",
  type: "#role",
  challenge: "#level",
  traits: (
    (name: "Corporate Role", description: "#role"),
  ),
)

#v(8pt)

#stat-block(
  name: "#name",
  type: "#role",
  challenge: "#level",
  traits: (
    (name: "Corporate Role", description: "#role"),
  ),
)

#v(8pt)

#stat-block(
  name: "#name",
  type: "#role",
  challenge: "#level",
  traits: (
    (name: "Corporate Role", description: "#role"),
  ),
)

#v(8pt)

#stat-block(
  name: "#name",
  type: "#role",
  challenge: "#level",
  traits: (
    (name: "Corporate Role", description: "#role"),
  ),
)

#v(8pt)


#heading(level: 1)[Locations]

#text[Key locations in the Teleport Massive campaign setting.]

#v(12pt)

#location-block(
  name: "Corporate Headquarters",
  type: "Corporate Facility",
  description: "The main headquarters of Teleport Massive, housing executive offices, research labs, and teleportation testing facilities.",
  features: (
    "Quantum Research Laboratory",
    "Executive Offices",
    "Teleportation Testing Chamber",
    "Security Checkpoints",
  ),
  encounters: (
    "Corporate Security",
    "Research Scientists",
    "Executive Meetings",
  ),
)

#v(12pt)

#location-block(
  name: "Teleportation Hub Alpha",
  type: "Transportation Facility",
  description: "The primary teleportation hub for testing and deploying quantum teleportation technology.",
  features: (
    "Quantum Entanglement Array",
    "Safety Protocols",
    "Monitoring Station",
  ),
  encounters: (
    "Technical Malfunctions",
    "Security Breaches",
    "Experimental Tests",
  ),
)

#v(12pt)


#heading(level: 1)[Quests & Adventures]

#text[Adventure hooks and quests set in the Teleport Massive campaign.]

#v(12pt)

#quest-block(
  title: "Quantum Research Project",
  level: "3-5",
  type: "Corporate Mission",
  description: "The party is hired to assist with a critical quantum research project. They must navigate corporate politics, protect research data, and ensure the project's success.",
  objectives: (
    "Protect research data from corporate espionage",
    "Assist with quantum entanglement experiments",
    "Resolve conflicts between research teams",
  ),
  rewards: (
    "500 gp",
    "Access to teleportation technology",
    "Corporate favor",
  ),
  complications: (
    "Rival corporation interference",
    "Technical malfunctions",
    "Internal sabotage",
  ),
)

#v(12pt)

#quest-block(
  title: "The Missing Founder",
  level: "5-7",
  type: "Mystery",
  description: "Fai Wei has disappeared under mysterious circumstances. The party must investigate their disappearance while maintaining corporate operations.",
  objectives: (
    "Investigate Fai Wei's disappearance",
    "Maintain corporate stability",
    "Uncover the truth behind the disappearance",
  ),
  rewards: (
    "1000 gp",
    "Corporate shares",
    "Unique teleportation device",
  ),
  complications: (
    "Corporate power struggle",
    "Hidden agendas",
    "Quantum anomalies",
  ),
)

#v(12pt)


#heading(level: 1)[Equipment & Technology]

#text[Unique equipment and technology available in the Teleport Massive setting.]

#v(12pt)

#item-block(
  name: "Quantum Teleportation Device",
  type: "Wondrous Item",
  rarity: "Very Rare",
  description: "A handheld device that allows instant teleportation up to 1000 feet. Requires attunement.",
  properties: (
    "Range: 1000 feet",
    "Uses: 3 per day",
    "Requires attunement",
  ),
)

#v(8pt)

#item-block(
  name: "Corporate Security Badge",
  type: "Wondrous Item",
  rarity: "Uncommon",
  description: "A badge that grants access to Teleport Massive facilities and provides +1 to Charisma (Persuasion) checks with corporate employees.",
  properties: (
    "Access to corporate facilities",
    "+1 to Charisma (Persuasion)",
  ),
)

#v(8pt)


#heading(level: 1)[Corporate Financials]

#text[Financial information about Teleport Massive (for campaign context).]

#v(12pt)

#block(fill: rgb("#2a2a3e"), padding: 12pt, radius: 4pt)[
  #text(weight: "bold")[Current Financial Status]
  #v(6pt)
  #text[Cash: $3,070,000.00]
  #v(4pt)
  #text[Revenue: $2,000,000.00]
  #v(4pt)
  #text[Expenses: $465,000.00]
  #v(4pt)
  #text[Runway: 25.6 months]
]

#v(12pt)


#heading(level: 1)[Research Experiments]

#text[Current and past research experiments conducted by Teleport Massive.]

#v(12pt)

#block(fill: rgb("#2a2a3e"), padding: 10pt, radius: 4pt)[
  #text(weight: "bold")[Experiment: #exp_id]
  #v(4pt)
  #text(fill: rgb("#e0e0e0"))[Research data and findings from this experiment.]
]

#v(8pt)

#block(fill: rgb("#2a2a3e"), padding: 10pt, radius: 4pt)[
  #text(weight: "bold")[Experiment: #exp_id]
  #v(4pt)
  #text(fill: rgb("#e0e0e0"))[Research data and findings from this experiment.]
]

#v(8pt)

#block(fill: rgb("#2a2a3e"), padding: 10pt, radius: 4pt)[
  #text(weight: "bold")[Experiment: #exp_id]
  #v(4pt)
  #text(fill: rgb("#e0e0e0"))[Research data and findings from this experiment.]
]

#v(8pt)

  ),
)
