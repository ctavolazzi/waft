// THE CAFETERIA MYSTERY
// An Unofficial Investigation

#import "@preview/showybox:2.0.4": showybox

#set document(title: "The Cafeteria Mystery", author: "Anonymous Researcher")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#let primary = rgb("#744210")
#let warning = rgb("#d69e2e")

#align(center)[
  #rect(fill: primary, width: 100%, inset: 2em)[
    #text(fill: white, size: 22pt, weight: "bold")[THE CAFETERIA MYSTERY]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 12pt)[An Unofficial Investigation]
    #v(0.2em)
    #text(fill: white.darken(20%), size: 10pt)[DOCUMENT NOT FOR DISTRIBUTION]
  ]
]

#v(1em)

#showybox(
  frame: (border-color: warning, body-color: warning.lighten(92%)),
)[
  *DISCLAIMER:* This document was found in the personal effects of [name withheld]. It does not represent official Teleport Massive positions. The author's current whereabouts are unknown.
]

= The Observations

I've been at Site-Delta-9 for six months now. Like everyone else, I noticed the cafeteria food is... remarkable. Too remarkable.

- The soup is always perfect
- The bread is always fresh
- Every meal is exactly what you wanted
- No one ever gets sick

*This is not normal.*

= The Investigation

I started keeping notes:

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  [*Date*], [*Observation*],
  [Day 15], [Noticed the menu changes before I realize what I want],
  [Day 23], [Asked for ingredients. Chef smiled but didn't answer.],
  [Day 31], [Followed supply truck. It came from [REDACTED].],
  [Day 45], [Tried to enter kitchen. Door wouldn't open.],
  [Day 52], [Found no delivery records for food supplies.],
)

#pagebreak()

= The Questions

1. *Where does the food come from?*
   - No visible deliveries
   - No supplier contracts on file
   - Storage areas are always "off-limits"

2. *Why is it so good?*
   - Professional chefs? (checked credentials — none exist)
   - Special ingredients? (can't identify some flavors)
   - Something else?

3. *Why won't anyone talk about it?*
   - Asked HR: "The cafeteria is well-managed."
   - Asked Security: "That's not a security concern."
   - Asked Dr. Chen: He changed the subject immediately.

= Theories

#grid(
  columns: 1,
  gutter: 1em,
  showybox(frame: (border-color: gray), title: "Theory 1: Quantum Food Generation")[
    The food is created using teleportation technology. It's not delivered — it's *materialized*. This would explain the lack of supply chain and the impossible freshness.
  ],
  showybox(frame: (border-color: gray), title: "Theory 2: Scint Stabilization")[
    The food is a by-product of Scint research. When reality fractures are stabilized, something is created. That something is edible.
  ],
  showybox(frame: (border-color: gray), title: "Theory 3: [REDACTED]")[
    I've heard whispers about the Void Room. About something that lives there. Something that needs to be... fed? Or something that *provides*?
  ],
)

= The Warning

I'm leaving this document where someone will find it. I've been asking too many questions. Yesterday, the cafeteria served my favorite meal from childhood — a meal I've never told anyone about.

*They know what I'm doing.*

If you're reading this:
- Don't ask about the food
- Don't investigate the kitchen
- Don't refuse to eat

*Just eat. Be grateful. And don't look too closely at what's in the soup.*

#v(1em)

#align(center)[
  #text(style: "italic", fill: gray)[
    [Document ends here. Several pages appear to have been removed.]
  ]
]
