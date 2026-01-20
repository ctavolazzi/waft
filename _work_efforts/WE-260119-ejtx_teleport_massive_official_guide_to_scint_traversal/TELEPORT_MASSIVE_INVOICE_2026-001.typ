#import "@preview/invoice-pro:0.1.1": *

// Set language to English for date/number formatting
#set text(lang: "en")

#show: invoice.with(
  format: "DIN-5008-A",

  sender: (
    name: "Quantum Research Labs, LLC",
    address: "2500 Sand Hill Road",
    city: "Menlo Park, CA 94025",
    extra: (
      "Tel": [+1 (650) 555-0123],
      "Email": [#raw("research@quantumlabs.com")],
      "Web": [#link("https://www.quantumlabs.com")[www.quantumlabs.com]],
    )
  ),

  recipient: (
    name: "Justin Ross",
    address: "Teleport Massive (Pre-Incorporation)",
    city: "San Francisco, CA 94102"
  ),

  invoice-nr: "QR-2026-001",
  date: datetime(year: 2026, month: 1, day: 10),
  tax-nr: "94-1234567",
  vat: 0.0, // No VAT for US-based transactions
  vat-exempt-small-biz: false,
)

// Invoice Items - Initial Research Consultation
#invoice-line-items(
  currency: [#raw("$")],
  item([Quantum Teleportation Research Analysis], quantity: 40, unit: [hrs], price: 250.00),
  item([Literature Review: 7 Peer-Reviewed Papers], quantity: 1, unit: [project], price: 1500.00),
  item([Scaling Feasibility Assessment], quantity: 1, unit: [report], price: 2000.00),
  item([Technical Architecture Consultation], quantity: 8, unit: [hrs], price: 300.00),
)

// Payment Terms - 30 days net
#payment-goal(days: 30, currency: [#raw("$")])

// Bank Details
#bank-details(
  bank: "Silicon Valley Bank",
  iban: "DE89370400440532013000", // Using valid IBAN format for template compatibility
  bic: "COBADEFFXXX",
  reference: "Invoice QR-2026-001 / Research Services",
  account-holder-text: "Quantum Research Labs, LLC",
  qr-code: (display: true, size: 3.5cm)
)

#signature(signature: block[
  #align(center)[
    #text(weight: "bold")[Dr. Sarah Chen]
    #linebreak()
    #text(style: "italic")[Principal Research Scientist]
    #linebreak()
    #text(style: "italic")[Quantum Research Labs, LLC]
  ]
])

#v(1cm)

#block(
  fill: rgb("#f5f5f5"),
  stroke: (thickness: 1pt, paint: rgb("#757575")),
  radius: 4pt,
  inset: 10pt,
  width: 100%,
)[
  #text(size: 9pt, style: "italic")[
    #text(weight: "bold")[Notes:]
    #linebreak()
    This invoice covers initial research consultation services provided to Mr. Justin Ross in preparation for the founding of Teleport Massive Inc. Services included comprehensive analysis of quantum teleportation research papers, feasibility assessment for scaling quantum entanglement systems, and technical architecture consultation for proposed quantum teleportation infrastructure.
    #linebreak()
    #linebreak()
    All research findings and recommendations have been documented in the accompanying research foundation booklet. Payment terms: Net 30 days.
  ]
]
