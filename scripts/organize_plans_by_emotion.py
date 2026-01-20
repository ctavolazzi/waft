#!/usr/bin/env python3
"""
Organize Plans by Emotional Constellation
==========================================

Reads all plan files and reorganizes them into a constellation of:
- Hopes: Aspirational features, improvements, enhancements
- Dreams: Visionary, ambitious, transformative ideas
- Dreads: Maintenance, fixes, technical debt, cleanup
- Fears: Security, failures, risks, critical issues

Creates new organized versions without moving originals.
"""

import re
import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# Paths
PLANS_DIR = Path(__file__).parent.parent / "_work_efforts" / "Plans"
ORGANIZED_DIR = PLANS_DIR / "_organized_constellation"
ORIGINALS_DIR = ORGANIZED_DIR / "_originals_backup"

# Emotional categories with keywords
CATEGORIES = {
    "hopes": {
        "keywords": [
            "enhancement",
            "improvement",
            "upgrade",
            "polish",
            "refine",
            "feature",
            "add",
            "implement",
            "create",
            "build",
            "new",
            "integration",
            "connect",
            "expand",
            "extend",
            "evolve",
        ],
        "description": "Aspirational features, improvements, and enhancements",
    },
    "dreams": {
        "keywords": [
            "vision",
            "architecture",
            "system",
            "revolutionary",
            "transform",
            "paradigm",
            "foundation",
            "core",
            "prime directive",
            "celestial",
            "evolution",
            "reincarnation",
            "being",
            "reality",
            "cosmic",
            "eternal",
            "sovereign",
            "intelligence",
            "meta",
            "self-improving",
            "larval",
            "mature form",
            "heavy seed",
            "protocol",
        ],
        "description": "Visionary, ambitious, transformative ideas",
    },
    "dreads": {
        "keywords": [
            "fix",
            "bug",
            "error",
            "issue",
            "problem",
            "cleanup",
            "clean",
            "remove",
            "delete",
            "refactor",
            "audit",
            "review",
            "simplify",
            "maintenance",
            "debt",
            "technical debt",
            "update",
            "migration",
            "deprecate",
            "obsolete",
            "stale",
            "broken",
            "failure",
        ],
        "description": "Maintenance, fixes, technical debt, cleanup",
    },
    "fears": {
        "keywords": [
            "security",
            "vulnerability",
            "risk",
            "critical",
            "urgent",
            "failure",
            "crash",
            "error",
            "exception",
            "malformed",
            "scan",
            "remediation",
            "alert",
            "danger",
            "threat",
            "breach",
            "secret",
            "token",
            "key",
            "auth",
            "permission",
            "access",
        ],
        "description": "Security, failures, risks, critical issues",
    },
}


def extract_plan_metadata(plan_path: Path) -> dict:
    """Extract metadata from plan file."""
    metadata = {
        "name": None,
        "overview": None,
        "created_date": None,
        "file_name": plan_path.name,
        "file_stem": plan_path.stem,
        "content": "",
        "frontmatter": {},
    }

    try:
        content = plan_path.read_text(encoding="utf-8")
        metadata["content"] = content

        # Extract frontmatter
        frontmatter_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if frontmatter_match:
            frontmatter_text = frontmatter_match.group(1)

            # Parse frontmatter
            for line in frontmatter_text.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    metadata["frontmatter"][key.strip()] = value.strip()

            # Extract name
            if "name" in metadata["frontmatter"]:
                metadata["name"] = metadata["frontmatter"]["name"]

            # Extract overview
            if "overview" in metadata["frontmatter"]:
                metadata["overview"] = metadata["frontmatter"]["overview"]

        # Extract date from filename
        date_match = re.search(r"(\d{4}-\d{2}-\d{2})", plan_path.stem)
        if date_match:
            metadata["created_date"] = date_match.group(1)
        else:
            mtime = datetime.fromtimestamp(plan_path.stat().st_mtime)
            metadata["created_date"] = mtime.strftime("%Y-%m-%d")

    except Exception as e:
        print(f"⚠️  Error reading {plan_path.name}: {e}")

    return metadata


