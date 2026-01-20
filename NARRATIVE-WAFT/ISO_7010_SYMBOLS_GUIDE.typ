#import "@preview/s6t5-page-bordering:1.0.0": s6t5-page-bordering
#import "@preview/typsium-iso-7010:0.1.0": *

// Custom header for ISO 7010 Symbols Guide
#let header = {
  set align(bottom)
  show table.cell.where(y: 0): set align(left)
  set text(weight: "bold", size: 9pt)
  table(
    stroke: (y: none),
    columns: (0.8fr, 1.4fr, 0.8fr),
    rows: 1fr,
    table.hline(),
    [ISO-7010-GUIDE], [ISO 7010 Safety Symbols Reference], [
      #context counter(page).display(
        "1 / 1",
        both: true,
      )
    ],
  )
}

// Custom footer
#let footer = {
  set text(weight: "bold", size: 9pt)
  table(
    stroke: (y: none),
    columns: (0.8fr, 1.4fr, 0.8fr),
    rows: 1fr,
    [ISO-7010-GUIDE], [typsium-iso-7010 Package v0.1.0], [
      #context counter(page).display(
        "1 / 1",
        both: true,
      )
    ],
    table.hline(),
  )
}

#show: s6t5-page-bordering.with(
  margin: (left: 30pt, right: 30pt, top: 60pt, bottom: 60pt),
  expand: 15pt,
  space-top: 15pt,
  space-bottom: 15pt,
  stroke-header: 1pt,
  stroke-footer: 1pt,
  header: header,
  footer: footer,
)

// Color scheme
#let primary-blue = rgb("#1a237e")
#let warning-yellow = rgb("#f57f17")
#let danger-red = rgb("#c62828")
#let safety-green = rgb("#2e7d32")
#let info-blue = rgb("#0277bd")
#let text-dark = rgb("#212121")

#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true, first-line-indent: 0.5cm)
#set heading(numbering: "1.")

= ISO 7010 Safety Symbols Guide

#align(center)[
  #text(size: 14pt, style: "italic", fill: primary-blue)[
    Complete Reference for typsium-iso-7010 Package
    #linebreak()
    Version 0.1.0
  ]
]

#v(1cm)

== Introduction

The `typsium-iso-7010` package provides ISO 7010 standard safety symbols for use in Typst documents. ISO 7010 is an international standard that specifies safety signs used in workplaces and public areas for accident prevention, fire protection, health hazard information, and emergency evacuation.

#block(
  fill: rgb("#e3f2fd"),
  stroke: primary-blue,
  radius: 4pt,
  inset: 12pt,
  width: 100%,
)[
  #text(weight: "bold", fill: primary-blue)[Package Information]
  #v(6pt)
  #text[
    • Package: `@preview/typsium-iso-7010:0.1.0`
    #linebreak()
    • License: MIT
    #linebreak()
    • Authors: Typsium Community & Ants Aare Alamaa
    #linebreak()
    • Standard: ISO 7010:2019 (International Organization for Standardization)
    #linebreak()
    • Reference: https://en.wikipedia.org/wiki/ISO_7010
  ]
]

ISO 7010 uses colors and principles set out in ISO 3864 for these symbols, and is intended to provide "safety information that relies as little as possible on the use of words to achieve understanding." The standard was first published in October 2003, with the latest version being ISO 7010:2019 (as of 2022).

#v(1cm)

== Shape and Colour Specifications

ISO 7010 specifies five combinations of shape and colour to distinguish between the type of information presented:

#table(
  columns: (1.2fr, 2fr, 1fr, 1fr),
  stroke: 1pt,
  fill: (x, y) => if calc.even(y) { rgb("#f5f5f5") } else { white },
  align: left,
  [*Sign Type*], [*Meaning*], [*Colour*], [*Shape*],
  [Prohibition sign], [Must not do], [Red], [Circle with diagonal line],
  [Mandatory sign], [Must do], [Blue], [Circle],
  [Warning sign], [Warn of hazard], [Yellow], [Equilateral triangle with rounded corners],
  [Safe condition sign], [Identifying of safety equipment and exits], [Green], [Square or rectangular],
  [Fire safety sign], [Identifying of firefighting equipment], [Red], [Square],
)

#v(1cm)

== ISO 7010 Symbol Numbering System

