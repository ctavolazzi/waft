// Combined Typst Packages Demo
// All 6 packages in one document
// Created: 2026-01-19

#import "@preview/s6t5-page-bordering:1.0.0": s6t5-page-bordering
#import "@preview/drafting:0.2.2": *
#import "@preview/scaffolder:0.2.1": scaffolding
#import "@preview/codly:1.3.0": *
#import "@preview/codly-languages:0.1.1": *
#import "@preview/pinit:0.2.2": *
#import "@preview/showybox:2.0.4": showybox

// ============================================================================
// DOCUMENT SETUP
// ============================================================================

#set text(font: "New Computer Modern", size: 10pt)
#set page(paper: "us-letter", margin: (left: 1in, right: 1.5in, top: 1in, bottom: 1in))

// Initialize codly for code blocks
#show: codly-init.with()
#codly(languages: codly-languages)

// Set up drafting margins
#set-page-properties(margin-right: 1.5in)

// ============================================================================
// TITLE PAGE
// ============================================================================

#align(center + horizon)[
  #text(size: 32pt, weight: "bold")[
    Typst Packages Demo
  ]
  
  #v(1em)
  
  #text(size: 16pt, fill: gray)[
    A comprehensive guide to 5 essential Typst packages
  ]
  
  #v(2em)
  
  #rect(fill: blue.lighten(90%), inset: 1.5em, radius: 0.5em)[
    #text(size: 12pt)[
      *Packages Included:*
      
      #table(
        columns: (auto, auto),
        stroke: none,
        align: (left, left),
        [1. s6t5-page-bordering], [v1.0.0],
        [2. drafting], [v0.2.2],
        [3. scaffolder], [v0.2.1],
        [4. codly], [v1.3.0],
        [5. pinit], [v0.2.2],
        [6. showybox], [v2.0.4],
        [7. stack-pointer], [v0.1.0],
      )
    ]
  ]
  
  #v(2em)
  
  #text(fill: gray)[January 19, 2026]
]

#pagebreak()

// ============================================================================
// TABLE OF CONTENTS
// ============================================================================

#outline(
  title: [Table of Contents],
  indent: 1em,
)

#pagebreak()

// ============================================================================
// PACKAGE 1: s6t5-page-bordering
// ============================================================================

= Package 1: s6t5-page-bordering
#label("pkg-bordering")

*URL:* https://typst.app/universe/package/s6t5-page-bordering

== Overview

The `s6t5-page-bordering` package creates professional bordered pages with customizable headers and footers. Ideal for business documents, technical specifications, and formal reports.

== Key Features

- Professional page borders around content
- Custom header and footer support
- Configurable margins and spacing
- Consistent styling across pages

== Usage Example

```typst
#import "@preview/s6t5-page-bordering:1.0.0": s6t5-page-bordering

#show: s6t5-page-bordering.with(
  margin: (left: 30pt, right: 30pt, top: 60pt, bottom: 60pt),
  expand: 15pt,
  space-top: 15pt,
  space-bottom: 15pt,
  header: your-header,
  footer: your-footer,
)
```

== Parameters

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  [*Parameter*], [*Description*],
  [`margin`], [Dictionary with left, right, top, bottom values],
  [`expand`], [Border expansion beyond margin],
  [`space-top`], [Space between header and content],
  [`space-bottom`], [Space between content and footer],
  [`header`], [Custom header content],
  [`footer`], [Custom footer content],
)

#margin-note(side: left)[
  Great for formal business documents!
]

#pagebreak()

// ============================================================================
// PACKAGE 2: drafting
// ============================================================================

= Package 2: drafting
#label("pkg-drafting")

*URL:* https://typst.app/universe/package/drafting

== Overview

The `drafting` package provides margin notes and inline annotations for document review. Perfect for collaborative editing and feedback.

== Basic Margin Notes

#lorem(15)
#margin-note[This is a margin note on the right side]

#lorem(10)
#margin-note(side: left)[Left margin note]

#lorem(10)

== Styled Notes

#margin-note(stroke: blue + 2pt)[Blue styled note]
#lorem(8)

#margin-note(stroke: green + 2pt)[Green styled note]
#lorem(8)

== Inline Notes

#lorem(8)
#inline-note(par-break: false, stroke: (paint: orange, dash: "dashed"))[
  This is an inline annotation
]
#lorem(8)

== Multiple Reviewers

#let reviewer-a = margin-note.with(stroke: purple)
#let reviewer-b = margin-note.with(stroke: teal)

#lorem(8)
#reviewer-a[Reviewer A comment]
#lorem(6)
#reviewer-b(side: left)[Reviewer B feedback]
#lorem(8)

#pagebreak()

// ============================================================================
// PACKAGE 3: scaffolder
// ============================================================================

= Package 3: scaffolder
#label("pkg-scaffolder")

*URL:* https://typst.app/universe/package/scaffolder

== Overview

