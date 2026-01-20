// THE CHRONICLER SYSTEM
// Automated Documentation Generation

#import "@preview/showybox:2.0.4": showybox

#set document(title: "Chronicler System", author: "WAFT Documentation Division")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#let primary = rgb("#744210")

#align(center)[
  #rect(fill: gradient.linear(primary, primary.darken(30%)), width: 100%, inset: 2em)[
    #text(fill: white, size: 24pt, weight: "bold")[THE CHRONICLER]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 12pt)[WAFT | Automated Documentation Generation]
  ]
]

#v(1em)

= What is the Chronicler?

The *Chronicler* is WAFT's automated documentation system. It generates reports, briefs, and records from simulation data.

#showybox(
  frame: (border-color: primary, body-color: primary.lighten(95%)),
  title: "Key Capability",
)[
  The Chronicler transforms raw WAFT data into professional documents — PDFs, reports, memos, and more.
]

= Document Types

#grid(
  columns: 2,
  gutter: 1em,
  showybox(frame: (border-color: blue, body-color: blue.lighten(95%)), title: "Reports")[
    - Status reports
    - Financial reports
    - Research summaries
    - Incident reports
  ],
  showybox(frame: (border-color: green, body-color: green.lighten(95%)), title: "Briefs")[
    - Executive briefs
    - Personnel briefs
    - Mission briefs
    - Technical briefs
  ],
  showybox(frame: (border-color: orange, body-color: orange.lighten(95%)), title: "Records")[
    - Employee records
    - Transaction logs
    - Event histories
    - Meeting minutes
  ],
  showybox(frame: (border-color: purple, body-color: purple.lighten(95%)), title: "Creative")[
    - Memos (in-character)
    - Letters
    - Announcements
    - Fictional documents
  ],
)

= Using the Chronicler

```python
from waft.chronicler import Chronicler

chronicler = Chronicler(project_path=Path("."))

# Generate a corporation report
report = chronicler.generate_report(
    report_type="status",
    corporation_id="teleport_massive_20250701",
    period="Q1 2026",
)

# Save as PDF
report.save_pdf("reports/tm_q1_2026.pdf")
```

#pagebreak()

= Report Templates

== Status Report

```python
report = chronicler.generate_report(
    report_type="status",
    corporation_id=corp_id,
    include_sections=[
        "executive_summary",
        "financial_overview",
        "personnel_changes",
        "research_progress",
        "next_quarter_goals",
    ],
)
```

== Personnel Brief

```python
brief = chronicler.generate_brief(
    brief_type="personnel",
    being_id=being.being_id,
    include_sections=[
        "background",
        "skills_assessment",
        "performance_history",
        "recommendations",
    ],
)
```

= Customization

== Custom Templates

```python
chronicler.register_template(
    name="incident_report",
    template_path="templates/incident.typ",
    required_fields=["incident_id", "date", "description"],
)
```

== Styling

```python
chronicler.set_style(
    header="TELEPORT MASSIVE",
    footer="Classification: Internal",
    color_scheme="corporate_blue",
    font="New Computer Modern",
)
```

= CLI Commands

```bash
# Generate status report
waft chronicle report --corp teleport_massive --type status

# Generate Being brief
waft chronicle brief --being abc-123 --type personnel

# List available templates
waft chronicle templates

# Custom document
waft chronicle custom --template incident_report --data incident.json
```

= Output Formats

- PDF (via Typst)
- HTML
- Markdown
- JSON (raw data)

#v(1em)

#align(center)[
  #rect(fill: primary, inset: 1em)[
    #text(fill: white)[THE CHRONICLER | Stories Write Themselves]
  ]
]
