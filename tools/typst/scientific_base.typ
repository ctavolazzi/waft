// scientific_base.typ - Foundation for Scientific Reports
// Part of DIALECTIC Engine Tools
// 
// Usage:
//   #import "scientific_base.typ": scientific-doc
//   #show: scientific-doc.with(title: "My Report", authors: ("Author",))

#let scientific-doc(
  title: "",
  authors: (),
  abstract: none,
  date: datetime.today().display("[month repr:long] [day], [year]"),
  keywords: (),
  body
) = {
  // Set document metadata
  set document(title: title, author: authors)
  
  // Page setup
  set page(
    paper: "us-letter",
    margin: (x: 1in, y: 1in),
    header: context {
      if counter(page).get().first() > 1 [
        #set text(8pt)
        #smallcaps(title) 
        #h(1fr) 
        #date
      ]
    },
    footer: [
      #set text(8pt)
      #h(1fr)
      #context counter(page).display("1 / 1", both: true)
      #h(1fr)
    ]
  )

  // Font setup
  set text(font: "New Computer Modern", size: 11pt)
  set par(justify: true, leading: 0.65em)

  // Title Block
  align(center)[
    #v(2em)
    #text(17pt, weight: "bold")[#title]
    #v(1em)
    #text(12pt)[#authors.join(", ")]
    #v(0.5em)
    #text(10pt, style: "italic")[#date]
    #v(1em)
  ]

  // Abstract
  if abstract != none {
    pad(x: 2em)[
      #text(weight: "bold", size: 10pt)[Abstract]
      #v(0.3em)
      #text(size: 10pt)[#abstract]
    ]
    v(0.5em)
  }

  // Keywords
  if keywords.len() > 0 {
    pad(x: 2em)[
      #text(weight: "bold", size: 9pt)[Keywords: ]
      #text(size: 9pt, style: "italic")[#keywords.join(", ")]
    ]
    v(1em)
  }

  line(length: 100%, stroke: 0.5pt)
  v(1em)

  // Heading Styling
  show heading.where(level: 1): it => {
    v(1em)
    text(14pt, weight: "bold")[
      #counter(heading).display("1.")
      #h(0.5em)
      #it.body
    ]
    v(0.5em)
  }
  
  show heading.where(level: 2): it => {
    v(0.8em)
    text(12pt, weight: "bold")[
      #counter(heading).display("1.1")
      #h(0.5em)
      #it.body
    ]
    v(0.3em)
  }
  
  show heading.where(level: 3): it => {
    v(0.5em)
    text(11pt, weight: "bold", style: "italic")[#it.body]
    v(0.2em)
  }

  // Body Content
  body
}

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

// Callout box for important notes
#let callout(title: "Note", body, color: blue) = {
  block(
    fill: color.lighten(90%),
    inset: 12pt,
    radius: 4pt,
    width: 100%,
    stroke: (left: 3pt + color),
  )[
    #text(weight: "bold", fill: color)[#title]
    #v(0.3em)
    #body
  ]
}

// Code block with syntax highlighting placeholder
#let code-block(lang: "python", code) = {
  block(
    fill: luma(245),
    inset: 10pt,
    radius: 4pt,
    width: 100%,
  )[
    #text(font: "Fira Code", size: 9pt)[
      #raw(code, lang: lang)
    ]
  ]
}

// Figure with caption
#let fig(image-path, caption: "", width: 80%) = {
  figure(
    image(image-path, width: width),
    caption: caption,
  )
}

// Table with header styling
#let data-table(headers, ..rows) = {
  table(
    columns: headers.len(),
    fill: (_, y) => if y == 0 { luma(230) } else { none },
    ..headers.map(h => text(weight: "bold")[#h]),
    ..rows.pos().flatten(),
  )
}

// Citation placeholder
#let cite-ref(key) = {
  text(fill: blue)[\[#key\]]
}

// Equation with number
#let eq(content) = {
  math.equation(
    block: true,
    numbering: "(1)",
    content,
  )
}
