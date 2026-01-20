#import "@preview/invoice-pro:0.1.1": *

// Set language to English
#set text(lang: "en")

#show: invoice.with(
  format: "DIN-5008-A",

  sender: (
    name: "Bay Area Legal Services, P.C.",
    address: "One Market Plaza, Suite 2000",
    city: "San Francisco, CA 94105",
    extra: (
      "Tel": [+1 (415) 555-0456],
      "Email": [#raw("corporate@baylegal.com")],
      "Web": [#link("https://www.baylegal.com")[www.baylegal.com]],
    )
  ),

  recipient: (
    name: "Justin Ross",
    address: "Teleport Massive (Pre-Incorporation)",
    city: "San Francisco, CA 94102"
  ),

  invoice-nr: "BALS-2026-042",
  date: datetime(year: 2026, month: 1, day: 12),
  tax-nr: "94-9876543",
  vat: 0.0,
  vat-exempt-small-biz: false,
)

// Invoice Items - Corporate Formation Services
#invoice-line-items(
  currency: [#raw("$")],
  item([Corporate Formation Consultation], quantity: 3, unit: [hrs], price: 450.00),
  item([Delaware C-Corp Formation], quantity: 1, unit: [filing], price: 2500.00),
  item([California Foreign Qualification], quantity: 1, unit: [filing], price: 800.00),
  item([Operating Agreement Drafting], quantity: 1, unit: [document], price: 3500.00),
  item([IP Assignment Agreements], quantity: 9, unit: [agreement], price: 250.00),
  item([Regulatory Compliance Review], quantity: 2, unit: [hrs], price: 450.00),
)

// Payment Terms
#payment-goal(days: 14, currency: [#raw("$")])

// Bank Details
#bank-details(
  bank: "Wells Fargo Bank",
  iban: "DE89370400440532013000", // Using valid IBAN format for template compatibility
  bic: "COBADEFFXXX",
  reference: "Invoice BALS-2026-042 / Corporate Formation",
  account-holder-text: "Bay Area Legal Services, P.C.",
  qr-code: (display: true, size: 3.5cm)
)

#signature(signature: block[
  #align(center)[
    #text(weight: "bold")[Soham Murray, Esq.]
    #linebreak()
    #text(style: "italic")[Partner, Corporate Law]
    #linebreak()
    #text(style: "italic")[Bay Area Legal Services, P.C.]
  ]
])

#v(1cm)

#block(
  fill: rgb("#e3f2fd"),
  stroke: (thickness: 1pt, paint: rgb("#1976d2")),
  radius: 4pt,
  inset: 10pt,
  width: 100%,
)[
  #text(size: 9pt)[
    #text(weight: "bold")[Corporate Formation Services:]
    #linebreak()
    This invoice covers legal services for the formation of Teleport Massive Inc. as a Delaware C-Corporation with California foreign qualification. Services include entity formation, operating agreement drafting, IP assignment agreements for all 9 founding team members, and initial regulatory compliance review for quantum technology research operations.
    #linebreak()
    #linebreak()
    #text(style: "italic")[Note: Soham Murray will join Teleport Massive as Head of Legal & Compliance upon incorporation on January 18, 2026.]
  ]
]
