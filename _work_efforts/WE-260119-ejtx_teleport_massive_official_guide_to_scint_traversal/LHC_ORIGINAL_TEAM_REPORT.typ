#import "@preview/s6t5-page-bordering:1.0.0": s6t5-page-bordering

// Enhanced typography and layout settings
#set text(font: "New Computer Modern", size: 10.5pt)
#set par(justify: true, first-line-indent: 0.4cm, leading: 1.2em)
#set heading(numbering: "1.")
#show heading: set text(size: 1.3em, weight: "bold")
#show heading.where(level: 1): set text(size: 1.8em)
#show heading.where(level: 2): set text(size: 1.4em)
#show heading.where(level: 3): set text(size: 1.2em)

= The Original LHC Team
#text(size: 14pt, style: "italic")[Large Hadron Collider - September 10, 2008 First Beam]

#v(0.5cm)

#align(center)[
  #text(size: 12pt, style: "italic")[
    Research Report: The Scientists, Engineers, and Leaders
    #linebreak()
    Who Achieved the First Circulating Beam
  ]
]

#v(1cm)

== Executive Summary

On September 10, 2008, at 10:28 AM local time, the Large Hadron Collider successfully circulated its first proton beam around the entire 27-kilometer ring. This historic achievement was the result of decades of work by thousands of scientists, engineers, and technicians from around the world.

This report documents the key figures who led and contributed to this momentous achievement, focusing on the leadership, experiment teams, and technical specialists who made the first beam possible.

#v(0.6cm)

#grid(
  columns: 2,
  gutter: 1cm,
  [
    #block(
      fill: rgb("#e3f2fd"),
      stroke: 2pt,
      radius: 4pt,
      inset: 10pt,
      width: 100%,
    )[
      #text(size: 11pt, weight: "bold")[Scale of Achievement]
      #v(8pt)
      #text[• Approximately 10,000 people from 60 countries]
      #text[• Over 1,700 scientists, engineers, students, and technicians from U.S. institutions alone]
      #text[• Decades of planning, design, and construction]
      #text[• First beam achieved on September 10, 2008, 10:28 AM]
    ]
  ],
  [
    #block(
      fill: rgb("#fff3e0"),
      stroke: 2pt,
      radius: 4pt,
      inset: 10pt,
      width: 100%,
    )[
      #text(size: 11pt, weight: "bold")[Technical Specifications]
      #v(8pt)
      #text[• 27-kilometer circumference ring]
      #text[• ~1,700 superconducting magnets]
      #text[• 1.9 Kelvin operating temperature]
      #text[• 7 TeV per beam (design energy)]
      #text[• Largest cryogenic system in the world]
    ]
  ]
)

#v(1cm)

== Team Member Profiles & Professional Information

#grid(
  columns: 2,
  gutter: 1cm,
  [
    #block(
      fill: rgb("#fffde7"),
      stroke: 1.5pt,
      radius: 4pt,
      inset: 10pt,
      width: 100%,
    )[
      #text(size: 11pt, weight: "bold")[Data Sources]
      #v(8pt)
      #text(size: 9pt)[Comprehensive JSON dataset available: `LHC_ORIGINAL_TEAM_LINKEDIN.json`]
      #v(8pt)
      #text(weight: "bold", size: 9.5pt)[LinkedIn Profiles:]
      #text(size: 9pt)[Most senior scientists do not maintain public LinkedIn profiles (common for CERN staff). Alternative sources documented.]
    ],
    [
      #block(
        fill: rgb("#e3f2fd"),
        stroke: 1.5pt,
        radius: 4pt,
        inset: 10pt,
        width: 100%,
      )[
        #text(size: 11pt, weight: "bold")[Photo Availability]
      #v(8pt)
      #text(size: 9pt)[• Lyn Evans: CERN archive (May 2007)]
      #text(size: 9pt)[• Rolf-Dieter Heuer: CERN archive (Jan 2009)]
      #text(size: 9pt)[• Robert Aymar: CERN obituary (may be logo)]
      #text(size: 9pt)[• Others: Photos not found in public sources]
      #text(size: 9pt)[All photo URLs and archive references in JSON dataset]
      ]
    ]
  ]
)

#v(0.8cm)

== CERN Leadership & Project Management

=== Lyn Evans - LHC Project Leader

