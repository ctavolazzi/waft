#import "@preview/aero-check:0.1.1": *

#show: checklist.with(
  title: "International Travel Packing Checklist",
  disclaimer: "Pack 24 hours before departure. Verify all documents.",
  style: 1,
)

#topic("Essential Documents")[
  #section("Travel Papers")[
    #step("Passport (valid 6+ months)", "Check")
    #step("Visa (if required)", "Check")
    #step("Travel insurance documents", "Check")
    #step("Flight confirmations printed", "Check")
    #step("Hotel reservations printed", "Check")
    #step("Emergency contact information", "Check")
  ]
]

#topic("Electronics")[
  #section("Devices & Chargers")[
    #step("Phone and charger", "Check")
    #step("Laptop and charger (if needed)", "Check")
    #step("Power adapter for destination", "Check")
    #step("Portable battery pack", "Check")
    #step("Headphones/earbuds", "Check")
  ]
]

#colbreak()

#topic("Clothing")[
  #section("Essentials")[
    #step("Underwear (1 per day + 2 extra)", "Check")
    #step("Socks (1 per day + 2 extra)", "Check")
    #step("Shirts/tops (mix of casual & formal)", "Check")
    #step("Pants/shorts (weather appropriate)", "Check")
    #step("Jacket or sweater", "Check")
    #step("Comfortable walking shoes", "Check")
    #step("Sleepwear", "Check")
  ]
]

#topic("Health & Safety")[
  #section("Medical")[
    #step("Prescription medications (original bottles)", "Check")
    #step("First aid kit", "Check")
    #step("Sunscreen and insect repellent", "Check")
    #step("Hand sanitizer", "Check")
    #step("Face masks (if required)", "Check")
  ]
]

#topic("Last Minute")[
  #section("Before Leaving")[
    #step("Notify bank of travel dates", "Check")
    #step("Set up mail hold or forwarding", "Check")
    #step("Arrange pet/house sitter", "Check")
    #step("Lock all doors and windows", "Check")
    #step("Turn off/unplug appliances", "Check")
  ]
]
