// THE SCRIVENER - Tarot Card
// League of Legends / Tarot Art Style

#set document(title: "The Scrivener - Tarot Card", author: "WAFT Pantheon")
#set page(
  width: 2.75in,
  height: 4.75in,
  margin: 0pt,
  fill: rgb("#0a0a12"),
)
#set text(font: "New Computer Modern", fill: white)

// Background gradient
#place(
  rect(
    width: 100%,
    height: 100%,
    fill: gradient.linear(
      rgb("#0a0a12"),
      rgb("#1a1a2e"),
      rgb("#16213e"),
      angle: 180deg,
    ),
  )
)

// Outer golden border
#place(
  rect(
    width: 100%,
    height: 100%,
    stroke: 3pt + gradient.linear(rgb("#c9a227"), rgb("#f4d03f"), rgb("#c9a227")),
    radius: 8pt,
  )
)

// Inner decorative border
#place(
  dx: 6pt,
  dy: 6pt,
  rect(
    width: 2.75in - 12pt,
    height: 4.75in - 12pt,
    stroke: 1pt + rgb("#c9a227").lighten(20%),
    radius: 6pt,
  )
)

// Top numeral
#place(
  top + center,
  dy: 15pt,
  [
    #text(
      size: 18pt,
      fill: gradient.linear(rgb("#c9a227"), rgb("#f4d03f")),
      weight: "bold",
    )[V]
  ]
)

// Card title at top
#place(
  top + center,
  dy: 38pt,
  [
    #rect(
      fill: rgb("#0a0a12").lighten(10%),
      stroke: 0.5pt + rgb("#c9a227"),
      inset: (x: 12pt, y: 4pt),
      radius: 3pt,
    )[
      #text(
        size: 8pt,
        fill: rgb("#c9a227"),
        tracking: 2pt,
      )[THE HIEROPHANT]
    ]
  ]
)

// Main illustration area
#place(
  center + horizon,
  dy: -20pt,
  [
    #rect(
      width: 2in,
      height: 2.2in,
      fill: gradient.radial(
        rgb("#1a365d"),
        rgb("#0a0a12"),
        center: (50%, 30%),
        radius: 100%,
      ),
      stroke: 1pt + rgb("#c9a227").darken(20%),
      radius: 4pt,
    )[
      #set align(center + horizon)
      
      // Mystical sigils background
      #place(center + horizon)[
        #text(size: 60pt, fill: rgb("#1a365d").lighten(20%))[✧]
      ]
      
      // Central figure silhouette
      #place(center + horizon, dy: -10pt)[
        #stack(
          dir: ttb,
          spacing: 5pt,
          // Halo of 14 sigils
          text(size: 8pt, fill: rgb("#f4d03f").transparentize(30%))[
            ✦ ✦ ✦ ✦ ✦ ✦ ✦
          ],
          // Head/face area
          text(size: 24pt, fill: rgb("#e8d5b7"))[◉],
          // Robes with text
          text(size: 10pt, fill: rgb("#8b7355"))[
            ⌇⌇⌇⌇⌇⌇⌇
          ],
          text(size: 10pt, fill: rgb("#8b7355"))[
            ≋≋≋≋≋≋≋≋≋
          ],
          // Hands holding items
          text(size: 12pt, fill: rgb("#c9a227"))[
            ✎ #h(20pt) ⬡
          ],
        )
      ]
      
      // Floating scrolls
      #place(top + left, dx: 10pt, dy: 20pt)[
        #text(size: 8pt, fill: rgb("#8b7355").lighten(20%))[📜]
      ]
      #place(top + right, dx: -15pt, dy: 30pt)[
        #text(size: 8pt, fill: rgb("#8b7355").lighten(20%))[📜]
      ]
      #place(bottom + left, dx: 15pt, dy: -20pt)[
        #text(size: 8pt, fill: rgb("#8b7355").lighten(20%))[📜]
      ]
      #place(bottom + right, dx: -10pt, dy: -25pt)[
        #text(size: 8pt, fill: rgb("#8b7355").lighten(20%))[📜]
      ]
    ]
  ]
)

// Entity name
#place(
  center + horizon,
  dy: 95pt,
  [
    #text(
      size: 16pt,
      fill: gradient.linear(rgb("#c9a227"), rgb("#f4d03f"), rgb("#c9a227")),
      weight: "bold",
      tracking: 3pt,
    )[THE SCRIVENER]
  ]
)

// Title
#place(
  center + horizon,
  dy: 115pt,
  [
    #text(
      size: 7pt,
      fill: rgb("#a0a0a0"),
      style: "italic",
    )[God of Reports & Intelligence Documents]
  ]
)

// Attributes bar
#place(
  bottom + center,
  dy: -75pt,
  [
    #rect(
      fill: rgb("#0a0a12").lighten(5%),
      stroke: 0.5pt + rgb("#c9a227").darken(30%),
      inset: 6pt,
      radius: 3pt,
    )[
      #text(size: 6pt, fill: rgb("#888888"))[
        #grid(
          columns: 4,
          gutter: 8pt,
          [#text(fill: rgb("#4a9eff"))[AIR-EARTH]],
          [#text(fill: rgb("#c9a227"))[MERCURY]],
          [#text(fill: rgb("#9b59b6"))[AQUARIUS]],
          [#text(fill: rgb("#e74c3c"))[JAN 20]],
        )
      ]
    ]
  ]
)

// Keywords
#place(
  bottom + center,
  dy: -50pt,
  [
    #text(size: 5pt, fill: rgb("#666666"), tracking: 1pt)[
      DOCUMENTATION • SYNTHESIS • TRUTH • CLARITY
    ]
  ]
)

// Sacred quote
#place(
  bottom + center,
  dy: -30pt,
  [
    #rect(
      width: 2.2in,
      fill: none,
      inset: 4pt,
    )[
      #text(
        size: 5.5pt,
        fill: rgb("#a0a0a0"),
        style: "italic",
      )[
        #set align(center)
        "If it wasn't documented, did it really happen?"
      ]
    ]
  ]
)

// Bottom decorative element
#place(
  bottom + center,
  dy: -12pt,
  [
    #text(size: 10pt, fill: rgb("#c9a227").darken(20%))[
      ═══════ ✧ ═══════
    ]
  ]
)

// Domain sigils in corners
#place(top + left, dx: 12pt, dy: 58pt)[
  #text(size: 8pt, fill: rgb("#c9a227").darken(30%))[⬡]
]
#place(top + right, dx: -18pt, dy: 58pt)[
  #text(size: 8pt, fill: rgb("#c9a227").darken(30%))[⬡]
]
