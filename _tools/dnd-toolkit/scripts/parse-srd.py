#!/usr/bin/env python3
"""
SRD Parser - Converts D&D 5e SRD markdown files to JSON for the toolkit.
Parses monsters, spells, and items from the dnd5e-srd repository.
"""

import json
import os
import re
import yaml
from pathlib import Path

# Paths
SRD_PATH = Path(__file__).parent.parent.parent.parent / "_external" / "dnd5e-srd" / "compendium"
OUTPUT_PATH = Path(__file__).parent.parent / "data"


def parse_frontmatter(content):
    """Extract YAML frontmatter from markdown file."""
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    try:
        frontmatter = yaml.safe_load(parts[1])
        body = parts[2].strip()
        return frontmatter or {}, body
    except yaml.YAMLError:
        return {}, content


def extract_tags(frontmatter):
    """Extract useful info from frontmatter tags."""
    tags = frontmatter.get("tags", [])
    result = {
        "source": None,
        "type": None,
        "subtype": None,
        "size": None,
        "environment": [],
        "level": None,
        "school": None,
        "classes": [],
        "rarity": None,
        "tier": None,
        "item_type": None,
    }

    for tag in tags:
        if tag.startswith("compendium/src/"):
            result["source"] = tag.split("/")[-1]
        elif tag.startswith("monster/type/"):
            parts = tag.replace("monster/type/", "").split("/")
            result["type"] = parts[0]
            if len(parts) > 1:
                result["subtype"] = parts[1]
        elif tag.startswith("monster/size/"):
            result["size"] = tag.replace("monster/size/", "")
        elif tag.startswith("monster/environment/"):
            result["environment"].append(tag.replace("monster/environment/", ""))
        elif tag.startswith("spell/level/"):
            level = tag.replace("spell/level/", "")
            result["level"] = int(level) if level.isdigit() else level
        elif tag.startswith("spell/school/"):
            result["school"] = tag.replace("spell/school/", "")
        elif tag.startswith("spell/class/"):
            result["classes"].append(tag.replace("spell/class/", ""))
        elif tag.startswith("item/rarity/"):
            result["rarity"] = tag.replace("item/rarity/", "")
        elif tag.startswith("item/tier/"):
            result["tier"] = tag.replace("item/tier/", "")
        elif tag.startswith("item/") and not tag.startswith("item/property/"):
            # Extract item type like item/weapon/martial/melee
            item_parts = tag.replace("item/", "").split("/")
            if item_parts[0] not in ["rarity", "tier", "property"]:
                result["item_type"] = "/".join(item_parts)

    return result


