// Teleport Massive D&D Campaign Book Template
// A homebrew D&D 5e campaign setting based on the Teleport Massive corporation

#set page(margin: (top: 2.5cm, bottom: 2cm, left: 2cm, right: 2cm))
#set text(font: "New Computer Modern", size: 11pt, leading: 0.65em)
#set heading(numbering: "1.")
#set par(justify: true, first-line-indent: 0.5cm)

// Color scheme - Corporate/Quantum theme
#let primary-color = rgb("#4a90e2")  // Corporate blue
#let secondary-color = rgb("#7b68ee")  // Quantum purple
#let accent-color = rgb("#00d4ff")  // Tech cyan
#let danger-color = rgb("#e74c3c")  // Alert red
#let success-color = rgb("#2ecc71")  // Success green
#let dark-bg = rgb("#1a1a2e")  // Dark background
#let light-text = rgb("#e0e0e0")  // Light text

// Custom functions for D&D stat blocks
#let stat-block(
  name: none,
  type: none,
  ac: none,
  hp: none,
  speed: none,
  str: none,
  dex: none,
  con: none,
  int: none,
  wis: none,
  cha: none,
  skills: (),
  senses: none,
  languages: none,
  challenge: none,
  traits: (),
  actions: (),
  reactions: (),
  legendaries: (),
) = {
  block(
    fill: dark-bg,
    stroke: primary-color,
    radius: 4pt,
    padding: 12pt,
    width: 100%,
    [
      #if name != none [
        #text(size: 14pt, weight: "bold", fill: accent-color)[#name]
        #if type != none [
          #text(size: 10pt, style: "italic", fill: light-text)[#type]
        ]
        #v(6pt)
      ]
      
      #if ac != none or hp != none or speed != none [
        #grid(
          columns: 3,
          column-gutter: 8pt,
          [
            #if ac != none [
              #text(weight: "bold")[AC:] #text(fill: light-text)[#ac]
            ]
            #if hp != none [
              #text(weight: "bold")[HP:] #text(fill: light-text)[#hp]
            ]
            #if speed != none [
              #text(weight: "bold")[Speed:] #text(fill: light-text)[#speed]
            ]
          ]
        )
        #v(6pt)
      ]
      
      #if str != none or dex != none or con != none or int != none or wis != none or cha != none [
        #text(weight: "bold", size: 10pt)[Ability Scores]
        #grid(
          columns: 6,
          column-gutter: 4pt,
          [
            #if str != none [#text(fill: light-text)[STR #str]]
            #if dex != none [#text(fill: light-text)[DEX #dex]]
            #if con != none [#text(fill: light-text)[CON #con]]
            #if int != none [#text(fill: light-text)[INT #int]]
            #if wis != none [#text(fill: light-text)[WIS #wis]]
            #if cha != none [#text(fill: light-text)[CHA #cha]]
          ]
        )
        #v(6pt)
      ]
      
      #if skills.len() > 0 [
        #text(weight: "bold", size: 10pt)[Skills]
        #for skill in skills [
          #text(fill: light-text)[#skill]
        ]
        #v(6pt)
      ]
      
      #if senses != none [
        #text(weight: "bold")[Senses:] #text(fill: light-text)[#senses]
        #v(6pt)
      ]
      
      #if languages != none [
        #text(weight: "bold")[Languages:] #text(fill: light-text)[#languages]
        #v(6pt)
      ]
      
      #if challenge != none [
        #text(weight: "bold")[Challenge:] #text(fill: success-color)[#challenge]
        #v(6pt)
      ]
      
      #if traits.len() > 0 [
        #text(weight: "bold", size: 12pt, fill: accent-color)[Traits]
        #v(4pt)
        #for trait in traits [
          #text(weight: "bold")[#trait.name] #text(fill: light-text)[#trait.description]
          #v(4pt)
        ]
      ]
      
      #if actions.len() > 0 [
        #text(weight: "bold", size: 12pt, fill: accent-color)[Actions]
        #v(4pt)
        #for action in actions [
          #text(weight: "bold")[#action.name] #text(fill: light-text)[#action.description]
          #v(4pt)
        ]
      ]
      
      #if reactions.len() > 0 [
        #text(weight: "bold", size: 12pt, fill: accent-color)[Reactions]
        #v(4pt)
        #for reaction in reactions [
          #text(weight: "bold")[#reaction.name] #text(fill: light-text)[#reaction.description]
          #v(4pt)
        ]
      ]
      
      #if legendaries.len() > 0 [
        #text(weight: "bold", size: 12pt, fill: secondary-color)[Legendary Actions]
        #v(4pt)
        #for legendary in legendaries [
          #text(weight: "bold")[#legendary.name] #text(fill: light-text)[#legendary.description]
          #v(4pt)
        ]
      ]
    ]
  )
}

