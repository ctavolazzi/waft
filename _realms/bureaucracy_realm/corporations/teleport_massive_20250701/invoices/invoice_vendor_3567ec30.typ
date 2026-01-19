#import "@preview/invoice-maker:1.1.0": *

#show: invoice.with(
  language: "en",
  invoice-id: "vendor_3567ec30",
  issuing-date: "2026-01-19",
  hourly-rate: 100,
  biller: (
    name: "Quantum Equipment Supply Co.",
    vat-id: "US000000000",
    iban: "US0000000000000000000000",
    address: (
      street: "123 Quantum Drive",
      city: "San Francisco",
      postal-code: "CA 94105",
    ),
  ),
  recipient: (
    name: "Teleport Massive Corporation",
    vat-id: "",
    address: (
      street: "123 Quantum Drive",
      city: "San Francisco",
      postal-code: "CA 94105",
      country: "United States",
    ),
  ),
  items: (
    (
      date: "2026-01-19",
      description: "Quantum entanglement measurement equipment",
      quantity: 1,
      unit: "item",
      price: 45000.00,
    ),
  ),
)