The `scaffolder` package shows borders around the main text area, header, and footer for debugging layout issues. Similar to LaTeX's `showframe` package.

== Usage

```typst
#import "@preview/scaffolder:0.2.1": scaffolding

#set page(background: scaffolding())
```

== Customization

```typst
// Red thin border
scaffolding(stroke: red + 0.5pt)

// Blue thick border  
scaffolding(stroke: blue + 1pt)

// Dashed green border
scaffolding(stroke: (paint: green, dash: "dashed"))
```

== Use Cases

1. *Debugging Margins* - See exact content boundaries
2. *Layout Design* - Understand page structure
3. *Teaching* - Demonstrate page anatomy
4. *Quality Assurance* - Verify consistent margins

#margin-note[
  Enable scaffolding temporarily to debug layout issues!
]

== Features

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  [*Feature*], [*Description*],
  [Visual debugging], [See exact content boundaries],
  [Custom strokes], [Color, width, dash patterns],
  [Multi-column], [Works with column layouts],
  [Minimal setup], [Single function call],
)

#pagebreak()

// ============================================================================
// PACKAGE 4: codly
// ============================================================================

= Package 4: codly
#label("pkg-codly")

*URL:* https://typst.app/universe/package/codly

== Overview

`Codly` supercharges code blocks with line numbering, syntax highlighting, language icons, annotations, and much more.

== Setup

```typst
#import "@preview/codly:1.3.0": *
#import "@preview/codly-languages:0.1.1": *
#show: codly-init.with()
#codly(languages: codly-languages)
```

== Code Examples

