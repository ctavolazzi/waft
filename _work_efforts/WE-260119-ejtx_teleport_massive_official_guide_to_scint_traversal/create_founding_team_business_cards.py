#!/usr/bin/env python3
"""
Create Business Cards for Teleport Massive Founding Team

Generates individual business card PDFs for each founding team member
using the minimalbc Typst package.
"""

import json
from pathlib import Path

work_effort_dir = Path(__file__).parent
json_path = work_effort_dir / "TELEPORT_MASSIVE_FOUNDING_TEAM_2026.json"
business_cards_dir = work_effort_dir / "founding_team_business_cards"
business_cards_dir.mkdir(exist_ok=True)

# Load team data
with open(json_path) as f:
    data = json.load(f)

# Generate business card Typst file for each team member
for member in data["team_members"]:
    name = member["name"]
    full_name = f"{name['first']} {name['last']}"
    role = member["role"]
    email = member["background"]["email"]

    # Generate phone number (format: +1 (415) 555-XXXX)
    # Use member ID to create unique but consistent numbers
    member_num = int(member["id"].split("-")[-1])
    phone_last = 1000 + member_num
    phone = f"+1 (415) 555-{phone_last:04d}"

    # Create filename
    filename = f"business_card_{name['last'].lower()}_{name['first'].lower()}.typ"
    filepath = business_cards_dir / filename

    # Generate Typst content
    typst_content = f'''#import "@preview/minimalbc:0.0.1": minimalbc

#show: minimalbc.with(
    geo_size: "us",
    flip: false,
    company_name: "Teleport Massive Inc.",
    name: "{full_name}",
    role: "{role}",
    telephone_number: "{phone}",
    email_address: "{email}",
    website: "teleportmassive.com",
    bg_color: "1a237e", // Dark blue brand color
)
'''

    # Write file
    with open(filepath, "w") as f:
        f.write(typst_content)

    print(f"✅ Created: {filename}")

print(f"\n✅ Generated {len(data['team_members'])} business card Typst files")
print(f"   Location: {business_cards_dir}")
