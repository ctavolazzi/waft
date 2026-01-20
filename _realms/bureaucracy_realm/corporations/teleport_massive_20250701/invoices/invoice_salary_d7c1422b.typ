#import "@preview/invoice-maker:1.1.0": *

#show: invoice.with(
  language: "en",
  invoice_id: "salary_d7c1422b",
  issue_date: datetime(year: 2026, month: 1, day: 19),
  sender: (
    name: "Teleport Massive Corporation",
    address: "123 Quantum Drive\nSan Francisco, CA 94105\nUnited States",
  ),
  recipient: (
    name: "Dr. Elena Voss",
    address: "456 Research Avenue\nSan Francisco, CA 94105",
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