ISO 7010 uses a systematic numbering system where:
- #text(weight: "bold")[E] numbers refer to Emergency (safe condition signs)
- #text(weight: "bold")[F] numbers refer to Fire protection
- #text(weight: "bold")[M] numbers refer to Mandatory actions
- #text(weight: "bold")[P] numbers refer to Prohibited actions
- #text(weight: "bold")[W] numbers refer to Warnings of hazards

For example: E001 = Emergency exit, F001 = Fire extinguisher, M003 = Wear ear protection, P002 = No smoking, W012 = Electricity.

#block(
  fill: rgb("#fff3e0"),
  stroke: warning-yellow,
  radius: 4pt,
  inset: 12pt,
  width: 100%,
)[
  #text(weight: "bold", fill: warning-yellow)[Note on Symbol Availability]
  #v(6pt)
  #text[
    The `typsium-iso-7010` package may not include all symbols from the ISO 7010 standard. The package uses numeric indices (1, 2, 3, etc.) rather than ISO codes (E001, F001, etc.). Check the package documentation or test symbol numbers to determine which symbols are available in your version.
  ]
]

#v(1cm)

== Installation and Import

To use ISO 7010 symbols in your Typst document, import the package:

```typst
#import "@preview/typsium-iso-7010:0.1.0": *
```

This imports all available symbol functions into your document's namespace.

#v(1cm)

== Symbol Categories

ISO 7010 symbols are organized into several categories:

#grid(
  columns: 2,
  column-gutter: 12pt,
  row-gutter: 8pt,
)[
  #block(
    fill: warning-yellow,
    stroke: rgb("#f9a825"),
    radius: 4pt,
    inset: 10pt,
    width: 100%,
  )[#text(weight: "bold")[Warning Signs]]
  
  #block(
    fill: danger-red,
    stroke: rgb("#d32f2f"),
    radius: 4pt,
    inset: 10pt,
    width: 100%,
  )[#text(weight: "bold", fill: white)[Fire Signs]]
  
  #block(
    fill: safety-green,
    stroke: rgb("#388e3c"),
    radius: 4pt,
    inset: 10pt,
    width: 100%,
  )[#text(weight: "bold", fill: white)[Emergency Signs]]
  
  #block(
    fill: info-blue,
    stroke: rgb("#01579b"),
    radius: 4pt,
    inset: 10pt,
    width: 100%,
  )[#text(weight: "bold", fill: white)[Mandatory Signs]]
]

#v(1cm)

== Warning Signs

Warning signs alert people to potential hazards. They typically use a yellow triangle with a black border and symbol.

=== Basic Usage

```typst
#warning-sign(n, height: 2cm)
```

Where `n` is the symbol number (1, 2, 3, etc.) and `height` controls the size of the symbol.

=== Available Warning Symbols

#text(size: 9pt, style: "italic")[Note: Package uses numeric indices. ISO codes (W001, W002, etc.) are provided for reference. Check package for available symbols.]

#grid(
  columns: (2fr, 3fr),
  column-gutter: 16pt,
  row-gutter: 12pt,
  align: center,
)[
  #warning-sign(1, height: 2cm)
  [
    #text(weight: "bold")[Warning Sign 1 (W001)]
    #linebreak()
    #text(style: "italic")[General warning sign]
    #linebreak()
    #v(4pt)
    #text(size: 9pt)[Indicates a general warning of a potential hazard. Use when the specific nature of the hazard is not covered by other warning signs. Yellow triangle with rounded corners.]
  ]
  
  #warning-sign(2, height: 2cm)
  [
    #text(weight: "bold")[Warning Sign 2 (W002)]
    #linebreak()
    #text(style: "italic")[Explosive material]
    #linebreak()
    #v(4pt)
    #text(size: 9pt)[Warns of the presence of explosive materials. Use in areas where explosives are stored or handled.]
  ]
  
  #warning-sign(3, height: 2cm)
  [
    #text(weight: "bold")[Warning Sign 3 (W003)]
    #linebreak()
    #text(style: "italic")[Radioactive material or ionizing radiation]
    #linebreak()
    #v(4pt)
    #text(size: 9pt)[Warns of the presence of ionizing radiation. Use in areas with radioactive materials or radiation sources.]
  ]
]

=== Common Warning Symbols (ISO 7010 Reference)

