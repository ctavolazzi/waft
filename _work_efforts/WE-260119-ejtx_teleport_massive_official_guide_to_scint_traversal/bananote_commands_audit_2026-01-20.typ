#import "@preview/bananote:0.1.1": *

#show: note.with(
  title: [Commands Audit + Bananote Notes],
  authors: (
    ([ctavolazzi], [WAFT]),
  ),
  date: datetime(year: 2026, month: 1, day: 20),
  version: "0.1"
)

#abstract[
This notebook tracks the command audit, /bananote setup, and Typst PDF outputs.
]

= Goals
- Create /bananote command for Typst notes
- Maintain notes while auditing commands
- Produce Typst PDF with command inventory and recommendations

= Work Log
== 21:14 PST
- Logged plan in devlog for WE-260119-ejtx / TKT-ejtx-008
- Created /bananote command doc in .cursor/commands
- Prepared command inventory extraction

== 21:18 PST
- Compiled bananote notes to PDF (font warnings for New Computer Modern Sans)
- Generated commands inventory JSON (129 commands)
- Created commands audit Typst source + Flow Way PDF

== 21:28 PST
- Ran /bananote update: logged this request and recompiled notes PDF

= Findings
- Empirica project-info command not available; used project-list + project-bootstrap with explicit ID
- 129 command docs detected in .cursor/commands
- Several command docs missing standard sections (Purpose, Execution Steps, Output Format)

= Decisions
- Use Flow Way template for the commands audit PDF
- Use bananote for live notes and archive source + PDF in work effort

= Next Steps
- Generate commands audit Typst source + PDF
- Update ticket with file links
- Run Empirica postflight
