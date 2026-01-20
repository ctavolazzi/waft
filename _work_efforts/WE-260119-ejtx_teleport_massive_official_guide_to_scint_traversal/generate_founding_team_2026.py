#!/usr/bin/env python3
"""
Generate Teleport Massive Founding Team (2026)

Creates the founding team that forms Teleport Massive as a corporation
in San Francisco on January 18, 2026.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import requests

# Founding team roles for a tech corporation
FOUNDING_ROLES = [
    {
        "role": "Chief Executive Officer & Co-Founder",
        "specialization": "Strategic vision and corporate leadership",
        "contribution": "Founded Teleport Massive with vision of reality traversal technology",
    },
    {
        "role": "Chief Technology Officer & Co-Founder",
        "specialization": "Quantum computing and reality physics",
        "contribution": "Led technical architecture and quantum system design",
    },
    {
        "role": "Chief Financial Officer",
        "specialization": "Corporate finance and venture capital",
        "contribution": "Secured initial funding and established financial infrastructure",
    },
    {
        "role": "Chief Operating Officer",
        "specialization": "Operations and business development",
        "contribution": "Established operational systems and early partnerships",
    },
    {
        "role": "Head of Research & Development",
        "specialization": "Experimental physics and reality mechanics",
        "contribution": "Led early research into reality fracture detection",
    },
    {
        "role": "Lead Quantum Engineer",
        "specialization": "Quantum systems engineering and hardware",
        "contribution": "Designed and built early quantum detection systems",
    },
    {
        "role": "Head of Legal & Compliance",
        "specialization": "Corporate law and regulatory compliance",
        "contribution": "Established legal framework and regulatory compliance",
    },
    {
        "role": "Head of Marketing & Business Development",
        "specialization": "Brand development and strategic partnerships",
        "contribution": "Developed brand identity and early market positioning",
    },
]


def fetch_random_users(count: int = 8, seed: str = "teleport_massive_2026") -> list[dict[str, Any]]:
    """Fetch random users from Random User API."""
    url = f"https://randomuser.me/api/?results={count}&seed={seed}&nat=us,gb,ca,au"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()["results"]


def generate_founding_team() -> dict[str, Any]:
    """Generate the founding team data structure."""
    users = fetch_random_users(count=8, seed="teleport_massive_2026")

    team_members = []
    for i, (user, role_info) in enumerate(zip(users, FOUNDING_ROLES, strict=False), 1):
        # Calculate age at founding (January 18, 2026)
        birth_year = int(user["dob"]["date"][:4])
        age_at_founding = 2026 - birth_year

        # Use San Francisco location for all founders
        location = "San Francisco, California, United States"

        member = {
            "id": f"TM-FT-2026-{i:03d}",
            "name": {
                "title": user["name"]["title"],
                "first": user["name"]["first"],
                "last": user["name"]["last"],
                "full": f"{user['name']['title']} {user['name']['first']} {user['name']['last']}",
            },
            "role": role_info["role"],
            "specialization": role_info["specialization"],
            "contribution": role_info["contribution"],
            "background": {
                "nationality": user["nat"],
                "location": location,
                "age_at_founding": age_at_founding,
                "email": f"{user['name']['first'].lower()}.{user['name']['last'].lower()}@teleportmassive.com",
            },
            "picture": {
                "large": user["picture"]["large"],
                "medium": user["picture"]["medium"],
                "thumbnail": user["picture"]["thumbnail"],
            },
        }
        team_members.append(member)

    return {
        "team_name": "Teleport Massive Founding Team",
        "founding_date": "2026-01-18",
        "founding_location": "San Francisco, California, United States",
        "founding_event": "Corporation Formation - Teleport Massive Inc.",
        "data_collection_date": datetime.now().strftime("%Y-%m-%d"),
        "team_members": team_members,
        "founding_timeline": {
            "2026-01-18": "Teleport Massive Inc. incorporated in San Francisco",
            "2026-01-18": "Initial team of 8 founders assembled",
            "2026-01-18": "Corporate headquarters established in San Francisco",
            "2026-02-01": "First research facility opened",
            "2026-03-15": "Initial funding round completed",
        },
        "corporate_structure": {
            "legal_name": "Teleport Massive Inc.",
            "incorporation_date": "2026-01-18",
            "jurisdiction": "California, United States",
            "headquarters": "San Francisco, California",
            "initial_focus": "Reality traversal technology, quantum systems, reality fracture detection",
        },
        "notes": "Team generated using Random User API (https://randomuser.me/) with seed 'teleport_massive_2026' for consistency. This is the founding team that established Teleport Massive as a corporation on January 18, 2026, in San Francisco.",
    }


def download_photos(team_data: dict[str, Any]) -> None:
    """Download photos for all team members."""
    photos_dir = Path(__file__).parent / "founding_team_photos_2026"
    photos_dir.mkdir(parents=True, exist_ok=True)

    print("\nDownloading team member photos...")
    for member in team_data["team_members"]:
        last_name = member["name"]["last"].lower()
        first_name = member["name"]["first"].lower()
        photo_url = member["picture"]["large"]
        output_path = photos_dir / f"{last_name}_{first_name}.jpg"

        if output_path.exists():
            print(f"  ⏭️  Already exists: {output_path.name}")
            member["picture"]["local_path"] = f"founding_team_photos_2026/{output_path.name}"
            continue

        try:
            response = requests.get(photo_url, timeout=30, stream=True)
            response.raise_for_status()

            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            member["picture"]["local_path"] = f"founding_team_photos_2026/{output_path.name}"
            print(f"  ✅ Downloaded: {output_path.name}")
        except Exception as e:
            print(f"  ❌ Failed to download {photo_url}: {e}")
            member["picture"]["local_path"] = None


def main():
    """Generate and save the founding team data."""
    output_file = Path(__file__).parent / "TELEPORT_MASSIVE_FOUNDING_TEAM_2026.json"

    print("Generating Teleport Massive Founding Team (2026)...")
    print("Founding Date: January 18, 2026")
    print("Location: San Francisco, California\n")

    team_data = generate_founding_team()

    # Download photos
    download_photos(team_data)

    # Save to JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(team_data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Generated founding team with {len(team_data['team_members'])} members")
    print(f"✅ Saved to: {output_file}")
    print("\nFounding Team Members:")
    for member in team_data["team_members"]:
        print(f"  • {member['name']['full']} - {member['role']}")

    return output_file


if __name__ == "__main__":
    main()