#grid(
  columns: (1fr, 2fr),
  gutter: 1.2cm,
  [
    #align(center)[
      #image("lhc_team_photos/evans_lyn.jpg", width: 100%)
      #v(8pt)
      #text(size: 9pt, style: "italic")[Lyn Evans]
      #text(size: 8pt, style: "italic")[LHC Project Leader (1994-2008)]
    ]
  ],
  [
    #block(
      fill: rgb("#f5f5f5"),
      stroke: 1pt,
      radius: 4pt,
      inset: 10pt,
      width: 100%,
    )[
      #text(weight: "bold", size: 13pt)[Lyn Evans (Lyndon Rees Evans)]
      #v(6pt)
      #text(size: 9pt, style: "italic")[Welsh (United Kingdom) | Born 1945, Aberdare, Wales]
      #v(10pt)
      #grid(
        columns: 2,
        gutter: 0.8cm,
        [
          #text(weight: "bold", size: 9.5pt)[Role:]
          #text(size: 9.5pt)[LHC Project Leader (1994-2008)]
          #v(6pt)
          #text(weight: "bold", size: 9.5pt)[Education:]
          #text(size: 9.5pt)[First-class physics degree and PhD (1970), Swansea University]
          #v(6pt)
          #text(weight: "bold", size: 9.5pt)[Current Status:]
          #text(size: 9.5pt)[Director of Linear Collider Collaboration (2012-present)]
        ],
        [
          #text(weight: "bold", size: 9.5pt)[Joined CERN:]
          #text(size: 9.5pt)[1970 (research fellow), permanent staff 1971]
          #v(6pt)
          #text(weight: "bold", size: 9.5pt)[Key Achievement:]
          #text(size: 9.5pt)[Led entire LHC project from design through first beam]
        ]
      )
      #v(10pt)
      #text(weight: "bold", size: 10pt)[Career Highlights:]
      #v(6pt)
      #text(size: 9.5pt)[• Worked on SPS accelerator, contributed to W/Z boson discovery (1983)]
      #text(size: 9.5pt)[• Project leader for SPS control system (1985)]
      #text(size: 9.5pt)[• Head of merged SPS & LEP Divisions (1990)]
      #text(size: 9.5pt)[• Associate Director for Future Accelerators (1994)]
      #text(size: 9.5pt)[• Coordinated 10,000+ person international collaboration]
      #v(10pt)
      #text(weight: "bold", size: 10pt)[Awards & Honors:]
      #v(6pt)
      #text(size: 9.5pt)[• CBE (2001) | Fellow: APS (1991), Royal Society (2010), Learned Society of Wales (2011)]
      #text(size: 9.5pt)[• Special Fundamental Physics Prize (2012) | Breakthrough Prize (2013) | Glazebrook Medal]
      #v(8pt)
      #text(size: 8.5pt, style: "italic")["As Project Leader, Evans was responsible for designing, overseeing construction, and commissioning the LHC."]
    ]
  ]
)

=== Robert Aymar - Director-General of CERN

#grid(
  columns: (1fr, 2fr),
  gutter: 1.2cm,
  [
    #align(center)[
      #image("lhc_team_photos/aymar_robert.png", width: 100%)
      #v(8pt)
      #text(size: 9pt, style: "italic")[Robert Aymar]
      #text(size: 8pt, style: "italic")[Director-General (2004-2008)]
      #text(size: 7pt, style: "italic", fill: rgb("#d32f2f"))[Deceased: September 23, 2024]
    ]
  ],
  [
    #block(
      fill: rgb("#f5f5f5"),
      stroke: 1pt,
      radius: 4pt,
      inset: 10pt,
      width: 100%,
    )[
      #text(weight: "bold", size: 13pt)[Robert Aymar]
      #v(6pt)
      #text(size: 9pt, style: "italic")[French | Born 1936 | Deceased September 23, 2024 (age 88)]
      #v(10pt)
      #text(weight: "bold", size: 10pt)[Key Contributions:]
      #v(6pt)
      #text(size: 9.5pt)[• Led Tore Supra tokamak project (1977-1988) - fusion research]
      #text(size: 9.5pt)[• Headed material sciences at French Atomic Energy Commission (CEA)]
      #text(size: 9.5pt)[• Directed ITER engineering design teams (1994-2003) - international fusion project]
      #text(size: 9.5pt)[• Oversaw completion of LHC construction and launch as Director-General]
      #text(size: 9.5pt)[• Delivered official commissioning messages and presided over first beam events]
      #text(size: 9.5pt)[• Managed CERN during critical final construction phase (2004-2008)]
      #v(10pt)
      #text(weight: "bold", size: 10pt)[Career Path:]
      #v(6pt)
      #text(size: 9.5pt)[Fusion Research → CEA Material Sciences → ITER Director → CERN Director-General]
    ]
  ]
)

=== Jos Engelen - Chief Scientific Officer

#block(
  fill: rgb("#f5f5f5"),
  stroke: 1pt,
  radius: 4pt,
  inset: 10pt,
  width: 100%,
)[
  #text(weight: "bold", size: 12pt)[Jos Engelen (Joseph Johannus Engelen)]
  #v(6pt)
  #text(size: 9pt, style: "italic")[Dutch | Born July 6, 1950]
  #v(10pt)
  #grid(
    columns: 2,
    gutter: 1cm,
    [
      #text(weight: "bold", size: 9.5pt)[Role:]
      #text(size: 9.5pt)[Chief Scientific Officer (2004-2008)]
      #v(6pt)
      #text(weight: "bold", size: 9.5pt)[Education:]
      #text(size: 9.5pt)[MSc Physics (1973), PhD (1979), Radboud University Nijmegen]
      #v(6pt)
      #text(weight: "bold", size: 9.5pt)[Current Status:]
      #text(size: 9.5pt)[Professor Emeritus, University of Amsterdam / NIKHEF]
    ],
    [
      #text(weight: "bold", size: 9.5pt)[Career Highlights:]
      #v(6pt)
      #text(size: 9.5pt)[• CERN fellow and staff (1979-1985)]
      #text(size: 9.5pt)[• Professor of Experimental Physics, University of Amsterdam (1987)]
      #text(size: 9.5pt)[• Chairman of Netherlands Organisation for Scientific Research (NWO, 2009-2016)]
      #text(size: 9.5pt)[• Oversaw LHC construction and commissioning as CSO]
    ]
  )
]

=== Rolf-Dieter Heuer - Incoming Director-General