// Corporate structure display
#let department-box(
  name: none,
  description: none,
  employees: (),
) = {
  block(
    fill: rgb("#2a2a3e"),
    stroke: primary-color,
    radius: 4pt,
    padding: 10pt,
    width: 100%,
    [
      #if name != none [
        #text(size: 12pt, weight: "bold", fill: accent-color)[#name]
        #v(4pt)
      ]
      #if description != none [
        #text(fill: light-text)[#description]
        #v(6pt)
      ]
      #if employees.len() > 0 [
        #text(weight: "bold", size: 10pt)[Employees:]
        #for emp in employees [
          #text(fill: light-text)[• #emp]
        ]
      ]
    ]
  )
}

// Quest/Adventure block
#let quest-block(
  title: none,
  level: none,
  type: none,
  description: none,
  objectives: (),
  rewards: (),
  complications: (),
) = {
  block(
    fill: rgb("#2a2a3e"),
    stroke: secondary-color,
    radius: 4pt,
    padding: 12pt,
    width: 100%,
    [
      #if title != none [
        #text(size: 13pt, weight: "bold", fill: secondary-color)[#title]
        #if level != none or type != none [
          #text(size: 9pt, style: "italic", fill: light-text)[
            #if level != none [Level #level]
            #if level != none and type != none [ • ]
            #if type != none [#type]
          ]
        ]
        #v(6pt)
      ]
      #if description != none [
        #text(fill: light-text)[#description]
        #v(8pt)
      ]
      #if objectives.len() > 0 [
        #text(weight: "bold", size: 11pt, fill: accent-color)[Objectives]
        #v(4pt)
        #for obj in objectives [
          #text(fill: light-text)[• #obj]
        ]
        #v(6pt)
      ]
      #if rewards.len() > 0 [
        #text(weight: "bold", size: 11pt, fill: success-color)[Rewards]
        #v(4pt)
        #for reward in rewards [
          #text(fill: light-text)[• #reward]
        ]
        #v(6pt)
      ]
      #if complications.len() > 0 [
        #text(weight: "bold", size: 11pt, fill: danger-color)[Complications]
        #v(4pt)
        #for comp in complications [
          #text(fill: light-text)[• #comp]
        ]
      ]
    ]
  )
}

// Location block
#let location-block(
  name: none,
  type: none,
  description: none,
  features: (),
  encounters: (),
) = {
  block(
    fill: rgb("#2a2a3e"),
    stroke: accent-color,
    radius: 4pt,
    padding: 10pt,
    width: 100%,
    [
      #if name != none [
        #text(size: 12pt, weight: "bold", fill: accent-color)[#name]
        #if type != none [
          #text(size: 9pt, style: "italic", fill: light-text)[#type]
        ]
        #v(6pt)
      ]
      #if description != none [
        #text(fill: light-text)[#description]
        #v(6pt)
      ]
      #if features.len() > 0 [
        #text(weight: "bold", size: 10pt)[Notable Features]
        #for feature in features [
          #text(fill: light-text)[• #feature]
        ]
        #v(6pt)
      ]
      #if encounters.len() > 0 [
        #text(weight: "bold", size: 10pt)[Possible Encounters]
        #for encounter in encounters [
          #text(fill: light-text)[• #encounter]
        ]
      ]
    ]
  )
}

// Equipment/Item block
#let item-block(
  name: none,
  type: none,
  rarity: none,
  description: none,
  properties: (),
) = {
  block(
    fill: rgb("#2a2a3e"),
    stroke: primary-color,
    radius: 4pt,
    padding: 8pt,
    width: 100%,
    [
      #if name != none [
        #text(size: 11pt, weight: "bold", fill: primary-color)[#name]
        #if type != none or rarity != none [
          #text(size: 9pt, style: "italic", fill: light-text)[
            #if type != none [#type]
            #if type != none and rarity != none [ • ]
            #if rarity != none [#rarity]
          ]
        ]
        #v(4pt)
      ]
      #if description != none [
        #text(fill: light-text)[#description]
        #v(4pt)
      ]
      #if properties.len() > 0 [
        #for prop in properties [
          #text(fill: light-text, size: 9pt)[• #prop]
        ]
      ]
    ]
  )
}

// Main document structure
#let campaign-book(
  title: "Teleport Massive Campaign Setting",
  subtitle: "A D&D 5e Homebrew Campaign",
  author: none,
  version: "1.0",
  sections: (),
) = {
  // Title page
  align(center)[
    #v(3cm)
    #text(size: 32pt, weight: "bold", fill: primary-color)[#title]
    #v(12pt)
    #text(size: 18pt, fill: secondary-color)[#subtitle]
    #v(2cm)
    #if author != none [
      #text(size: 14pt, fill: light-text)[By #author]
      #v(12pt)
    ]
    #text(size: 10pt, fill: light-text)[Version #version]
    #v(12pt)
    #text(size: 10pt, fill: light-text)[Generated: #datetime.today().display()]
  ]
  
  #pagebreak()
  
  // Table of contents
  #heading(level: 1)[Table of Contents]
  #v(12pt)
  #outline(depth: 2)
  
  #pagebreak()
  
  // Main content
  #for section in sections [
    #section
    #v(1cm)
  ]
}

// Export the main function
#let teleport-massive-campaign = campaign-book
