// Drafting Demo - Margin Notes and Annotations
// https://typst.app/universe/package/drafting

#import "@preview/drafting:0.2.2": *

#set page(margin: (left: 2.5cm, right: 4cm, top: 2cm, bottom: 2cm))
#set-page-properties(margin-right: 4cm)

#set text(font: "New Computer Modern", size: 11pt)

= Drafting Package Demo

This document demonstrates the `drafting` package for Typst, which provides helpful functions for content positioning and margin comments/notes.

== Basic Margin Notes

#lorem(20)
#margin-note(side: left)[Hello from the left margin!]
#lorem(10)
#margin-note[This note appears in the right margin by default]
#margin-note[Notes automatically avoid collision when they would overlap]
#margin-note(stroke: aqua + 3pt)[Custom stroke styling is easy to apply]

#lorem(25)

== Highlighted Phrases with Notes

#margin-note(stroke: green, side: left)[You can highlight text and add a note at the same time.][This phrase is highlighted and connected to the margin note.]

#lorem(15)

== Inline Notes

#lorem(10)
#inline-note[The default inline note will split the paragraph at its location]
#lorem(10)

#inline-note(par-break: false, stroke: (paint: orange, dash: "dashed"))[
  You can specify `par-break: false` to keep the note inline without breaking the paragraph
]

#lorem(10)

== Custom Styled Notes

#let caution-rect = rect.with(inset: 1em, radius: 0.5em, fill: yellow.lighten(80%))
#inline-note(rect: caution-rect)[
  *Caution:* This is a custom-styled inline note with a yellow background and rounded corners.
]

#lorem(15)

== Multiple Reviewers

#let reviewer-a = margin-note.with(stroke: blue)
#let reviewer-b = margin-note.with(stroke: purple)
#let reviewer-c = margin-note.with(stroke: orange)

#lorem(10)
#reviewer-a[Comment from Reviewer A - This section needs more detail]
#lorem(8)
#reviewer-b(side: left)[Reviewer B says: Consider restructuring this paragraph]
#lorem(8)
#reviewer-c[Reviewer C: Excellent point made here!]

#lorem(20)

== Summary

The `drafting` package provides:
- *margin-note*: Add notes to page margins
- *inline-note*: Add inline annotations
- *set-margin-note-defaults*: Customize default styling
- *set-page-properties*: Configure page bounds for proper layout
- Automatic collision avoidance for overlapping notes
- Support for multiple reviewer styles

#v(1cm)

#align(center)[
  #rect(fill: blue.lighten(90%), inset: 1em, radius: 0.5em)[
    *Package:* drafting v0.2.2 \
    *Source:* https://typst.app/universe/package/drafting
  ]
]