#align(center)[
  #image("lhc_team_photos/heuer_rolf_dieter.jpg", width: 5cm)
  #v(8pt)
  #text(size: 10pt, style: "italic", weight: "bold")[Rolf-Dieter Heuer - Director-General of CERN (2009-2015)]
]

#v(12pt)

#block(
  fill: rgb("#f5f5f5"),
  stroke: 1pt,
  radius: 4pt,
  inset: 12pt,
  width: 100%,
)[
  #text(weight: "bold", size: 12pt)[Rolf-Dieter Heuer]
  #v(8pt)
  #text(weight: "bold")[Role:] Director-General of CERN (2009-2015), appointed December 2007
  #v(6pt)
  #text(weight: "bold")[Born:] 1948, Bad Boll, Germany
  #v(6pt)
  #text(weight: "bold")[Nationality:] German
  #v(6pt)
  #text(weight: "bold")[Education:] Physics (University of Stuttgart), PhD (University of Heidelberg, 1977)
  #v(6pt)
  #text(weight: "bold")[Current Status:] Former Director-General of CERN
  #v(8pt)
  #text(weight: "bold")[Key Contributions:]
  #v(6pt)
  #text[• Worked on JADE collaboration at DESY on PETRA]
  #text[• Joined CERN's OPAL collaboration (LEP) in 1984, spokesperson (1994-1998)]
  #text[• Professor at University of Hamburg]
  #text[• Research Director at DESY (2004)]
  #text[• Appointed Director-General in December 2007, taking office January 1, 2009]
  #text[• In 2008, served as Research Director for Particle and Astroparticle Physics at DESY]
  #text[• Prepared to take over CERN leadership during first beam period]
  #text[• Oversaw LHC operations and Higgs boson discovery in 2012]
  #v(8pt)
  #text(weight: "bold")[Profile Information:]
  #v(6pt)
  #text[• LinkedIn: Not available]
  #text[• Photo: Available in CERN archives (CERN-HI-0901002-07, January 2009), Wikimedia Commons]
  #text[• Alternative sources: Wikipedia, CERN official biography, SIS archives]
]

#v(1cm)

== Technical Leadership

=== Stephen Myers - Accelerators and Beams Department

#grid(
  columns: 2,
  gutter: 1cm,
  [
    #block(
      fill: rgb("#fff3e0"),
      stroke: 1pt,
      radius: 4pt,
      inset: 10pt,
      width: 100%,
    )[
      #text(weight: "bold", size: 12pt)[Stephen Myers (Steve Myers)]
      #v(6pt)
      #text(size: 9pt, style: "italic")[British | Electronic Engineer]
      #v(10pt)
      #text(weight: "bold", size: 9.5pt)[Role:]
      #text(size: 9.5pt)[Head of Accelerators and Beams Department (2003-2008)]
      #v(8pt)
      #text(weight: "bold", size: 9.5pt)[Education:]
      #text(size: 9.5pt)[BSc & PhD Electrical Engineering, Queen's University Belfast (1968, 1972)]
      #v(8pt)
      #text(weight: "bold", size: 9.5pt)[Current Status:]
      #text(size: 9.5pt)[Head of Office of Medical Applications, CERN]
    ],
    [
      #block(
        fill: rgb("#fff3e0"),
        stroke: 1pt,
        radius: 4pt,
        inset: 10pt,
        width: 100%,
      )[
        #text(weight: "bold", size: 10pt)[Career Highlights:]
        #v(6pt)
        #text(size: 9.5pt)[• Helped commission Large Electron-Positron Collider (LEP)]
        #text(size: 9.5pt)[• Led LEP-2 energy upgrade]
        #text(size: 9.5pt)[• Head of AB Department (2003-2008) - responsible for beam performance]
        #text(size: 9.5pt)[• Director of Accelerators and Technology (2009-2014)]
        #text(size: 9.5pt)[• Led post-accident repair of LHC after 2008 incident]
        #text(size: 9.5pt)[• Critical role in achieving first circulating beam]
      ]
    ]
  ]
)

=== Philippe Lebrun - Accelerator Technology

#grid(
  columns: 2,
  gutter: 1cm,
  [
    #block(
      fill: rgb("#fff3e0"),
      stroke: 1pt,
      radius: 4pt,
      inset: 10pt,
      width: 100%,
    )[
      #text(weight: "bold", size: 12pt)[Philippe Lebrun]
      #v(6pt)
      #text(size: 9pt, style: "italic")[French | Cryogenics Expert]
      #v(10pt)
      #text(weight: "bold", size: 9.5pt)[Role:]
      #text(size: 9.5pt)[Head of Accelerator Technology Department (2004)]
      #v(8pt)
      #text(weight: "bold", size: 9.5pt)[Education:]
      #text(size: 9.5pt)[Engineering (École des Mines, Paris), MSc (Caltech)]
      #v(8pt)
      #text(weight: "bold", size: 9.5pt)[Awards:]
      #text(size: 9.5pt)[Honorary doctorate (Wrocław, 2007), Engineer of the Year (2010)]
    ],
    [
      #block(
        fill: rgb("#fff3e0"),
        stroke: 1pt,
        radius: 4pt,
        inset: 10pt,
        width: 100%,
      )[
        #text(weight: "bold", size: 10pt)[Key Contributions:]
        #v(6pt)
        #text(size: 9.5pt)[• Joined CERN in 1974 (ISR Division)]
        #text(size: 9.5pt)[• Worked on ISR, LEP, and LHC projects]
        #text(size: 9.5pt)[• Leader of LHC Division (1999-2001)]
        #text(size: 9.5pt)[• Led design and construction of LHC cryogenics system]
        #text(size: 9.5pt)[• Expert in superconducting magnets (NbTi), cryogenic refrigeration]
        #text(size: 9.5pt)[• Designed world's largest cryogenic system (36,000 tons at 1.9 K)]
      ]
    ]
  ]
)