def parse_statblock(body):
    """Parse ad-statblock content for monsters."""
    statblock = {}

    # Find the statblock
    match = re.search(r'```ad-statblock(.*?)```', body, re.DOTALL)
    if not match:
        return statblock

    block = match.group(1)

    # Extract basic info
    title_match = re.search(r'title:\s*"?([^"\n]+)"?', block)
    if title_match:
        statblock["name"] = title_match.group(1).strip()

    # AC
    ac_match = re.search(r'\*\*Armor Class\*\*\s*(\d+)', block)
    if ac_match:
        statblock["ac"] = int(ac_match.group(1))

    # HP
    hp_match = re.search(r'\*\*Hit Points\*\*\s*(\d+)', block)
    if hp_match:
        statblock["hp"] = int(hp_match.group(1))

    # Speed
    speed_match = re.search(r'\*\*Speed\*\*\s*([^\n]+)', block)
    if speed_match:
        statblock["speed"] = speed_match.group(1).strip()

    # Stats table - look for STR|DEX|CON|INT|WIS|CHA pattern
    stats_match = re.search(r'\|(\d+)\s*\([^)]+\)\|(\d+)\s*\([^)]+\)\|(\d+)\s*\([^)]+\)\|(\d+)\s*\([^)]+\)\|(\d+)\s*\([^)]+\)\|(\d+)\s*\([^)]+\)\|', block)
    if stats_match:
        statblock["str"] = int(stats_match.group(1))
        statblock["dex"] = int(stats_match.group(2))
        statblock["con"] = int(stats_match.group(3))
        statblock["int"] = int(stats_match.group(4))
        statblock["wis"] = int(stats_match.group(5))
        statblock["cha"] = int(stats_match.group(6))

    # CR
    cr_match = re.search(r'\*\*Challenge\*\*\s*([0-9/]+)', block)
    if cr_match:
        cr_str = cr_match.group(1)
        if "/" in cr_str:
            num, den = cr_str.split("/")
            statblock["cr"] = float(num) / float(den)
            statblock["cr_display"] = cr_str
        else:
            statblock["cr"] = float(cr_str)
            statblock["cr_display"] = cr_str

    # Senses
    senses_match = re.search(r'\*\*Senses\*\*\s*([^\n]+)', block)
    if senses_match:
        statblock["senses"] = senses_match.group(1).strip()

    # Languages
    lang_match = re.search(r'\*\*Languages\*\*\s*([^\n]+)', block)
    if lang_match:
        statblock["languages"] = lang_match.group(1).strip()

    # Actions - extract action names and descriptions
    actions = []
    action_section = re.search(r'## Actions(.*?)(?:## |$)', block, re.DOTALL)
    if action_section:
        action_matches = re.findall(r'\*\*\*([^*]+)\*\*\*\.?\s*([^\n]+(?:\n(?!\*\*\*)[^\n]+)*)', action_section.group(1))
        for name, desc in action_matches:
            actions.append({"name": name.strip(), "description": desc.strip()})
    statblock["actions"] = actions

    # Traits
    traits = []
    trait_section = re.search(r'## Traits(.*?)(?:## |$)', block, re.DOTALL)
    if trait_section:
        trait_matches = re.findall(r'\*\*\*([^*]+)\*\*\*\.?\s*([^\n]+(?:\n(?!\*\*\*)[^\n]+)*)', trait_section.group(1))
        for name, desc in trait_matches:
            traits.append({"name": name.strip(), "description": desc.strip()})
    statblock["traits"] = traits

    return statblock


def parse_spell(body):
    """Parse spell information from markdown body."""
    spell = {}

    # Level and school line
    level_match = re.search(r'\*(\d+)(?:st|nd|rd|th)-level,?\s*(\w+)\*', body, re.IGNORECASE)
    if level_match:
        spell["level"] = int(level_match.group(1))
        spell["school"] = level_match.group(2).lower()
    else:
        # Cantrip
        cantrip_match = re.search(r'\*(\w+)\s+cantrip\*', body, re.IGNORECASE)
        if cantrip_match:
            spell["level"] = 0
            spell["school"] = cantrip_match.group(1).lower()

    # Casting time
    cast_match = re.search(r'\*\*Casting [Tt]ime[:\*]*\*?\*?\s*([^\n]+)', body)
    if cast_match:
        spell["casting_time"] = cast_match.group(1).strip()

    # Range
    range_match = re.search(r'\*\*Range[:\*]*\*?\*?\s*([^\n]+)', body)
    if range_match:
        spell["range"] = range_match.group(1).strip()

    # Components
    comp_match = re.search(r'\*\*Components[:\*]*\*?\*?\s*([^\n]+)', body)
    if comp_match:
        spell["components"] = comp_match.group(1).strip()

    # Duration
    dur_match = re.search(r'\*\*Duration[:\*]*\*?\*?\s*([^\n]+)', body)
    if dur_match:
        spell["duration"] = dur_match.group(1).strip()

    # Description - text after the metadata
    desc_match = re.search(r'\*\*Duration[:\*]*\*?[^\n]+\n\n(.+?)(?:\n\*\*(?:At Higher Levels|Classes)\*\*|\n\*Source:|$)', body, re.DOTALL)
    if desc_match:
        spell["description"] = desc_match.group(1).strip()

    # At Higher Levels
    higher_match = re.search(r'\*\*At Higher Levels[.\*]*\*?\*?\s*([^\n]+(?:\n(?!\*\*)[^\n]+)*)', body)
    if higher_match:
        spell["at_higher_levels"] = higher_match.group(1).strip()

    return spell


