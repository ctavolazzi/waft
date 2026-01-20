// Showybox Demo - Colorful and Customizable Boxes
// https://typst.app/universe/package/showybox

#import "@preview/showybox:2.0.4": showybox

#set text(font: "New Computer Modern", size: 11pt)
#set page(paper: "us-letter", margin: 1in)

= Showybox Package Demo

*Showybox* creates colorful and customizable boxes for Typst documents.

== Basic Usage

#showybox[
  Hello world! This is a basic showybox with default styling.
]

== With Title

#showybox(
  title: "Important Notice",
  [This showybox has a title. Great for callouts and notes!]
)

== Custom Colors

#showybox(
  frame: (
    border-color: red.darken(50%),
    title-color: red.lighten(60%),
    body-color: red.lighten(80%)
  ),
  title-style: (
    color: black,
    weight: "regular",
    align: center
  ),
  title: "Red Alert Box",
  [This is a red-themed showybox with custom colors for the border, title background, and body background.]
)

#v(0.5em)

#showybox(
  frame: (
    border-color: blue.darken(50%),
    title-color: blue.lighten(60%),
    body-color: blue.lighten(80%)
  ),
  title-style: (
    color: black,
  ),
  title: "Information",
  [A blue-themed information box.]
)

#v(0.5em)

#showybox(
  frame: (
    border-color: green.darken(50%),
    title-color: green.lighten(60%),
    body-color: green.lighten(80%)
  ),
  title-style: (
    color: black,
  ),
  title: "Success",
  [A green success notification box.]
)

== With Shadow

#showybox(
  frame: (
    border-color: purple.darken(30%),
    title-color: purple.lighten(70%),
    body-color: purple.lighten(90%)
  ),
  shadow: (
    offset: 4pt,
    color: gray.lighten(50%)
  ),
  title: "Shadowed Box",
  [This showybox has a subtle shadow effect for depth.]
)

#pagebreak()

== Dashed Borders

#showybox(
  frame: (
    dash: "dashed",
    border-color: orange.darken(20%),
    body-color: orange.lighten(90%)
  ),
  body-style: (
    align: center
  ),
  [This box has dashed borders!]
)

== Multiple Sections

#showybox(
  frame: (
    border-color: teal.darken(30%),
    title-color: teal.lighten(70%),
    body-color: teal.lighten(90%)
  ),
  title: "Multi-Section Box",
  [First section of content.],
  [Second section - automatically separated.],
  [Third section with more content.]
)

== With Footer

#showybox(
  frame: (
    border-color: maroon.darken(20%),
    title-color: maroon.lighten(70%),
    body-color: maroon.lighten(90%),
    footer-color: maroon.lighten(80%)
  ),
  title: "Box with Footer",
  footer: "Source: Typst Universe",
  [This showybox includes both a title and a footer section.]
)

== Boxed Title Style

#showybox(
  title-style: (
    boxed-style: (
      anchor: (x: center, y: horizon),
      radius: 5pt,
    )
  ),
  frame: (
    title-color: navy,
    border-color: navy,
    body-color: navy.lighten(95%),
    thickness: 2pt,
    radius: 10pt,
  ),
  title: "Floating Title",
  [The title appears as a floating box above the main content!]
)

#pagebreak()

== Custom Styling Examples

#showybox(
  frame: (
    border-color: gradient.linear(red, orange, yellow),
    body-color: yellow.lighten(90%),
    thickness: 3pt,
    radius: 10pt,
  ),
  [A box with gradient-colored thick border and rounded corners.]
)

#v(1em)

#showybox(
  frame: (
    border-color: black,
    body-color: black.lighten(95%),
    radius: 0pt,
    thickness: 2pt,
  ),
  body-style: (
    align: center,
  ),
  [*Square corners* for a more formal look.]
)

== Nested Boxes

#showybox(
  frame: (
    border-color: blue.darken(30%),
    body-color: blue.lighten(90%)
  ),
  title: "Outer Box",
  [
    Content in the outer box.
    
    #showybox(
      frame: (
        border-color: green.darken(30%),
        body-color: green.lighten(90%)
      ),
      title: "Inner Box",
      [Nested showybox inside another!]
    )
    
    More content after the inner box.
  ]
)

== Summary

#showybox(
  frame: (
    border-color: purple,
    title-color: purple,
    body-color: purple.lighten(95%),
  ),
  title-style: (
    color: white,
    weight: "bold",
  ),
  shadow: (
    offset: 3pt,
  ),
  title: "Showybox Features",
  [
    - *Customizable colors* - title, body, footer, border
    - *Shadow effects* - configurable offset and color
    - *Border styles* - solid, dashed, custom thickness
    - *Rounded corners* - adjustable radius
    - *Boxed titles* - floating title style
    - *Multi-section* - automatic separators
    - *Footer support* - bottom content area
    - *Nestable* - boxes within boxes
  ]
)

#v(1cm)

#align(center)[
  #showybox(
    frame: (
      border-color: gradient.linear(blue, purple),
      body-color: white,
      thickness: 2pt,
      radius: 8pt,
    ),
    shadow: (offset: 4pt),
    [
      *Package:* showybox v2.0.4 \
      *Source:* https://typst.app/universe/package/showybox
    ]
  )
]