#v(1cm)

== Magnet System Specialists

=== Giorgio Brianti - Magnet Design

#block(
  fill: rgb("#e8f5e9"),
  stroke: 1pt,
  radius: 4pt,
  inset: 12pt,
  width: 100%,
)[
  #text(weight: "bold", size: 12pt)[Giorgio Brianti]
  #v(6pt)
  #text(size: 10pt, style: "italic")[Note: Correct spelling is "Giorgio" (not "Georgi")]
  #v(8pt)
  #text(weight: "bold")[Role:] "Father" of LHC Magnet Design
  #v(6pt)
  #text(weight: "bold")[Born:] 1930
  #v(6pt)
  #text(weight: "bold")[Status:] Deceased (2023)
  #v(8pt)
  #text(weight: "bold")[Key Contributions:]
  #v(6pt)
  #text[• Joined CERN in 1954]
  #text[• Major contributions to accelerator development]
  #text[• Bending magnet design for Proton Synchrotron]
  #text[• Upgrades to Synchrocyclotron]
  #text[• Design leadership for Booster and Super Proton Synchrotron]
  #text[• CERN Technical Director, Associate Director for Future Accelerators]
  #text[• Helped lay foundations for LHC, especially superconducting magnet technology]
  #text[• Developed the unique twin-aperture (two-in-one) superconducting magnet system]
  #text[• Referenced as "the 'father' of the machine" in 2008 ceremonies]
  #v(8pt)
  #text(weight: "bold")[Profile Information:]
  #v(6pt)
  #text[• LinkedIn: Not available (deceased 2023)]
  #text[• Alternative sources: CERN obituary]
]

=== Lucio Rossi - Magnets & Superconductors

#grid(
  columns: 2,
  gutter: 1cm,
  [
    #block(
      fill: rgb("#e8f5e9"),
      stroke: 1pt,
      radius: 4pt,
      inset: 10pt,
      width: 100%,
    )[
      #text(weight: "bold", size: 12pt)[Lucio Rossi]
      #v(6pt)
      #text(size: 9pt, style: "italic")[Italian | Born September 24, 1955, Podenzano]
      #v(10pt)
      #text(weight: "bold", size: 9.5pt)[Role:]
      #text(size: 9.5pt)[Director, Magnets & Superconductors Group]
      #v(8pt)
      #text(weight: "bold", size: 9.5pt)[Current Status:]
      #text(size: 9.5pt)[Professor of Experimental Physics, University of Milan / INFN]
      #v(8pt)
      #text(weight: "bold", size: 9.5pt)[Awards:]
      #text(size: 9.5pt)[IEEE Council of Superconductivity Award (2007), EPS Rolf Widerøe Prize (2020)]
    ],
    [
      #block(
        fill: rgb("#e8f5e9"),
        stroke: 1pt,
        radius: 4pt,
        inset: 10pt,
        width: 100%,
      )[
        #text(weight: "bold", size: 10pt)[Key Contributions:]
        #v(6pt)
        #text(size: 9.5pt)[• Joined CERN in May 2001]
        #text(size: 9.5pt)[• Led Superconducting Magnets and Cryostats group for LHC]
        #text(size: 9.5pt)[• Developed large Nb-Ti superconducting magnet system (~1,232 dipoles)]
        #text(size: 9.5pt)[• Proposed and coordinated High-Luminosity LHC upgrade (2010-2020)]
        #text(size: 9.5pt)[• Over 200 peer-reviewed papers on superconductivity]
        #text(size: 9.5pt)[• Moved toward Nb₃Sn superconductors for stronger fields (~12 T)]
      ]
    ]
  ]
)

=== Vinod Chohan - Magnet Testing & Commissioning

#block(
  fill: rgb("#e8f5e9"),
  stroke: 1pt,
  radius: 4pt,
  inset: 10pt,
  width: 100%,
)[
  #text(weight: "bold", size: 12pt)[Vinod Chohan (Vinod "Nick" Chohan)]
  #v(6pt)
  #text(size: 9pt, style: "italic", fill: rgb("#d32f2f"))[British (born Tanganyika) | Born May 1, 1949 | Deceased June 12, 2017 (age 68)]
  #v(10pt)
  #grid(
    columns: 2,
    gutter: 1cm,
    [
      #text(weight: "bold", size: 9.5pt)[Role:]
      #text(size: 9.5pt)[Accelerator Engineer, Superconducting Magnets Specialist]
      #v(8pt)
      #text(weight: "bold", size: 9.5pt)[CERN Service:]
      #text(size: 9.5pt)[Nearly 40 years at CERN]
      #v(8pt)
      #text(weight: "bold", size: 9.5pt)[Areas of Expertise:]
      #text(size: 9.5pt)[Beam diagnostics, controls, instrumentation, safety systems]
    ],
    [
      #text(weight: "bold", size: 10pt)[Key Achievement:]
      #v(6pt)
      #text(size: 9.5pt)[• Led team that tested, measured, and trained for over 1,000 superconducting magnets]
      #text(size: 9.5pt)[• Tested approximately 1,300 out of ~1,700 total magnets]
      #text(size: 9.5pt)[• Crucial for magnet reliability and alignment at first beam]
      #text(size: 9.5pt)[• Worked on Antiproton Accumulator (AA)]
    ]
  )
]