According to ISO 7010:2019, common warning symbols include:
- W001 – General warning sign
- W002 – Explosive material
- W003 – Radioactive material or ionizing radiation
- W004 – Laser beam
- W005 – Non-ionizing radiation
- W006 – Magnetic field
- W007 – Floor-level obstacle
- W008 – Drop (fall)
- W009 – Biological hazard
- W010 – Low temperature/freezing conditions
- W011 – Slippery surface
- W012 – Electricity
- W013 – Guard dog
- W014 – Forklift trucks and other industrial vehicles
- W015 – Overhead load
- W016 – Toxic material
- W017 – Hot surface
- W018 – Automatic start-up
- W019 – Crushing
- W020 – Overhead obstacle
- W021 – Flammable material
- W022 – Sharp element
- W023 – Corrosive substance

And many more (W001 through W089 in ISO 7010:2019). Check the package documentation to see which symbols are available.

#v(1cm)

== Fire Signs

Fire signs indicate the location of fire-fighting equipment and fire-related facilities. They use a red square with a white symbol.

=== Basic Usage

```typst
#fire-sign(n, height: 2cm)
```

=== Available Fire Symbols

#text(size: 9pt, style: "italic")[Note: Package uses numeric indices. ISO codes (F001, F002, etc.) are provided for reference.]

#grid(
  columns: (2fr, 3fr),
  column-gutter: 16pt,
  row-gutter: 12pt,
  align: center,
)[
  #fire-sign(1, height: 2cm)
  [
    #text(weight: "bold")[Fire Sign 1 (F001)]
    #linebreak()
    #text(style: "italic")[Fire extinguisher]
    #linebreak()
    #v(4pt)
    #text(size: 9pt)[Indicates the location of a fire extinguisher. Red square with white symbol. Place near fire extinguisher equipment.]
  ]
  
  #fire-sign(2, height: 2cm)
  [
    #text(weight: "bold")[Fire Sign 2 (F002)]
    #linebreak()
    #text(style: "italic")[Fire hose reel]
    #linebreak()
    #v(4pt)
    #text(size: 9pt)[Indicates the location of a fire hose reel. Use to mark fire hose storage locations.]
  ]
]

=== Common Fire Symbols (ISO 7010 Reference)

According to ISO 7010:2019, common fire symbols include:
- F001 – Fire extinguisher
- F002 – Fire hose reel
- F003 – Fire ladder
- F004 – Collection of firefighting equipment
- F005 – Fire alarm call point
- F006 – Fire emergency telephone
- F007 – Fire protection door
- F008 – Fixed fire extinguishing battery
- F009 – Wheeled fire extinguisher
- F010 – Portable foam applicator unit
- F011 – Water fog applicator
- F012 – Fixed fire extinguishing installation
- F013 – Fixed fire extinguishing bottle
- F014 – Remote release station
- F015 – Fire monitor
- F016 – Fire blanket
- F017 – Firefighters' lift
- F018 – Fire alarm flashing light
- F019 – Unconnected fire hose

All fire signs use a red square background with white symbols.

#v(1cm)

== Emergency Signs

Emergency signs indicate emergency exits, first aid stations, and other emergency facilities. They use a green square with a white symbol.

=== Basic Usage

```typst
#emergency-sign(n, height: 2cm)
```

=== Available Emergency Symbols

#text(size: 9pt, style: "italic")[Note: Package uses numeric indices. ISO codes (E001, E002, etc.) are provided for reference.]

#grid(
  columns: (2fr, 3fr),
  column-gutter: 16pt,
  row-gutter: 12pt,
  align: center,
)[
  #emergency-sign(1, height: 2cm)
  [
    #text(weight: "bold")[Emergency Sign 1 (E001/E002)]
    #linebreak()
    #text(style: "italic")[Emergency exit (left/right hand)]
    #linebreak()
    #v(4pt)
    #text(size: 9pt)[Indicates an emergency exit. E001 = left hand, E002 = right hand. Green square with white symbol. Use to mark doors, corridors, or paths leading to safety.]
  ]
  
  #emergency-sign(2, height: 2cm)
  [
    #text(weight: "bold")[Emergency Sign 2 (E003)]
    #linebreak()
    #text(style: "italic")[First aid]
    #linebreak()
    #v(4pt)
    #text(size: 9pt)[Indicates the location of first aid equipment or a first aid station. Place near first aid kits or medical facilities.]
  ]
  
  #emergency-sign(3, height: 2cm)
  [
    #text(weight: "bold")[Emergency Sign 3 (E004)]
    #linebreak()
    #text(style: "italic")[Emergency telephone]
    #linebreak()
    #v(4pt)
    #text(size: 9pt)[Indicates the location of an emergency telephone. Mark emergency communication devices.]
  ]
]

