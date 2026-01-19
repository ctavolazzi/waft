#import "@preview/invoice-maker:1.1.0": *

#show: invoice.with(
  language: "en",
  invoice-id: "salary_4062d2eb",
  issuing-date: "2026-01-19",
  biller: (
    name: "Teleport Massive Corporation",
    address: (
      street: "123 Quantum Drive",
      city: "San Francisco",
      country: "CA 94105",
      city: "United States",
    ),
  ),
  recipient: (
    name: "Dr. Elena Voss",
    address: (
      street: "456 Research Avenue",
      city: "San Francisco",
      country: "CA 94105",
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