=== Amalia Ballarino - Superconductor Systems

#grid(
  columns: 2,
  gutter: 1cm,
  [
    #block(
      fill: rgb("#e8f5e9"),
      stroke: 1pt,
      radius: 4pt,
      inset: 10pt,
      width: 100%,
    )[
      #text(weight: "bold", size: 12pt)[Amalia Ballarino]
      #v(6pt)
      #text(size: 9pt, style: "italic")[Italian | Superconductor Systems Expert]
      #v(10pt)
      #text(weight: "bold", size: 9.5pt)[Role:]
      #text(size: 9.5pt)[Deputy Group Leader, Magnets, Superconductors and Cryostats (MSC)]
      #v(8pt)
      #text(weight: "bold", size: 9.5pt)[Education:]
      #text(size: 9.5pt)[MSc & PhD Nuclear Engineering, Polytechnic University of Turin]
      #v(8pt)
      #text(weight: "bold", size: 9.5pt)[Awards:]
      #text(size: 9.5pt)[Superconductor Industry Person of the Year (2006), IEEE James Wong Award (2021)]
    ],
    [
      #block(
        fill: rgb("#e8f5e9"),
        stroke: 1pt,
        radius: 4pt,
        inset: 10pt,
        width: 100%,
      )[
        #text(weight: "bold", size: 10pt)[Key Contributions:]
        #v(6pt)
        #text(size: 9.5pt)[• Joined CERN around 1995]
        #text(size: 9.5pt)[• Led superconductors development team (2010-2023)]
        #text(size: 9.5pt)[• Developed HTS current leads for LHC (first large-scale HTS application)]
        #text(size: 9.5pt)[• Initiated "cold-powering" system for HL-LHC using MgB₂]
        #text(size: 9.5pt)[• World record: 60m line transmitting 54,000 A (2020)]
        #text(size: 9.5pt)[• Previous record: 20 kA at 24 K in 20m MgB₂ line (2014)]
      ]
    ]
  ]
)

#v(1cm)

== Experiment Collaboration Leadership

#grid(
  columns: 2,
  gutter: 0.8cm,
  [
    #block(
      fill: rgb("#f3e5f5"),
      stroke: 1.5pt,
      radius: 4pt,
      inset: 10pt,
      width: 100%,
    )[
      #text(weight: "bold", size: 12pt)[ATLAS Collaboration]
      #v(8pt)
      #text(weight: "bold", size: 10pt)[Spokesperson (2008):]
      #text(size: 10pt)[Peter Jenni]
      #v(8pt)
      #text(size: 9pt)[• Spokesperson (1995-2009), Co-Spokesperson (1992-1995)]
      #text(size: 9pt)[• Led ATLAS structure, physics reach, detector design]
      #text(size: 9pt)[• Detector ready for first beam passes (September 2008)]
      #text(size: 9pt)[• Current: CERN Guest Scientist, Honorary Professor (Freiburg)]
      #v(6pt)
      #text(size: 8pt, style: "italic")[Note: Fabiola Gianotti became spokesperson in 2009]
    ],
    [
      #block(
        fill: rgb("#f3e5f5"),
        stroke: 1.5pt,
        radius: 4pt,
        inset: 10pt,
        width: 100%,
      )[
        #text(weight: "bold", size: 12pt)[CMS Collaboration]
        #v(8pt)
        #text(weight: "bold", size: 10pt)[Key Leaders:]
        #v(6pt)
        #text(size: 9.5pt)[• *Michel Della Negra* - Founding visionary, Spokesperson (1992-2006)]
        #text(size: 9.5pt)[• *Tejinder (Jim) Virdee* - Spokesperson (2007-2010), founding member]
        #v(8pt)
        #text(size: 9pt)[• Originated CMS concept (early 1990s)]
        #text(size: 9pt)[• Designed hermetic detector with solenoidal magnetic field]
        #text(size: 9pt)[• CMS saw first beam passes (September 2008)]
        #text(size: 9pt)[• Key role in Higgs boson discovery (2012)]
        #v(6pt)
        #text(size: 8pt, style: "italic")[Virdee: Knighted (2014), Fellow of Royal Society (2012), Royal Medal (2024)]
      ]
    ]
  ]
)

#v(0.6cm)