def categorize_plan(metadata: dict) -> tuple[str, float]:
    """Categorize a plan into emotional constellation. Returns (category, confidence)."""
    name = (metadata.get("name") or "").lower()
    overview = (metadata.get("overview") or "").lower()
    content = (metadata.get("content") or "").lower()

    # Combine all text for analysis
    text = f"{name} {overview} {content[:500]}"  # First 500 chars of content

    # Score each category
    scores = {}
    for category, config in CATEGORIES.items():
        score = 0
        for keyword in config["keywords"]:
            # Count occurrences
            count = text.count(keyword.lower())
            score += count * 2  # Weight keyword matches

        # Check filename patterns
        file_stem = metadata.get("file_stem", "").lower()
        for keyword in config["keywords"]:
            if keyword in file_stem:
                score += 3  # Higher weight for filename matches

        scores[category] = score

    # Find highest scoring category
    if max(scores.values()) == 0:
        # Default to "hopes" if no matches
        return ("hopes", 0.0)

    best_category = max(scores.items(), key=lambda x: x[1])
    total_score = sum(scores.values())
    confidence = best_category[1] / total_score if total_score > 0 else 0.0

    return (best_category[0], confidence)


def create_organized_structure():
    """Create directory structure for organized plans."""
    for category in CATEGORIES.keys():
        (ORGANIZED_DIR / category).mkdir(parents=True, exist_ok=True)

    # Create originals backup location (for reference)
    ORIGINALS_DIR.mkdir(parents=True, exist_ok=True)


def write_organized_plan(plan_path: Path, metadata: dict, category: str, confidence: float):
    """Write organized plan to new location with category metadata."""
    category_dir = ORGANIZED_DIR / category
    new_filename = f"{category}_{metadata['file_name']}"
    new_path = category_dir / new_filename

    # Read original content
    content = metadata.get("content", "")

    # Add category metadata to frontmatter
    if content.startswith("---"):
        # Insert category info after first frontmatter
        frontmatter_end = content.find("---", 3)
        if frontmatter_end > 0:
            frontmatter = content[: frontmatter_end + 3]
            body = content[frontmatter_end + 3 :]

            # Add category metadata
            category_meta = f"\ncategory: {category}\nconfidence: {confidence:.2f}\nconstellation_date: {datetime.now().strftime('%Y-%m-%d')}\n"

            # Insert before closing ---
            new_frontmatter = frontmatter[:-3] + category_meta + "---"
            new_content = new_frontmatter + body
        else:
            new_content = content
    else:
        # No frontmatter, add it
        category_meta = f"""---
category: {category}
confidence: {confidence:.2f}
constellation_date: {datetime.now().strftime("%Y-%m-%d")}
original_file: {metadata["file_name"]}
---

"""
        new_content = category_meta + content

    # Write organized plan
    new_path.write_text(new_content, encoding="utf-8")

    # Also copy to originals backup for reference
    backup_path = ORIGINALS_DIR / metadata["file_name"]
    if not backup_path.exists():
        shutil.copy2(plan_path, backup_path)


def create_constellation_index(plans_by_category: dict[str, list[tuple[Path, dict, str, float]]]):
    """Create master index of organized constellation."""
    lines = [
        "# Plans Constellation: Hopes, Dreams, Dreads, and Fears",
        "",
        f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "This is an emotional reorganization of all plans into a constellation of:",
        "",
        "- **Hopes**: Aspirational features, improvements, and enhancements",
        "- **Dreams**: Visionary, ambitious, transformative ideas",
        "- **Dreads**: Maintenance, fixes, technical debt, cleanup",
        "- **Fears**: Security, failures, risks, critical issues",
        "",
        "---",
        "",
        "## Constellation Overview",
        "",
    ]

    # Summary stats
    total = sum(len(plans) for plans in plans_by_category.values())
    lines.append(f"**Total Plans Organized**: {total}")
    lines.append("")

    for category, config in CATEGORIES.items():
        count = len(plans_by_category.get(category, []))
        lines.append(f"- **{category.title()}**: {count} plans - {config['description']}")

    lines.extend(
        [
            "",
            "---",
            "",
            "## By Category",
            "",
        ]
    )

    # Detailed breakdown by category
    for category, config in CATEGORIES.items():
        plans = plans_by_category.get(category, [])
        lines.append(f"### {category.title()} ({len(plans)} plans)")
        lines.append("")
        lines.append(f"*{config['description']}*")
        lines.append("")

        # Sort by confidence (highest first)
        sorted_plans = sorted(plans, key=lambda x: x[3], reverse=True)

        for _plan_path, metadata, _cat, confidence in sorted_plans:
            name = metadata.get("name", metadata.get("file_stem", "Unknown"))
            file_name = metadata["file_name"]
            new_file = f"{category}_{file_name}"

            lines.append(f"- **{name}** (confidence: {confidence:.2f})")
            lines.append(f"  - File: [{new_file}]({category}/{new_file})")
            if metadata.get("overview"):
                overview = (
                    metadata["overview"][:100] + "..."
                    if len(metadata.get("overview", "")) > 100
                    else metadata["overview"]
                )
                lines.append(f"  - Overview: {overview}")
            lines.append("")

    # Write index
    index_path = ORGANIZED_DIR / "00_CONSTELLATION_INDEX.md"
    index_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ Created constellation index: {index_path.name}")


