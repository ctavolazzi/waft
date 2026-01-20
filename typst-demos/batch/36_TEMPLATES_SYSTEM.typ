// WAFT TEMPLATES SYSTEM
// Document Generation Templates

#import "@preview/showybox:2.0.4": showybox

#set document(title: "Templates System", author: "WAFT Documentation")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#let primary = rgb("#c05621")

#align(center)[
  #rect(fill: gradient.linear(primary, primary.darken(30%)), width: 100%, inset: 2em)[
    #text(fill: white, size: 24pt, weight: "bold")[TEMPLATES SYSTEM]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 12pt)[WAFT | Document Generation Templates]
  ]
]

#v(1em)

= Overview

WAFT includes multiple template engines for generating professional documents from simulation data.

= Available Templates

#table(
  columns: (auto, 1fr, auto),
  stroke: 0.5pt,
  inset: 8pt,
  [*Template*], [*Description*], [*Format*],
  [`tm_report`], [Teleport Massive branded reports], [HTML/PDF],
  [`brief`], [Executive and technical briefs], [PDF],
  [`personal_memo`], [In-character staff memos], [HTML],
  [`invoice`], [Financial invoices], [PDF],
  [`incident_report`], [Safety incident reports], [PDF],
  [`tech_spec`], [Technical specifications], [PDF],
  [`case_brief`], [Legal/case documentation], [Typst],
)

= Template: TM Report

```python
from waft.templates import tm_report

html = tm_report.generate(
    title="Q1 2026 Research Summary",
    sections=[
        {"heading": "Overview", "content": "..."},
        {"heading": "Findings", "content": "..."},
    ],
    header="TELEPORT MASSIVE",
    classification="INTERNAL",
)
```

= Template: Brief

```python
from waft.templates import brief

pdf = brief.generate(
    title="Project Lazarus Status",
    cover_header="TELEPORT MASSIVE",
    cover_subtitle="Quantum Research Division",
    summary="Current status of Project Lazarus...",
    sections=[...],
    footer="Site-Delta-9",
)
```

#pagebreak()

= Template: Personal Memo

In-character memos from Teleport Massive staff:

```python
from waft.templates import personal_memo

html = personal_memo.generate(
    from_name="Dr. Marcus Chen",
    to_name="Research Team",
    subject="New Safety Protocols",
    date="January 15, 2026",
    body="""
    Team,
    
    Following the incident, we're implementing new protocols...
    """,
    mood="concerned",  # Affects styling
)
```

= Creating Custom Templates

== Typst Templates

```typst
// templates/my_template.typ
#let my_template(title, content) = {
  set document(title: title)
  set page(paper: "us-letter")
  
  align(center)[
    #text(size: 24pt, weight: "bold")[#title]
  ]
  
  content
}
```

== Register Template

```python
from waft.templates import register_template

register_template(
    name="my_template",
    path="templates/my_template.typ",
    engine="typst",
)
```

= Template Variables

All templates have access to:

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  [*Variable*], [*Description*],
  [`{{title}}`], [Document title],
  [`{{date}}`], [Generation date],
  [`{{author}}`], [Author name],
  [`{{corporation}}`], [Corporation data],
  [`{{being}}`], [Being data (if applicable)],
  [`{{custom.*}}`], [Custom fields],
)

= CLI Usage

```bash
# Generate from template
waft template generate tm_report --data report.json

# List templates
waft template list

# Preview template
waft template preview brief --sample
```

#v(1em)

#align(center)[
  #rect(fill: primary, inset: 1em)[
    #text(fill: white)[TEMPLATES | Professional Documents, Automated]
  ]
]