=== Python

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Calculate first 10 Fibonacci numbers
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")
```

=== Rust

```rust
fn main() {
    let numbers = vec![1, 2, 3, 4, 5];
    let sum: i32 = numbers.iter().sum();
    println!("Sum: {}", sum);
}
```

=== JavaScript

```javascript
const fetchData = async (url) => {
  const response = await fetch(url);
  return response.json();
};
```

#margin-note[
  Codly automatically detects languages and applies syntax highlighting!
]

== Features

- Line numbering with customizable format
- Syntax highlighting via language detection
- Language icons with codly-languages
- Zebra striping for readability
- Code highlights and annotations
- Smart indentation for wrapped lines

#pagebreak()

// ============================================================================
// PACKAGE 5: pinit
// ============================================================================

= Package 5: pinit
#label("pkg-pinit")

*URL:* https://typst.app/universe/package/pinit

== Overview

`Pinit` provides relative positioning by pins - place invisible markers in text and draw arrows, highlights, and annotations between them.

== Basic Highlighting

A simple #pin(1)highlighted phrase#pin(2) in text.

#pinit-highlight(1, 2)

#pinit-point-from(2, offset-dx: 20pt, offset-dy: 25pt)[
  This text is highlighted!
]

#v(2em)

== Arrows Between Elements

Connect #pin(3)this#pin(4) to #pin(5)that#pin(6).

#pinit-arrow(4, 5, start-dy: -3pt, end-dy: -3pt)

#v(1em)

== Multiple Highlights

Text with #pin("h1")red#pin("h1e"), #pin("h2")blue#pin("h2e"), and #pin("h3")green#pin("h3e") sections.

#pinit-highlight("h1", "h1e", fill: red.transparentize(70%))
#pinit-highlight("h2", "h2e", fill: blue.transparentize(70%))
#pinit-highlight("h3", "h3e", fill: green.transparentize(70%))

#v(1em)

== Key Functions

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  [*Function*], [*Description*],
  [`pin(name)`], [Place invisible marker],
  [`pinit-highlight()`], [Highlight between pins],
  [`pinit-arrow()`], [Arrow between pins],
  [`pinit-double-arrow()`], [Bidirectional arrow],
  [`pinit-point-to()`], [Arrow pointing to pin],
  [`pinit-point-from()`], [Arrow from pin to content],
  [`pinit-rect()`], [Rectangle around pins],
  [`pinit-line()`], [Line between pins],
)

#margin-note[
  Perfect for slides and educational materials!
]

#pagebreak()

// ============================================================================
// PACKAGE 6: showybox
// ============================================================================

= Package 6: showybox
#label("pkg-showybox")

*URL:* https://typst.app/universe/package/showybox

== Overview

`Showybox` creates colorful and customizable boxes for callouts, notes, warnings, and highlighted content.

== Basic Box

#showybox[
  A simple showybox with default styling.
]

== With Title

#showybox(
  title: "Note",
  [This showybox has a title section.]
)

== Custom Colors

#showybox(
  frame: (
    border-color: red.darken(50%),
    title-color: red.lighten(60%),
    body-color: red.lighten(80%)
  ),
  title-style: (color: black),
  title: "Warning",
  [Red-themed warning box with custom colors.]
)

#v(0.5em)

#showybox(
  frame: (
    border-color: blue.darken(50%),
    title-color: blue.lighten(60%),
    body-color: blue.lighten(80%)
  ),
  title-style: (color: black),
  title: "Information",
  [Blue information box.]
)

#v(0.5em)

#showybox(
  frame: (
    border-color: green.darken(50%),
    title-color: green.lighten(60%),
    body-color: green.lighten(80%)
  ),
  title-style: (color: black),
  title: "Success",
  [Green success notification.]
)

== With Shadow

#showybox(
  frame: (
    border-color: purple.darken(30%),
    title-color: purple.lighten(70%),
    body-color: purple.lighten(90%)
  ),
  shadow: (offset: 4pt),
  title: "Shadowed",
  [Box with shadow effect for depth.]
)

== Features

#margin-note[
  Great for callouts, warnings, and tips!
]

- Custom colors (title, body, footer, border)
- Shadow effects
- Dashed borders
- Rounded corners
- Boxed/floating titles
- Multi-section support
- Nestable boxes

#pagebreak()

// ============================================================================
// PACKAGE 7: stack-pointer
// ============================================================================

= Package 7: stack-pointer
#label("pkg-stack-pointer")

*URL:* https://typst.app/universe/package/stack-pointer

== Overview

`Stack Pointer` visualizes the execution of imperative programs, showing call stack frames and local variables step by step.

== Example Program

#showybox(
  frame: (border-color: gray, body-color: luma(250)),
  title: "C Program",
)[
```c
int main() {
  int x = foo();
  return 0;
}
int foo() { return 0; }
```
]

== Typst Representation

#showybox(
  frame: (border-color: blue, body-color: blue.lighten(95%)),
  title: "Stack Pointer Code",
)[
```typst
#let steps = execute({
  let foo() = func("foo", 6, l => {
    l(0); l(1); retval(0)
  })
  let main() = func("main", 1, l => {
    l(0); l(1)
    let (x, ..rest) = foo(); rest
    l(1, push("x", x)); l(2)
  })
  main(); l(none)
})
```
]

== Call Stack Visualization

#align(center)[
  #grid(
    columns: 3,
    gutter: 1.5em,
    [
      *Step 2*
      #rect(stroke: 1pt, inset: 0.4em)[
        #rect(fill: blue.lighten(80%), width: 100%, inset: 0.4em)[
          *main()* Line: 1
        ]
      ]
    ],
    [
      *Step 3*
      #rect(stroke: 1pt, inset: 0.4em)[
        #rect(fill: green.lighten(80%), width: 100%, inset: 0.4em)[
          *foo()* Line: 0
        ]
        #rect(fill: blue.lighten(80%), width: 100%, inset: 0.4em)[
          *main()* Line: 1
        ]
      ]
    ],
    [
      *Step 5*
      #rect(stroke: 1pt, inset: 0.4em)[
        #rect(fill: blue.lighten(80%), width: 100%, inset: 0.4em)[
          *main()* x = 0
        ]
      ]
    ],
  )
]

#margin-note[
  Great for CS education and teaching recursion!
]

== Key Functions

- `execute()` - Run program, collect steps
- `func(name, line, body)` - Define function
- `l(line)` - Mark current line
- `push(var, val)` - Add variable to stack
- `retval(value)` - Return from function

#pagebreak()

// ============================================================================
// SUMMARY
// ============================================================================

= Summary
#label("summary")

== All Packages at a Glance

#table(
  columns: (auto, auto, 1fr),
  stroke: 0.5pt,
  inset: 10pt,
  align: (left, center, left),
  [*Package*], [*Version*], [*Purpose*],
  [s6t5-page-bordering], [1.0.0], [Professional page borders with headers/footers],
  [drafting], [0.2.2], [Margin notes and inline annotations],
  [scaffolder], [0.2.1], [Layout debugging borders],
  [codly], [1.3.0], [Beautiful code blocks with syntax highlighting],
  [pinit], [0.2.2], [Pins, arrows, and relative positioning],
  [showybox], [2.0.4], [Colorful customizable boxes],
  [stack-pointer], [0.1.0], [Program execution visualization],
)

== Quick Import Reference

```typst
// All packages in one import block
#import "@preview/s6t5-page-bordering:1.0.0": s6t5-page-bordering
#import "@preview/drafting:0.2.2": *
#import "@preview/scaffolder:0.2.1": scaffolding
#import "@preview/codly:1.3.0": *
#import "@preview/codly-languages:0.1.1": *
#import "@preview/pinit:0.2.2": *
#import "@preview/showybox:2.0.4": showybox
#import "@preview/stack-pointer:0.1.0": *  // Requires Polylux
```

== Resources

- *Typst Universe:* https://typst.app/universe
- *Typst Documentation:* https://typst.app/docs
- *Typst Discord:* https://discord.gg/typst

#v(1cm)

#align(center)[
  #rect(fill: gradient.linear(blue, purple), inset: 1.5em, radius: 0.5em)[
    #text(fill: white, weight: "bold", size: 14pt)[
      Built with Typst + FastAPI + SvelteKit
    ]
  ]
]