def parse_item(body):
    """Parse item information from markdown body."""
    item = {}

    # Type/rarity line
    type_match = re.search(r'\*([^*]+),\s*([^*]+)\*', body)
    if type_match:
        item["type_line"] = type_match.group(1).strip()
        item["rarity_line"] = type_match.group(2).strip()

    # Damage (for weapons)
    dmg_match = re.search(r'\*\*Damage[:\*]*\*?\*?\s*([^\n]+)', body)
    if dmg_match:
        item["damage"] = dmg_match.group(1).strip()

    # Properties
    prop_match = re.search(r'\*\*Properties[:\*]*\*?\*?\s*([^\n]+)', body)
    if prop_match:
        item["properties"] = prop_match.group(1).strip()

    # Cost
    cost_match = re.search(r'\*\*Cost[:\*]*\*?\*?\s*([^\n]+)', body)
    if cost_match:
        cost = cost_match.group(1).strip()
        if cost != "⏤":
            item["cost"] = cost

    # Weight
    weight_match = re.search(r'\*\*Weight[:\*]*\*?\*?\s*([^\n]+)', body)
    if weight_match:
        weight = weight_match.group(1).strip()
        if weight != "⏤":
            item["weight"] = weight

    # Description - everything after metadata
    desc_start = body.find("\n\n", body.find("**Weight**") if "**Weight**" in body else 0)
    if desc_start > 0:
        desc_text = body[desc_start:].strip()
        # Remove source line
        desc_text = re.sub(r'\*Source:[^*]+\*', '', desc_text).strip()
        if desc_text:
            item["description"] = desc_text

    return item


def parse_monsters():
    """Parse all monster files."""
    monsters = []
    bestiary_path = SRD_PATH / "bestiary"

    if not bestiary_path.exists():
        print(f"Bestiary path not found: {bestiary_path}")
        return monsters

    for md_file in bestiary_path.rglob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            frontmatter, body = parse_frontmatter(content)

            # Get name from title
            title_match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
            name = title_match.group(1).strip() if title_match else md_file.stem

            # Skip index files
            if name.lower() in ["index", "readme"]:
                continue

            tags = extract_tags(frontmatter)
            statblock = parse_statblock(body)

            monster = {
                "name": statblock.get("name", name),
                "type": tags["type"],
                "subtype": tags["subtype"],
                "size": tags["size"],
                "source": tags["source"],
                "environment": tags["environment"],
                "ac": statblock.get("ac"),
                "hp": statblock.get("hp"),
                "speed": statblock.get("speed"),
                "str": statblock.get("str"),
                "dex": statblock.get("dex"),
                "con": statblock.get("con"),
                "int": statblock.get("int"),
                "wis": statblock.get("wis"),
                "cha": statblock.get("cha"),
                "cr": statblock.get("cr"),
                "cr_display": statblock.get("cr_display"),
                "senses": statblock.get("senses"),
                "languages": statblock.get("languages"),
                "traits": statblock.get("traits", []),
                "actions": statblock.get("actions", []),
                "file": str(md_file.relative_to(SRD_PATH)),
            }

            # Only add if we got meaningful data
            if monster["name"] and (monster["ac"] or monster["hp"] or monster["cr"] is not None):
                monsters.append(monster)

        except Exception as e:
            print(f"Error parsing {md_file}: {e}")

    return sorted(monsters, key=lambda x: x["name"])


