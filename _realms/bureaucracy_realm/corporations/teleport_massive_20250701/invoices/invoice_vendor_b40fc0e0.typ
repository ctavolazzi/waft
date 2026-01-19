#import "@preview/invoice-maker:1.1.0": *

#show: invoice.with(
  language: "en",
  invoice_id: "vendor_b40fc0e0",
  issue_date: datetime(year: 2026, month: 1, day: 19),
  sender: (
    name: "Quantum Equipment Supply Co.",
    address: "123 Quantum Drive\nSan Francisco, CA 94105",
  ),
  recipient: (
    name: "Teleport Massive Corporation",
    address: "123 Quantum Drive\nSan Francisco, CA 94105\nUnited States",
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
