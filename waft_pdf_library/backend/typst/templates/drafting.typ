#import "@preview/drafting:0.2.2": margin-note, inline-note, set-margin-note-defaults, note-outline

#set page(margin: (left: 2cm, right: 2cm, top: 2.5cm, bottom: 2.5cm))
#set text(font: "Libertinus Serif", size: 11pt)

= WAFT Drafting Demo

This document showcases margin notes, inline notes, and layout guidance for in-progress drafts. It is designed to be a live editorial layer you can toggle on/off before final export.

#margin-note(side: left)[Scope: Show core drafting features in one page.]
#margin-note[Style: Keep the voice clear and minimal.]

== Draft Objectives

- Provide fast in-margin review cues
- Mark inline corrections without breaking flow
- Highlight risky assumptions as they appear

#lorem(30)

#inline-note[Inline notes can flag specific claims or add alternative phrasing.]

#lorem(25)

#set-margin-note-defaults(stroke: orange + 2pt, side: right)
#margin-note[Reviewer A: tighten this paragraph, reduce redundancy.]
#margin-note(side: left)[Reviewer B: add a source link here.]

== Risk Register

#lorem(18)
#inline-note(par-break: false, stroke: (paint: red, dash: "dashed"))[
  WARNING: This section needs a citation before release.
]
#lorem(18)

== Editorial Timeline

#table(
  columns: (auto, auto, 1fr),
  [Version], [Date], [Notes],
  [0.1], [2026-01-19], [Initial drafting prototype],
  [0.2], [2026-01-20], [Margin notes refined],
)

#note-outline()
