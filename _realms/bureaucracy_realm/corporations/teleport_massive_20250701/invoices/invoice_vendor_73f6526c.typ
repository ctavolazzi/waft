#import "@preview/invoice-maker:1.1.0": *

#show: invoice.with(
  language: "en",
  invoice-id: "vendor_73f6526c",
  issuing-date: "2026-01-19",
  biller: (
    name: "Quantum Equipment Supply Co.",
    address: (
      street: "123 Quantum Drive",
      city: "San Francisco",
      postal-code: "CA 94105",
    ),
  ),
  recipient: (
    name: "Teleport Massive Corporation",
    address: (
      street: "123 Quantum Drive",
      city: "San Francisco",
      postal-code: "CA 94105",
      country: "United States",
    ),
  ),
  items: (
    (
      description: "Quantum entanglement measurement equipment",
      quantity: 1,
      unit: "item",
      price: 45000.00,
    ),
  ),
)