def create_category_readme(category: str, config: dict, plans: list[tuple[Path, dict, str, float]]):
    """Create README for each category."""
    lines = [
        f"# {category.title()}",
        "",
        f"*{config['description']}*",
        "",
        f"**Count**: {len(plans)} plans",
        "",
        "---",
        "",
        "## Plans",
        "",
    ]

    # Sort by confidence
    sorted_plans = sorted(plans, key=lambda x: x[3], reverse=True)

    for _plan_path, metadata, _cat, confidence in sorted_plans:
        name = metadata.get("name", metadata.get("file_stem", "Unknown"))
        file_name = metadata["file_name"]
        new_file = f"{category}_{file_name}"
        created_date = metadata.get("created_date", "Unknown")

        lines.append(f"### {name}")
        lines.append("")
        lines.append(f"- **Confidence**: {confidence:.2f}")
        lines.append(f"- **Date**: {created_date}")
        lines.append(f"- **File**: [{new_file}]({new_file})")
        if metadata.get("overview"):
            lines.append(f"- **Overview**: {metadata['overview']}")
        lines.append("")

    # Write README
    readme_path = ORGANIZED_DIR / category / "README.md"
    readme_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    """Main execution function."""
    print("\n" + "=" * 70)
    print("🌟 PLANS CONSTELLATION ORGANIZER")
    print("=" * 70)
    print()

    # Check source directory
    if not PLANS_DIR.exists():
        print(f"❌ Plans directory not found: {PLANS_DIR}")
        return 1

    # Create organized structure
    print("📁 Creating organized structure...")
    create_organized_structure()
    print(f"📁 Organized plans will be in: {ORGANIZED_DIR}")
    print()

    # Find all plan files
    plan_files = list(PLANS_DIR.glob("*.plan.md"))
    print(f"📄 Found {len(plan_files)} plan files")
    print()

    if not plan_files:
        print("⚠️  No plan files found. Nothing to organize.")
        return 0

    # Process each plan
    plans_by_category = defaultdict(list)
    processed_count = 0

    print("🔮 Categorizing plans into constellation...")
    for plan_path in sorted(plan_files):
        try:
            # Extract metadata
            metadata = extract_plan_metadata(plan_path)

            # Categorize
            category, confidence = categorize_plan(metadata)

            # Store
            plans_by_category[category].append((plan_path, metadata, category, confidence))

            # Write organized version
            write_organized_plan(plan_path, metadata, category, confidence)

            processed_count += 1
            if processed_count % 50 == 0:
                print(f"  ✨ Processed {processed_count} plans...")

        except Exception as e:
            print(f"  ❌ Error processing {plan_path.name}: {e}")

    print()
    print(f"✅ Processed: {processed_count} plans")
    print()

    # Create constellation index
    print("📝 Creating constellation index...")
    create_constellation_index(plans_by_category)

    # Create category READMEs
    print("📚 Creating category READMEs...")
    for category, config in CATEGORIES.items():
        plans = plans_by_category.get(category, [])
        create_category_readme(category, config, plans)
        print(f"  ✅ Created README for {category} ({len(plans)} plans)")

    print()
    print("=" * 70)
    print("✅ CONSTELLATION ORGANIZATION COMPLETE!")
    print("=" * 70)
    print()
    print(f"📁 Location: {ORGANIZED_DIR.absolute()}")
    print(f"📄 Plans organized: {processed_count}")
    print()

    # Print summary
    for category, config in CATEGORIES.items():
        count = len(plans_by_category.get(category, []))
        print(f"  {category.title()}: {count} plans")

    print()
    print("💡 Original plans remain untouched in:", PLANS_DIR.absolute())
    print("📋 See 00_CONSTELLATION_INDEX.md for the full constellation")
    print()

    return 0


if __name__ == "__main__":
    exit(main())