=== Common Emergency Symbols (ISO 7010 Reference)

According to ISO 7010:2019, common emergency (safe condition) symbols include:
- E001 – Emergency exit (left hand)
- E002 – Emergency exit (right hand)
- E003 – First aid
- E004 – Emergency telephone
- E007 – Evacuation assembly point
- E008 – Break to obtain access
- E009 – Doctor
- E010 – Automated external heart defibrillator
- E011 – Eyewash station
- E012 – Safety shower
- E013 – Stretcher
- E015 – Drinking water
- E016 – Emergency window with escape ladder
- E017 – Rescue window
- E020 – Emergency stop button
- E021 – Protection shelter
- E024 – Evacuation temporary refuge
- E025 – Emergency hammer
- E060 – Evacuation chair
- E061 – Water life-saving equipment
- E062 – Tsunami evacuation area
- E063 – Tsunami evacuation building
- E064 – First aid responder
- E075 – Lifeguard

And many more (E001 through E076 in ISO 7010:2019). All emergency signs use a green square or rectangular background with white symbols.

#v(1cm)

== Directional Arrows

The package also provides directional arrows for use with emergency and fire signs to indicate direction.

=== Emergency Arrows

```typst
#emergency-arrow(direction: "up", height: 2cm)
#emergency-arrow(direction: "down", height: 2cm)
#emergency-arrow(direction: "left", height: 2cm)
#emergency-arrow(direction: "right", height: 2cm)
```

#grid(
  columns: 4,
  column-gutter: 12pt,
  align: center,
)[
  [
    #emergency-arrow(direction: "up", height: 1.5cm)
    #linebreak()
    #text(size: 9pt)[Up]
  ]
  [
    #emergency-arrow(direction: "down", height: 1.5cm)
    #linebreak()
    #text(size: 9pt)[Down]
  ]
  [
    #emergency-arrow(direction: "left", height: 1.5cm)
    #linebreak()
    #text(size: 9pt)[Left]
  ]
  [
    #emergency-arrow(direction: "right", height: 1.5cm)
    #linebreak()
    #text(size: 9pt)[Right]
  ]
]

=== Fire Arrows

```typst
#fire-arrow(direction: "up", height: 2cm)
#fire-arrow(direction: "down", height: 2cm)
#fire-arrow(direction: "left", height: 2cm)
#fire-arrow(direction: "right", height: 2cm)
```

#grid(
  columns: 4,
  column-gutter: 12pt,
  align: center,
)[
  [
    #fire-arrow(direction: "up", height: 1.5cm)
    #linebreak()
    #text(size: 9pt)[Up]
  ]
  [
    #fire-arrow(direction: "down", height: 1.5cm)
    #linebreak()
    #text(size: 9pt)[Down]
  ]
  [
    #fire-arrow(direction: "left", height: 1.5cm)
    #linebreak()
    #text(size: 9pt)[Left]
  ]
  [
    #fire-arrow(direction: "right", height: 1.5cm)
    #linebreak()
    #text(size: 9pt)[Right]
  ]
]

#v(1cm)

== Common Usage Patterns

=== Inline Usage

Symbols can be used inline with text:

```typst
#warning-sign(3, height: 1em) indicates electrical hazards.
```

#warning-sign(3, height: 1em) indicates electrical hazards.

=== In Grids

Organize multiple symbols in a grid:

```typst
#grid(
  columns: 3,
  column-gutter: 12pt,
  align: center,
)[
  #warning-sign(1, height: 2cm),
  #fire-sign(1, height: 2cm),
  #emergency-sign(1, height: 2cm),
]
```

#grid(
  columns: 3,
  column-gutter: 12pt,
  align: center,
)[
  #warning-sign(1, height: 2cm),
  #fire-sign(1, height: 2cm),
  #emergency-sign(1, height: 2cm),
]

=== With Labels

Combine symbols with descriptive text:

```typst
#grid(
  columns: (1fr, 2fr),
  align: center,
)[
  #emergency-sign(1, height: 2cm),
  [
    *Emergency Exit*
    #linebreak()
    Use this door in case of emergency
  ],
]
```

#grid(
  columns: (1fr, 2fr),
  align: center,
)[
  #emergency-sign(1, height: 2cm),
  [
    *Emergency Exit*
    #linebreak()
    Use this door in case of emergency
  ],
]

=== With Directional Arrows

Combine signs with directional arrows:

```typst
#grid(
  columns: 2,
  align: center,
)[
  #emergency-sign(1, height: 2cm),
  #emergency-arrow(direction: "right", height: 2cm),
]
```

#grid(
  columns: 2,
  align: center,
)[
  #emergency-sign(1, height: 2cm),
  #emergency-arrow(direction: "right", height: 2cm),
]

#v(1cm)

== Size Guidelines

The `height` parameter controls the size of symbols. Recommended sizes:

#block(
  fill: rgb("#f5f5f5"),
  stroke: primary-blue,
  radius: 4pt,
  inset: 12pt,
  width: 100%,
)[
  #text(weight: "bold")[Size Recommendations:]
  #v(6pt)
  #text[
    • Inline text: `height: 1em` (matches text size)
    #linebreak()
    • Small displays: `height: 1cm` to `2cm`
    #linebreak()
    • Standard signs: `height: 3cm` to `5cm`
    #linebreak()
    • Large displays: `height: 10cm` or larger
  ]
]

#v(1cm)

== Best Practices

=== Placement

#text(weight: "bold")[1. Visibility]
Place symbols where they are clearly visible and not obstructed.

#text(weight: "bold")[2. Consistency]
Use consistent sizes for the same type of symbol throughout your document.

#text(weight: "bold")[3. Context]
Always provide context or labels when the meaning might not be immediately clear.

#text(weight: "bold")[4. Standards Compliance]
Follow ISO 7010 guidelines for proper symbol usage and placement.

=== Color Usage

ISO 7010 specifies standard colors:
- Warning signs: Yellow background (hex: f57f17)
- Fire signs: Red background (hex: c62828)
- Emergency signs: Green background (hex: 2e7d32)
- Prohibition signs: Red circle with diagonal line
- Mandatory signs: Blue circle

The package handles colors automatically according to ISO 7010 standards.

#v(1cm)

== Complete Function Reference

=== Warning Signs

- `#warning-sign(n, height: <size>)` - Display warning sign number `n`
  - Available numbers: 1, 2, 3, 4, 5, and more (check package documentation)
  - Height: Any valid Typst length (e.g., `2cm`, `1em`, `10pt`)

=== Fire Signs

- `#fire-sign(n, height: <size>)` - Display fire sign number `n`
  - Available numbers: 1, 2, 3, 4, and more
  - Height: Any valid Typst length

=== Emergency Signs

- `#emergency-sign(n, height: <size>)` - Display emergency sign number `n`
  - Available numbers: 1, 2, 3, 4, 5, and more
  - Height: Any valid Typst length

=== Directional Arrows

- `#emergency-arrow(direction: "<dir>", height: <size>)` - Emergency arrow
  - Directions: `"up"`, `"down"`, `"left"`, `"right"`
  - Height: Any valid Typst length

- `#fire-arrow(direction: "<dir>", height: <size>)` - Fire arrow
  - Directions: `"up"`, `"down"`, `"left"`, `"right"`
  - Height: Any valid Typst length

#v(1cm)

== Examples

=== Example 1: Safety Information Panel

```typst
#grid(
  columns: 2,
  column-gutter: 16pt,
  row-gutter: 12pt,
)[
  #warning-sign(3, height: 3cm),
  [
    *Electrical Hazard*
    #linebreak()
    High voltage equipment. Do not touch.
  ],
  #fire-sign(1, height: 3cm),
  [
    *Fire Extinguisher*
    #linebreak()
    Located 10 meters to your right.
  ],
  #emergency-sign(1, height: 3cm),
  [
    *Emergency Exit*
    #linebreak()
    Use in case of emergency.
  ],
]
```

