// Pinit Demo - Relative Positioning by Pins
// https://typst.app/universe/package/pinit

#import "@preview/pinit:0.2.2": *

#set text(font: "New Computer Modern", size: 11pt)
#set page(paper: "us-letter", margin: 1in)

= Pinit Package Demo

*Pinit* provides relative positioning by pins, especially useful for making slides and adding annotations to text.

== Basic Highlighting

A simple #pin(1)highlighted text#pin(2) example.

#pinit-highlight(1, 2)

#pinit-point-from(2)[This text is highlighted!]

#v(2em)

== Arrows Between Elements

Let's connect #pin(3)this word#pin(4) to #pin(5)that word#pin(6).

#pinit-arrow(4, 5, start-dy: -5pt, end-dy: -5pt)

#v(1em)

== Mathematical Annotations

Consider the quadratic formula:

#pin(7)$ x = (-b plus.minus sqrt(b^2 - 4 a c)) / (2a) $#pin(8)

#pinit-highlight(7, 8, fill: yellow.transparentize(70%))

#pinit-point-from((7, 8), offset-dy: 40pt)[
  The famous quadratic formula!
]

#v(3em)

== Code Explanation

```python
def factorial(n):      # pin(a)
    if n <= 1:         # pin(b)
        return 1       # pin(c)
    return n * factorial(n-1)  # pin(d)
```

The function uses #pin("a")recursion#pin("a-end") to calculate factorials.

#pinit-highlight("a", "a-end", fill: green.transparentize(80%))

#v(1em)

== Multiple Highlights

This sentence has #pin("h1")multiple#pin("h1e") different #pin("h2")highlighted#pin("h2e") sections #pin("h3")throughout#pin("h3e").

#pinit-highlight("h1", "h1e", fill: red.transparentize(70%))
#pinit-highlight("h2", "h2e", fill: blue.transparentize(70%))
#pinit-highlight("h3", "h3e", fill: green.transparentize(70%))

#v(1em)

#pagebreak()

= Advanced Features

== Double Arrows

Bidirectional relationship: #pin("da1")Client#pin("da1e") #h(3em) #pin("da2")Server#pin("da2e")

#pinit-double-arrow("da1e", "da2", start-dx: 5pt, end-dx: -5pt)

#v(2em)

== Rectangles Around Content

#pin("r1")This entire block of text is surrounded by a rectangle to draw attention to it.#pin("r2")

#pinit-rect("r1", "r2", stroke: 2pt + blue, radius: 5pt)

#v(2em)

== Lines Between Points

Start #pin("l1")here#pin("l1e") and end #pin("l2")there#pin("l2e").

#pinit-line("l1e", "l2", stroke: 2pt + red)

#v(2em)

== Pointing To Content

The #pin("pt1")important concept#pin("pt2") is explained here.

#pinit-point-to(
  "pt1",
  offset-dx: -60pt,
  offset-dy: -40pt,
  pin-dy: -8pt,
)[Key idea!]

#v(3em)

== Complex Diagram Example

#align(center)[
  #box(width: 80%)[
    #pin("box1")#rect(inset: 1em, fill: blue.lighten(80%))[Input Data]#pin("box1e")
    #h(1fr)
    #pin("box2")#rect(inset: 1em, fill: green.lighten(80%))[Process]#pin("box2e")
    #h(1fr)
    #pin("box3")#rect(inset: 1em, fill: orange.lighten(80%))[Output]#pin("box3e")
  ]
]

#pinit-arrow("box1e", "box2", start-dx: 5pt, end-dx: -5pt)
#pinit-arrow("box2e", "box3", start-dx: 5pt, end-dx: -5pt)

#v(2em)

== Summary

Pinit provides:

- *pin()* - Place invisible markers in text
- *pinit-highlight()* - Highlight between pins
- *pinit-arrow()* - Draw arrows between pins
- *pinit-double-arrow()* - Bidirectional arrows
- *pinit-point-to()* - Arrow pointing to pin
- *pinit-point-from()* - Arrow from pin to content
- *pinit-rect()* - Rectangle around pins
- *pinit-line()* - Simple line between pins
- *pinit-place()* - Place content at pin location

#v(1cm)

#align(center)[
  #rect(fill: purple.lighten(90%), inset: 1em, radius: 0.5em)[
    *Package:* pinit v0.2.2 \
    *Source:* https://typst.app/universe/package/pinit \
    *Best for:* Slides, annotations, diagrams
  ]
]
