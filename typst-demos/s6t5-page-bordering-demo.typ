// s6t5-page-bordering Demo - Professional Page Borders
// https://typst.app/universe/package/s6t5-page-bordering

#import "@preview/s6t5-page-bordering:1.0.0": s6t5-page-bordering

// Define custom header
#let header = {
  set align(bottom)
  show table.cell.where(y: 0): set align(left)
  set text(weight: "bold", size: 9pt)
  table(
    stroke: (y: none),
    columns: (0.8fr, 1.4fr, 0.8fr),
    rows: 1fr,
    table.hline(),
    [Document ID], [Title], [Page],
    [WAFT-DEMO-001],
    [s6t5-page-bordering Demo Document],
    [
      #context counter(page).display(
        "1 / 1",
        both: true,
      )
    ],
  )
}

// Define custom footer
#let footer = {
  set text(weight: "bold", size: 9pt)
  table(
    stroke: (y: none),
    columns: (0.8fr, 1.4fr, 0.8fr),
    rows: 1fr,
    [Classification: Internal],
    [WAFT Documentation System],
    [
      Version 1.0.0
    ],
    table.hline(),
  )
}

// Apply the page bordering template
#show: s6t5-page-bordering.with(
  margin: (left: 40pt, right: 40pt, top: 70pt, bottom: 70pt),
  expand: 15pt,
  space-top: 15pt,
  space-bottom: 15pt,
  stroke-header: none,
  stroke-footer: none,
  header: header,
  footer: footer,
)

#set text(font: "New Computer Modern", size: 11pt)

= s6t5-page-bordering Demo

== Overview

This document demonstrates the `s6t5-page-bordering` package for Typst. This package provides a professional way to add borders around page margins, including support for custom headers and footers.

== Key Features

The package offers:

- *Page Border*: A clean border around the entire page content area
- *Header Support*: Custom header content within the bordered area
- *Footer Support*: Custom footer content within the bordered area
- *Configurable Margins*: Full control over page margins
- *Expandable Borders*: Adjust border expansion beyond content

== Configuration Parameters

#table(
  columns: (auto, 1fr),
  align: (left, left),
  stroke: 0.5pt,
  inset: 8pt,
  [*Parameter*], [*Description*],
  [`margin`], [Dictionary with left, right, top, bottom values],
  [`expand`], [Border expansion beyond margin],
  [`space-top`], [Space between header and content],
  [`space-bottom`], [Space between content and footer],
  [`stroke-header`], [Stroke style for header border],
  [`stroke-footer`], [Stroke style for footer border],
  [`header`], [Custom header content],
  [`footer`], [Custom footer content],
)

== Use Cases

This package is particularly useful for:

1. *Business Documents*: Official reports and specifications
2. *Technical Documentation*: Product manuals and guides
3. *Academic Papers*: Thesis documents and research papers
4. *Legal Documents*: Contracts and agreements

== Example Code

```typst
#import "@preview/s6t5-page-bordering:1.0.0": s6t5-page-bordering
#show: s6t5-page-bordering.with(
  margin: (left: 30pt, right: 30pt, top: 60pt, bottom: 60pt),
  expand: 15pt,
  header: your-header-content,
  footer: your-footer-content,
)
```

#pagebreak()

= Page 2 - Additional Content

This is the second page to demonstrate that the page bordering continues consistently across multiple pages.

== Document History

#table(
  columns: (auto, auto, auto, 1fr),
  align: (center, center, center, left),
  stroke: 0.5pt,
  inset: 8pt,
  [*Version*], [*Date*], [*Author*], [*Changes*],
  [1.0.0], [2026-01-19], [WAFT Team], [Initial demo document],
)

== Summary

The `s6t5-page-bordering` package provides:
- Professional bordered pages
- Consistent header/footer placement
- Easy configuration
- Business-ready document styling

#v(1fr)

#align(center)[
  #rect(fill: green.lighten(90%), inset: 1em, radius: 0.5em)[
    *Package:* s6t5-page-bordering v1.0.0 \
    *Source:* https://typst.app/universe/package/s6t5-page-bordering
  ]
]