def parse_spells():
    """Parse all spell files."""
    spells = []
    spells_path = SRD_PATH / "spells"

    if not spells_path.exists():
        print(f"Spells path not found: {spells_path}")
        return spells

    for md_file in spells_path.glob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            frontmatter, body = parse_frontmatter(content)

            # Get name from title
            title_match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
            name = title_match.group(1).strip() if title_match else md_file.stem

            # Skip index files
            if name.lower() in ["index", "readme"]:
                continue

            tags = extract_tags(frontmatter)
            spell_data = parse_spell(body)

            # Ensure level is an int
            level = spell_data.get("level", tags["level"])
            if isinstance(level, str):
                level = int(level) if level.isdigit() else 0

            spell = {
                "name": name,
                "level": level,
                "school": spell_data.get("school", tags["school"]),
                "classes": tags["classes"],
                "source": tags["source"],
                "casting_time": spell_data.get("casting_time"),
                "range": spell_data.get("range"),
                "components": spell_data.get("components"),
                "duration": spell_data.get("duration"),
                "description": spell_data.get("description"),
                "at_higher_levels": spell_data.get("at_higher_levels"),
                "file": str(md_file.relative_to(SRD_PATH)),
            }

            # Only add if we got meaningful data
            if spell["name"] and spell["level"] is not None:
                spells.append(spell)

        except Exception as e:
            print(f"Error parsing {md_file}: {e}")

    def sort_key(x):
        level = x["level"]
        if level is None:
            level = 0
        elif isinstance(level, str):
            level = int(level) if level.isdigit() else 0
        return (level, x["name"])
    return sorted(spells, key=sort_key)


def parse_items():
    """Parse all item files."""
    items = []
    items_path = SRD_PATH / "items"

    if not items_path.exists():
        print(f"Items path not found: {items_path}")
        return items

    for md_file in items_path.glob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            frontmatter, body = parse_frontmatter(content)

            # Get name from title
            title_match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
            name = title_match.group(1).strip() if title_match else md_file.stem

            # Skip index files
            if name.lower() in ["index", "readme"]:
                continue

            tags = extract_tags(frontmatter)
            item_data = parse_item(body)

            item = {
                "name": name,
                "type": tags["item_type"],
                "rarity": tags["rarity"],
                "tier": tags["tier"],
                "source": tags["source"],
                "type_line": item_data.get("type_line"),
                "rarity_line": item_data.get("rarity_line"),
                "damage": item_data.get("damage"),
                "properties": item_data.get("properties"),
                "cost": item_data.get("cost"),
                "weight": item_data.get("weight"),
                "description": item_data.get("description"),
                "file": str(md_file.relative_to(SRD_PATH)),
            }

            # Only add if we got meaningful data
            if item["name"]:
                items.append(item)

        except Exception as e:
            print(f"Error parsing {md_file}: {e}")

    return sorted(items, key=lambda x: x["name"])


def main():
    """Main parser entry point."""
    print("SRD Parser - Converting markdown to JSON")
    print(f"Source: {SRD_PATH}")
    print(f"Output: {OUTPUT_PATH}")
    print()

    # Ensure output directory exists
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    # Parse monsters
    print("Parsing monsters...")
    monsters = parse_monsters()
    monsters_file = OUTPUT_PATH / "monsters.json"
    with open(monsters_file, "w", encoding="utf-8") as f:
        json.dump(monsters, f, indent=2, ensure_ascii=False)
    print(f"  Wrote {len(monsters)} monsters to {monsters_file.name}")

    # Parse spells
    print("Parsing spells...")
    spells = parse_spells()
    spells_file = OUTPUT_PATH / "spells.json"
    with open(spells_file, "w", encoding="utf-8") as f:
        json.dump(spells, f, indent=2, ensure_ascii=False)
    print(f"  Wrote {len(spells)} spells to {spells_file.name}")

    # Parse items
    print("Parsing items...")
    items = parse_items()
    items_file = OUTPUT_PATH / "items.json"
    with open(items_file, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    print(f"  Wrote {len(items)} items to {items_file.name}")

    print()
    print("Done!")


if __name__ == "__main__":
    main()