#grid(
  columns: 2,
  gutter: 0.8cm,
  [
    #block(
      fill: rgb("#f3e5f5"),
      stroke: 1.5pt,
      radius: 4pt,
      inset: 10pt,
      width: 100%,
    )[
      #text(weight: "bold", size: 12pt)[LHCb Collaboration]
      #v(8pt)
      #text(weight: "bold", size: 10pt)[Key Leader:]
      #text(size: 10pt)[Themis Bowcock]
      #v(6pt)
      #text(size: 9pt)[• Project Leader for VELO (Vertex Locator) Subdetector]
      #text(size: 9pt)[• Professor of Particle Physics, University of Liverpool]
      #text(size: 9pt)[• Head of Particle Physics group (2011-2019)]
      #v(8pt)
      #text(size: 9pt)[• Led design, construction, commissioning of VELO]
      #text(size: 9pt)[• Critical sub-detector for LHCb]
      #text(size: 9pt)[• First particle tracking (August 2008 synchronization tests)]
    ],
    [
      #block(
        fill: rgb("#f3e5f5"),
        stroke: 1.5pt,
        radius: 4pt,
        inset: 10pt,
        width: 100%,
      )[
        #text(weight: "bold", size: 12pt)[ALICE Collaboration]
        #v(8pt)
        #text(size: 9.5pt)[ALICE's readiness involved alignment, electronics, and calibration work. While numerous scientists contributed, individual names were less frequently featured in early beam announcement sources compared to other experiments.]
        #v(8pt)
        #text(weight: "bold", size: 9.5pt)[Focus:]
        #text(size: 9.5pt)[Heavy ion collisions, quark-gluon plasma studies]
      ]
    ]
  ]
)

#v(1cm)

== Former CERN Leadership Present

#block(
  fill: rgb("#fce4ec"),
  stroke: 1pt,
  radius: 4pt,
  inset: 12pt,
  width: 100%,
)[
  #text(weight: "bold")[Former Director-Generals Present at First Beam:]
  #v(8pt)
  #text[• Herwig Schopper]
  #text[• Carlo Rubbia]
  #text[• Christopher Llewellyn Smith]
  #text[• Luciano Maiani]
  #v(8pt)
  #text[These former leaders were present in the Control Centre to witness the first beam, representing the continuity of CERN's mission and the culmination of decades of work.]
]

#v(1cm)

== The Scale of Collaboration

#grid(
  columns: 2,
  gutter: 1cm,
  [
    #block(
      fill: rgb("#e1f5fe"),
      stroke: 2pt,
      radius: 4pt,
      inset: 12pt,
      width: 100%,
    )[
      #text(size: 12pt, weight: "bold")[International Workforce]
      #v(10pt)
      #text(weight: "bold", size: 10pt)[Total:]
      #text(size: 10pt)[~10,000 people from 60 countries]
      #v(8pt)
      #text(weight: "bold", size: 10pt)[United States:]
      #text(size: 10pt)[Over 1,700 scientists, engineers, students, technicians]
      #v(8pt)
      #text(weight: "bold", size: 10pt)[Scope:]
      #text(size: 10pt)[Accelerator design, construction, detector development, commissioning]
      #v(8pt)
      #text(weight: "bold", size: 10pt)[Institutions:]
      #text(size: 10pt)[Universities, research labs, industrial partners worldwide]
    ],
    [
      #block(
        fill: rgb("#fff9c4"),
        stroke: 2pt,
        radius: 4pt,
        inset: 12pt,
        width: 100%,
      )[
        #text(size: 12pt, weight: "bold")[Project Timeline]
        #v(10pt)
      #text(weight: "bold", size: 10pt)[Planning:]
      #text(size: 10pt)[1984: First discussions | 1994: Project approved]
      #v(8pt)
      #text(weight: "bold", size: 10pt)[Construction:]
      #text(size: 10pt)[1998: Begins | 10 years of building]
      #v(8pt)
      #text(weight: "bold", size: 10pt)[Commissioning:]
      #text(size: 10pt)[Months of testing and calibration]
      #v(8pt)
      #text(weight: "bold", size: 10pt)[First Beam:]
      #text(size: 10pt, fill: rgb("#d32f2f"))[*September 10, 2008, 10:28 AM*]
      ]
    ]
  ]
)

#v(1cm)

== The First Beam Timeline

#block(
  fill: rgb("#fff9c4"),
  stroke: 1.5pt,
  radius: 4pt,
  inset: 10pt,
  width: 100%,
)[
  #table(
    columns: 2,
    stroke: 0.5pt,
    align: left,
    inset: 6pt,
    [*Date*], [*Event*],
    [*September 10, 2008*], [*First Beam Day*],
    [9:30 AM], [Beam injection into LHC begins],
    [10:28 AM], [*First full circuit completed* - Beam successfully circulated entire 27-kilometer ring],
    [*September 19, 2008*], [*Incident*],
    [], [Magnet quench in sector 3-4 - Required repairs and improvements],
    [*November 2009*], [*Operations Resume*],
    [], [Full operations resumed, collisions began],
    [*2010*], [First high-energy collisions at 7 TeV],
    [*2012*], [Higgs boson discovery announced],
  )
]

#v(1cm)

== Technical Achievements

