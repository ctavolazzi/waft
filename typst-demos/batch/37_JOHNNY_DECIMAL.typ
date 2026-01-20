// JOHNNY DECIMAL SYSTEM
// Organizing WAFT Projects

#import "@preview/showybox:2.0.4": showybox

#set document(title: "Johnny Decimal System", author: "WAFT Organization")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#let primary = rgb("#2b6cb0")

#align(center)[
  #rect(fill: gradient.linear(primary, primary.darken(30%)), width: 100%, inset: 2em)[
    #text(fill: white, size: 24pt, weight: "bold")[JOHNNY DECIMAL]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 12pt)[WAFT | Project Organization System]
  ]
]

#v(1em)

= What is Johnny Decimal?

*Johnny Decimal* is a system for organizing files and folders using a two-level numeric scheme: Areas (10-99) and Categories (X.00-X.99).

#showybox(
  frame: (border-color: primary, body-color: primary.lighten(95%)),
  title: "The Pattern",
)[
  ```
  XX-XX_area_name/
      XX_category_name/
          XX.XX_document_name.md
  ```
]

= WAFT Organization

== Work Efforts

```
_work_efforts/
├── 00-09_meta/
│   ├── 00_index/
│   │   └── 00.00_index.md
│   └── 01_templates/
│       └── 01.01_work_effort_template.md
├── 10-19_development/
│   ├── 10_features/
│   │   ├── 10.00_index.md
│   │   └── 10.01_scint_detection.md
│   └── 11_bugfixes/
├── 20-29_documentation/
└── 30-39_research/
```

== Document IDs

Every document has a unique ID:

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  [*ID*], [*Meaning*],
  [`10.01`], [Area 10, Category 10, Document 01],
  [`25.03`], [Area 20-29, Category 25, Document 03],
  [`00.00`], [Index file (special)],
)

#pagebreak()

= Benefits

#grid(
  columns: 2,
  gutter: 1em,
  showybox(frame: (border-color: blue, body-color: blue.lighten(95%)), title: "Findability")[
    Know immediately where things are:
    - "That's a 20-something — documentation"
    - "10.x — development work"
  ],
  showybox(frame: (border-color: green, body-color: green.lighten(95%)), title: "Scalability")[
    - 10 areas (00-09 to 90-99)
    - 10 categories per area
    - 100 items per category
    - = 10,000 possible items
  ],
  showybox(frame: (border-color: orange, body-color: orange.lighten(95%)), title: "Consistency")[
    Everyone uses the same system:
    - No "my stuff" folders
    - No duplicate hierarchies
    - Clear ownership
  ],
  showybox(frame: (border-color: purple, body-color: purple.lighten(95%)), title: "Navigation")[
    Index files link everything:
    - Area indexes
    - Category indexes
    - Cross-references
  ],
)

= Using Johnny Decimal in WAFT

== Create Work Effort

```bash
waft work-effort create "Implement Scint detection" \
    --area 10 \
    --category 10
# Creates: 10_features/10.01_implement_scint_detection.md
```

== List by Area

```bash
waft work-effort list --area 10-19
```

== Search

```bash
waft work-effort search "scint"
```

= Index Files

Every category has an index (`XX.00_index.md`):

```markdown
# 10_features Index

## Documents
- [[10.01_scint_detection]] - Scint detection feature
- [[10.02_stabilization_loop]] - Stabilization implementation

## Related
- [[../11_bugfixes/11.00_index|Bugfixes]]
- [[../../20-29_documentation/20_guides/20.00_index|Guides]]
```

= Best Practices

1. *Always use the system* — Don't create ad-hoc folders
2. *Update indexes* — Keep them current
3. *Use descriptive names* — Numbers + words
4. *Cross-reference* — Link related documents
5. *Archive, don't delete* — Move to 90-99 archive area

#v(1em)

#align(center)[
  #rect(fill: primary, inset: 1em)[
    #text(fill: white)[JOHNNY DECIMAL | A Place for Everything]
  ]
]
