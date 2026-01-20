#import "@preview/invoice-maker:1.1.0": *

#show: invoice.with(
  language: "en",
  invoice-id: "txn_e0a7c1b3_20250731",
  issuing-date: "2026-01-19",
  hourly-rate: 100,
  biller: (
    name: "Teleport Massive",
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
    name: "Dr. Marcus Chen",
    vat-id: "US000000001",
    address: (
      city: "Unknown",
      postal-code: "00000",
      country: "USA",
    ),
  ),
  items: (
    (
      date: "2026-01-19",
      description: "Payroll payment for being_20260119_025316_f8e06283",
      quantity: 1,
      unit: "payment",
      price: 15000.00,
    ),
  ),
)