#grid(
  columns: 2,
  gutter: 1cm,
  [
    #block(
      fill: rgb("#e8f5e9"),
      stroke: 1.5pt,
      radius: 4pt,
      inset: 10pt,
      width: 100%,
    )[
      #text(weight: "bold", size: 11pt)[Superconducting Magnet System]
      #v(8pt)
      #text(weight: "bold", size: 9.5pt)[Total Magnets:] #text(size: 9.5pt)[~1,700]
      #v(6pt)
      #text(size: 9.5pt)[• 1,232 dipole magnets (bend beam in 27km ring)]
      #text(size: 9.5pt)[• 392 quadrupole magnets (focus beam)]
      #text(size: 9.5pt)[• Additional corrector magnets]
      #v(8pt)
      #text(weight: "bold", size: 9.5pt)[Operating Temperature:]
      #text(size: 9.5pt)[1.9 Kelvin (-271.3°C) - colder than outer space]
      #v(6pt)
      #text(size: 9.5pt)[Cooling: Liquid helium systems]
      #text(size: 9.5pt)[Field Strength: 8.3 Tesla (dipoles)]
    ],
    [
      #block(
        fill: rgb("#e1f5fe"),
        stroke: 1.5pt,
        radius: 4pt,
        inset: 10pt,
        width: 100%,
      )[
        #text(weight: "bold", size: 11pt)[Cryogenics System]
        #v(8pt)
        #text(weight: "bold", size: 9.5pt)[World's Largest:]
        #v(6pt)
        #text(size: 9.5pt)[• Cools 36,000 tons of material to 1.9 K]
        #text(size: 9.5pt)[• Uses 120 tons of liquid helium]
        #text(size: 9.5pt)[• Maintains superconducting state]
        #v(8pt)
        #text(weight: "bold", size: 9.5pt)[Led by:]
        #text(size: 9.5pt)[Philippe Lebrun (Head of Accelerator Technology)]
        #v(6pt)
        #text(size: 9.5pt)[Superfluid helium-based system]
      ]
    ]
  ]
)

#v(0.8cm)

#block(
  fill: rgb("#fff3e0"),
  stroke: 1.5pt,
  radius: 4pt,
  inset: 10pt,
  width: 100%,
)[
  #text(weight: "bold", size: 11pt)[Beam Injection System - Accelerator Chain]
  #v(8pt)
  #grid(
    columns: 5,
    gutter: 0.6cm,
    column-gutter: 0.4cm,
    [
      #align(center)[
        #text(weight: "bold", size: 9pt)[Linac 2]
        #v(4pt)
        #text(size: 8pt)[Linear]
        #text(size: 8pt)[Accelerator]
      ]
    ],
    [
      #align(center)[
        #text(weight: "bold", size: 9pt)[PS Booster]
        #v(4pt)
        #text(size: 8pt)[Proton]
        #text(size: 8pt)[Synchrotron]
        #text(size: 8pt)[Booster]
      ]
    ],
    [
      #align(center)[
        #text(weight: "bold", size: 9pt)[PS]
        #v(4pt)
        #text(size: 8pt)[Proton]
        #text(size: 8pt)[Synchrotron]
      ]
    ],
    [
      #align(center)[
        #text(weight: "bold", size: 9pt)[SPS]
        #v(4pt)
        #text(size: 8pt)[Super Proton]
        #text(size: 8pt)[Synchrotron]
      ]
    ],
    [
      #align(center)[
        #text(weight: "bold", size: 9pt)[LHC]
        #v(4pt)
        #text(size: 8pt)[Large Hadron]
        #text(size: 8pt)[Collider]
        #text(size: 8pt)[27 km ring]
      ]
    ]
  )
  #v(8pt)
  #text(size: 8.5pt, style: "italic")[Each stage accelerates particles to higher energies before injection into the next]
]

#v(1cm)

== Legacy and Impact

#grid(
  columns: 3,
  gutter: 0.8cm,
  [
    #block(
      fill: rgb("#e3f2fd"),
      stroke: 1.5pt,
      radius: 4pt,
      inset: 10pt,
      width: 100%,
    )[
      #text(weight: "bold", size: 11pt)[Scientific Discoveries]
      #v(8pt)
      #text(size: 9.5pt)[• *Higgs boson* (2012) - confirmed Higgs field existence]
      #text(size: 9.5pt)[• Precision Standard Model measurements]
      #text(size: 9.5pt)[• Searches for new physics]
      #text(size: 9.5pt)[• Quark-gluon plasma studies]
      #text(size: 9.5pt)[• Rare particle decays]
    ],
    [
      #block(
        fill: rgb("#fff3e0"),
        stroke: 1.5pt,
        radius: 4pt,
        inset: 10pt,
        width: 100%,
      )[
        #text(weight: "bold", size: 11pt)[Technological Innovations]
        #v(8pt)
      #text(size: 9.5pt)[• Superconducting magnets]
      #text(size: 9.5pt)[• Cryogenics systems]
      #text(size: 9.5pt)[• Detector technologies]
      #text(size: 9.5pt)[• Worldwide LHC Computing Grid]
      #text(size: 9.5pt)[• Medical imaging (PET, hadron therapy)]
      #text(size: 9.5pt)[• Data processing methods]
      ]
    ],
    [
      #block(
        fill: rgb("#e8f5e9"),
        stroke: 1.5pt,
        radius: 4pt,
        inset: 10pt,
        width: 100%,
      )[
        #text(weight: "bold", size: 11pt)[Collaboration Model]
        #v(8pt)
      #text(size: 9.5pt)[• Model for mega-science projects]
      #text(size: 9.5pt)[• Global cooperation demonstration]
      #text(size: 9.5pt)[• Training ground for scientists]
      #text(size: 9.5pt)[• Cultural exchange]
      #text(size: 9.5pt)[• Knowledge sharing networks]
      #text(size: 9.5pt)[• International standards]
      ]
    ]
  ]
)

#v(1cm)

== Conclusion

