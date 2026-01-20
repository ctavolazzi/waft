// Stack Pointer Demo - Program Execution Visualization
// https://typst.app/universe/package/stack-pointer
// Note: Requires compatible Polylux version

#set text(font: "New Computer Modern", size: 11pt)
#set page(paper: "us-letter", margin: 1in)

= Stack Pointer Package Demo

*Stack Pointer* is a library for visualizing the execution of imperative computer programs, particularly showing effects on the call stack: stack frames and local variables.

== Overview

This package helps you:
- Visualize program execution step-by-step
- Show call stack frames
- Display local variables in each frame
- Trace function calls and returns

== Example: C Program Visualization

Consider this simple C program:

#rect(fill: luma(245), inset: 1em, width: 100%)[
```c
int main() {
  int x = foo();
  return 0;
}

int foo() {
  return 0;
}
```
]

=== Typst Representation

#rect(fill: blue.lighten(95%), inset: 1em, width: 100%)[
```typst
#import "@preview/stack-pointer:0.1.0": *

#let steps = execute({
  let foo() = func("foo", 6, l => {
    l(0)
    l(1); retval(0)
  })
  let main() = func("main", 1, l => {
    l(0)
    l(1)
    let (x, ..rest) = foo(); rest
    l(1, push("x", x))
    l(2)
  })
  main(); l(none)
})
```
]

== Execution Steps Visualization

The `steps` variable contains an array where each element corresponds to one line of code execution.

#table(
  columns: (auto, auto, 1fr),
  stroke: 0.5pt,
  inset: 10pt,
  align: (center, center, left),
  [*Step*], [*Function*], [*State*],
  [1], [main], [Line 0 - Enter main()],
  [2], [main], [Line 1 - Before foo() call],
  [3], [foo], [Line 0 - Enter foo()],
  [4], [foo], [Line 1 - Return 0],
  [5], [main], [Line 1 - x = 0 (from foo)],
  [6], [main], [Line 2 - Return 0],
  [7], [-], [Program end],
)

== Key Functions

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 8pt,
  [*Function*], [*Description*],
  [`execute(body)`], [Execute program and collect execution steps],
  [`func(name, line, body)`], [Define a function with name, starting line, and body],
  [`l(line)`], [Mark current line number in execution],
  [`l(line, push(var, val))`], [Mark line and push variable to stack frame],
  [`retval(value)`], [Return a value from the current function],
  [`push(name, value)`], [Add a local variable to current stack frame],
)

#pagebreak()

== Call Stack Visualization

At each step, you can visualize the call stack:

#align(center)[
  #grid(
    columns: 3,
    gutter: 2em,
    [
      *Step 2*
      #rect(stroke: 2pt, inset: 0.5em)[
        #rect(fill: blue.lighten(80%), width: 100%, inset: 0.5em)[
          *main()*\
          Line: 1
        ]
      ]
    ],
    [
      *Step 3*
      #rect(stroke: 2pt, inset: 0.5em)[
        #rect(fill: green.lighten(80%), width: 100%, inset: 0.5em)[
          *foo()*\
          Line: 0
        ]
        #rect(fill: blue.lighten(80%), width: 100%, inset: 0.5em)[
          *main()*\
          Line: 1
        ]
      ]
    ],
    [
      *Step 5*
      #rect(stroke: 2pt, inset: 0.5em)[
        #rect(fill: blue.lighten(80%), width: 100%, inset: 0.5em)[
          *main()*\
          Line: 1\
          x = 0
        ]
      ]
    ],
  )
]

== Use Cases

#grid(
  columns: 2,
  gutter: 1em,
  [
    === Teaching
    - Explain function calls
    - Show stack behavior
    - Demonstrate recursion
  ],
  [
    === Presentations
    - Step through code
    - Animate execution
    - Works with Polylux
  ],
)

== Integration with Polylux

Stack Pointer is designed to work with Polylux for creating animated slide presentations:

#rect(fill: purple.lighten(95%), inset: 1em, width: 100%)[
```typst
#import "@preview/polylux:0.3.1": *
#import "@preview/stack-pointer:0.1.0": *

#let steps = execute({ ... })

#for step in steps {
  #slide[
    // Render current execution state
    // Show stack frames
    // Highlight current line
  ]
}
```
]

== Features Summary

- *Step-by-step execution* - Track each line of code
- *Call stack visualization* - See function stack frames
- *Variable tracking* - Monitor local variables per frame
- *Return value tracing* - Track function return values
- *Presentation integration* - Works with Polylux slides

#v(1cm)

#align(center)[
  #rect(fill: teal.lighten(90%), inset: 1em, radius: 0.5em)[
    *Package:* stack-pointer v0.1.0 \
    *Source:* https://typst.app/universe/package/stack-pointer \
    *Best for:* CS education, teaching, presentations \
    *Note:* Requires Polylux 0.3.1 compatibility
  ]
]