#grid(
  columns: 2,
  column-gutter: 16pt,
  row-gutter: 12pt,
)[
  #warning-sign(3, height: 3cm),
  [
    *Electrical Hazard*
    #linebreak()
    High voltage equipment. Do not touch.
  ],
  #fire-sign(1, height: 3cm),
  [
    *Fire Extinguisher*
    #linebreak()
    Located 10 meters to your right.
  ],
  #emergency-sign(1, height: 3cm),
  [
    *Emergency Exit*
    #linebreak()
    Use in case of emergency.
  ],
]

=== Example 2: Emergency Evacuation Route

```typst
#grid(
  columns: 4,
  align: center,
)[
  #emergency-sign(1, height: 2cm),
  #emergency-arrow(direction: "right", height: 2cm),
  #emergency-arrow(direction: "right", height: 2cm),
  #emergency-sign(1, height: 2cm),
]
```

#grid(
  columns: 4,
  align: center,
)[
  #emergency-sign(1, height: 2cm),
  #emergency-arrow(direction: "right", height: 2cm),
  #emergency-arrow(direction: "right", height: 2cm),
  #emergency-sign(1, height: 2cm),
]

#v(1cm)

== Mandatory and Prohibition Signs

The ISO 7010 standard also includes Mandatory signs (M codes) and Prohibition signs (P codes), though the `typsium-iso-7010` package may not include all of these.

=== Mandatory Signs (M codes)

Mandatory signs indicate actions that must be taken. They use a blue circle with white symbols. Common examples include:
- M001 – General mandatory action sign
- M002 – Refer to instruction manual/booklet
- M003 – Wear ear protection
- M004 – Wear eye protection
- M005 – Connect an earth terminal to the ground
- M006 – Disconnect mains plug from electrical outlet
- M008 – Wear safety footwear
- M009 – Wear protective gloves
- M010 – Wear protective clothing
- M011 – Wash your hands
- M012 – Use handrail
- M013 – Wear a face shield
- M014 – Wear head protection
- M015 – Wear high-visibility clothing
- M016 – Wear a mask
- M017 – Wear respiratory protection
- M018 – Wear a safety harness

And many more (M001 through M072 in ISO 7010:2019).

=== Prohibition Signs (P codes)

Prohibition signs indicate actions that must not be done. They use a red circle with a diagonal line and white/black symbols. Common examples include:
- P001 – General prohibition sign
- P002 – No smoking
- P003 – No open flame; Fire, open ignition source and smoking prohibited
- P004 – No thoroughfare
- P005 – Not drinking water
- P006 – No access for forklift trucks and industrial vehicles
- P009 – No climbing
- P010 – Do not touch
- P011 – Do not extinguish with water
- P013 – No activated mobile phone
- P020 – Do not use lift in the event of fire
- P021 – No dogs
- P022 – No eating or drinking
- P029 – No photography
- P036 – No children allowed
- P080 – No access for unauthorized persons

And many more (P001 through P081 in ISO 7010:2019).

#v(1cm)

== Additional Resources

#block(
  fill: rgb("#e8f5e9"),
  stroke: safety-green,
  radius: 4pt,
  inset: 12pt,
  width: 100%,
)[
  #text(weight: "bold", fill: safety-green)[Reference Materials]
  #v(6pt)
  #text[
    • ISO 7010:2019 Standard: Official ISO documentation (www.iso.org/standard/72424.html)
    #linebreak()
    • Wikipedia Reference: https://en.wikipedia.org/wiki/ISO_7010 (comprehensive symbol list)
    #linebreak()
    • Package Repository: Check GitHub for latest updates
    #linebreak()
    • Typst Universe: https://typst.app/universe/package/typsium-iso-7010
    #linebreak()
    • ISO 3864: Safety colors and safety signs (base standard for ISO 7010)
  ]
]

#v(1cm)

== Conclusion

The `typsium-iso-7010` package provides a comprehensive set of ISO 7010 safety symbols for use in Typst documents. By following this guide and the ISO 7010 standard, you can create clear, professional safety documentation that communicates hazards and emergency information effectively.

Remember to:
- Use appropriate symbol sizes for your context
- Provide clear labels and descriptions
- Follow ISO 7010 color and design standards
- Test symbol visibility in your final document

#v(2cm)

#align(center)[
  #text(size: 10pt, style: "italic", fill: primary-blue)[
    Document prepared for WAFT Project
    #linebreak()
    ISO 7010 Safety Symbols Reference Guide
    #linebreak()
    Last updated: January 2026
  ]
]
