#import "@preview/invoice-maker:1.1.0": *

#show: invoice.with(
  language: "en",
  invoice-id: "salary_c3314db2",
  issuing-date: "2026-01-19",
  biller: (
    name: "Teleport Massive Corporation",
    vat-id: "US000000000",
    iban: "US0000000000000000000000",
    address: (
      street: "123 Quantum Drive",
      city: "San Francisco",
      postal-code: "CA 94105",
      country: "United States",
    ),
  ),
  recipient: (
    name: "Dr. Elena Voss",
    vat-id: "",
    address: (
      street: "456 Research Avenue",
      city: "San Francisco",
      postal-code: "CA 94105",
    ),
  ),
  items: (
    (
      description: "Monthly salary payment - January 2026",
      quantity: 1,
      unit: "payment",
      price: 8000.00,
    ),
  ),
)
