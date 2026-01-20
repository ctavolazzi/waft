// Scaffolder Demo - Layout Debugging Borders
// https://typst.app/universe/package/scaffolder

#import "@preview/scaffolder:0.2.1": scaffolding

#set text(font: "New Computer Modern", size: 11pt)
#set page(paper: "us-letter", margin: (x: 1in, y: 1in))

// Apply scaffolding to show layout borders
#set page(background: scaffolding(stroke: red + 0.5pt))

= Scaffolder Package Demo

== Overview

The `scaffolder` package shows borders around the main text area, header, and footer in Typst documents. This is invaluable for understanding and debugging layout issues.

Similar to the LaTeX `showframe` package, it provides visual guides for your document structure.

== Use Cases

1. *Debugging Margins*: See exactly where your content boundaries are
2. *Layout Design*: Understand how headers/footers relate to main content
3. *Teaching*: Demonstrate page structure to students
4. *Quality Assurance*: Verify consistent margins across pages

== Basic Usage

```typst
#import "@preview/scaffolder:0.2.1": scaffolding

#set page(background: scaffolding())
```

That's it! The scaffolding function adds visual borders to your page layout.

#lorem(30)

#pagebreak()

// Change to blue styling for second page
#set page(background: scaffolding(stroke: blue + 1pt))

= Page 2 - Custom Styling

You can customize the border appearance by passing stroke parameters.

== Stroke Options

```typst
// Red thin border
scaffolding(stroke: red + 0.5pt)

// Blue thick border  
scaffolding(stroke: blue + 1pt)

// Dashed green border
scaffolding(stroke: (paint: green, dash: "dashed"))
```

#lorem(40)

#pagebreak()

// Multi-column layout
#set page(
  background: scaffolding(stroke: purple + 0.75pt),
  columns: 2,
)

= Page 3 - Multi-Column Layout

Scaffolder works with multi-column layouts too, showing the boundaries of each column.

#lorem(80)

#colbreak()

== Column 2

This is the second column. Notice how the scaffolding shows the column boundaries clearly.

#lorem(60)

#pagebreak()

// Reset to single column for summary
#set page(
  background: scaffolding(stroke: orange + 1pt),
  columns: 1,
)

= Summary

The `scaffolder` package provides:

- *Visual debugging* for page layouts
- *Customizable strokes* (color, width, dash pattern)
- *Multi-column support*
- *Minimal overhead* - just one function call

#v(1cm)

#align(center)[
  #rect(fill: orange.lighten(90%), inset: 1em, radius: 0.5em)[
    *Package:* scaffolder v0.2.1 \
    *Source:* https://typst.app/universe/package/scaffolder \
    *Inspired by:* LaTeX showframe package
  ]
]