#block(
  fill: rgb("#f5f5f5"),
  stroke: 2pt,
  radius: 4pt,
  inset: 14pt,
  width: 100%,
)[
  #text(size: 11pt)[The first beam on September 10, 2008, was the culmination of decades of work by thousands of dedicated scientists, engineers, and technicians from around the world. While this report highlights key leadership figures, it represents only a fraction of the massive collaborative effort.]
  #v(12pt)
  #text(weight: "bold", size: 10.5pt)[The achievement required:]
  #v(8pt)
  #grid(
    columns: 2,
    gutter: 1cm,
    [
      #text(size: 9.5pt)[• *Visionary leadership* - Lyn Evans (14-year project leadership), Robert Aymar (CERN Director-General), Rolf-Dieter Heuer (incoming leadership)]
      #text(size: 9.5pt)[• *Technical expertise* - Magnet specialists (Giorgio Brianti, Lucio Rossi, Vinod Chohan, Amalia Ballarino), cryogenics engineers (Philippe Lebrun), accelerator physicists (Stephen Myers)]
    ],
    [
      #text(size: 9.5pt)[• *Experiment collaboration* - ATLAS (Peter Jenni), CMS (Michel Della Negra, Tejinder Virdee), LHCb (Themis Bowcock), ALICE teams]
      #text(size: 9.5pt)[• *International cooperation* - 10,000 people from 60 countries, decades of planning, years of construction]
    ]
  )
  #v(14pt)
  #align(center)[
    #text(size: 11pt, weight: "bold", fill: rgb("#1976d2"))[
      This moment—10:28 AM on September 10, 2008—marked not just a scientific achievement,
      #linebreak()
      but a testament to what humanity can accomplish through collaboration, dedication,
      #linebreak()
      and the pursuit of understanding the fundamental nature of reality.
    ]
  ]
]

#v(2cm)

#align(center)[
  #text(size: 10pt, style: "italic")[
    Report compiled: #datetime.today().display()
    #linebreak()
    #linebreak()
    Sources: CERN archives, scientific publications, and historical records
    #linebreak()
    #linebreak()
    "The LHC is not just a machine. It is a symbol of what we can achieve when we work together."
  ]
]

#pagebreak()

== Appendix: Key Dates and Milestones

#grid(
  columns: 3,
  gutter: 0.8cm,
  [
    #block(
      fill: rgb("#f5f5f5"),
      stroke: 1pt,
      radius: 4pt,
      inset: 10pt,
      width: 100%,
    )[
      #text(weight: "bold", size: 10.5pt)[Pre-2008 Timeline]
      #v(8pt)
      #text(size: 9pt)[• 1984: First discussions]
      #text(size: 9pt)[• 1994: Project approved]
      #text(size: 9pt)[• 1994-2008: Lyn Evans Project Leader]
      #text(size: 9pt)[• 1998: Construction begins]
      #text(size: 9pt)[• 2004-2008: Robert Aymar Director-General]
      #text(size: 9pt)[• 2007: Rolf-Dieter Heuer appointed]
    ],
    [
      #block(
        fill: rgb("#fff9c4"),
        stroke: 1.5pt,
        radius: 4pt,
        inset: 10pt,
        width: 100%,
      )[
        #text(weight: "bold", size: 10.5pt)[2008 Timeline]
        #v(8pt)
        #text(size: 9pt)[• Aug: Synchronization tests]
        #text(size: 9pt, fill: rgb("#d32f2f"))[• Sep 10, 9:30 AM: Beam injection]
        #text(size: 9pt, fill: rgb("#d32f2f"), weight: "bold")[• Sep 10, 10:28 AM: *First circuit*]
        #text(size: 9pt)[• Sep 19: Magnet quench incident]
        #text(size: 9pt)[• Dec: Repairs begin]
      ]
    ],
    [
      #block(
        fill: rgb("#e8f5e9"),
        stroke: 1pt,
        radius: 4pt,
        inset: 10pt,
        width: 100%,
      )[
        #text(weight: "bold", size: 10.5pt)[Post-2008 Timeline]
        #v(8pt)
        #text(size: 9pt)[• 2009: Rolf-Dieter Heuer becomes DG]
        #text(size: 9pt)[• Nov 2009: Operations resume]
        #text(size: 9pt)[• 2010: High-energy collisions]
        #text(size: 9pt, weight: "bold")[• 2012: Higgs boson discovery]
        #text(size: 9pt)[• 2013-2015: Run 1]
        #text(size: 9pt)[• 2015-2018: Run 2]
        #text(size: 9pt)[• 2018-2022: Upgrades]
        #text(size: 9pt)[• 2022: Run 3 begins]
      ]
    ]
  ]
)

== References

#text[• CERN Archives and Historical Records]
#text[• CERN Courier: "The LHC sees its first circulating beam"]
#text[• CERN Press Releases (September 2008)]
#text[• Wikipedia: Lyn Evans, Rolf-Dieter Heuer, Vinod Chohan, Lucio Rossi, Robert Aymar, Jos Engelen, Stephen Myers, Philippe Lebrun, Giorgio Brianti, Amalia Ballarino, Peter Jenni, Michel Della Negra, Tejinder Virdee, Themis Bowcock]
#text[• CERN Official Biographies]
#text[• U.S. Department of Energy Science Headlines (September 2008)]
#text[• Fermilab News: "U.S. scientists count down to LHC startup"]
#text[• LHC_ORIGINAL_TEAM_LINKEDIN.json - Comprehensive profile dataset with detailed information, photo sources, and alternative professional references]
