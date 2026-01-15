#!/usr/bin/env python3
"""
Consolidate Plans Script
========================

Copies all plans from ~/.cursor/plans/ to _work_efforts/Plans/
and creates a consolidated index and summary.
"""

from pathlib import Path
from datetime import datetime
import shutil
import re
from collections import defaultdict
from typing import Dict, List, Tuple

# Paths
CURSOR_PLANS_DIR = Path.home() / ".cursor" / "plans"
WORK_EFFORTS_DIR = Path(__file__).parent.parent / "_work_efforts"
PLANS_DIR = WORK_EFFORTS_DIR / "Plans"

def extract_plan_metadata(plan_path: Path) -> Dict:
    """Extract metadata from plan file frontmatter."""
    metadata = {
        "name": None,
        "overview": None,
        "created_date": None,
        "file_name": plan_path.name,
        "file_stem": plan_path.stem,
    }

    try:
        content = plan_path.read_text(encoding='utf-8')

        # Extract frontmatter
        frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)

            # Extract name
            name_match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
            if name_match:
                metadata["name"] = name_match.group(1).strip()

            # Extract overview
            overview_match = re.search(r'^overview:\s*(.+)$', frontmatter, re.MULTILINE)
            if overview_match:
                metadata["overview"] = overview_match.group(1).strip()

        # Extract date from filename if possible (format: name_date_hash.plan.md)
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', plan_path.stem)
        if date_match:
            metadata["created_date"] = date_match.group(1)
        else:
            # Use file modification time
            mtime = datetime.fromtimestamp(plan_path.stat().st_mtime)
            metadata["created_date"] = mtime.strftime("%Y-%m-%d")

    except Exception as e:
        print(f"⚠️  Error reading {plan_path.name}: {e}")

    return metadata

def organize_plans_by_date(plans: List[Tuple[Path, Dict]]) -> Dict[str, List[Tuple[Path, Dict]]]:
    """Organize plans by date."""
    by_date = defaultdict(list)
    for plan_path, metadata in plans:
        date = metadata.get("created_date", "unknown")
        by_date[date].append((plan_path, metadata))
    return dict(by_date)

def create_consolidated_index(plans: List[Tuple[Path, Dict]], output_path: Path):
    """Create a consolidated index of all plans."""

    # Organize by date
    by_date = organize_plans_by_date(plans)

    # Generate index content
    lines = [
        "# Plans Consolidation Index",
        "",
        f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Total Plans**: {len(plans)}",
        "",
        "---",
        "",
        "## Summary",
        "",
        f"This directory contains {len(plans)} development plans copied from `~/.cursor/plans/`.",
        "",
        "### Organization",
        "",
        "- Plans are organized by date (YYYY-MM-DD)",
        "- Each plan retains its original filename",
        "- Original plans remain in `~/.cursor/plans/`",
        "",
        "---",
        "",
        "## Plans by Date",
        "",
    ]

    # Sort dates
    sorted_dates = sorted(by_date.keys(), reverse=True)

    for date in sorted_dates:
        date_plans = by_date[date]
        lines.append(f"### {date} ({len(date_plans)} plans)")
        lines.append("")

        # Sort plans by name
        date_plans_sorted = sorted(date_plans, key=lambda x: (x[1].get("name") or x[0].stem) or "")

        for plan_path, metadata in date_plans_sorted:
            name = metadata.get("name", plan_path.stem)
            overview = metadata.get("overview", "No overview available")
            file_name = metadata["file_name"]

            lines.append(f"- **{name}**")
            lines.append(f"  - File: `{file_name}`")
            if overview and overview != "No overview available":
                lines.append(f"  - Overview: {overview}")
            lines.append("")

    lines.extend([
        "---",
        "",
        "## All Plans (Alphabetical)",
        "",
    ])

    # Sort all plans alphabetically by name
    all_plans_sorted = sorted(plans, key=lambda x: ((x[1].get("name") or x[0].stem) or "").lower())

    for plan_path, metadata in all_plans_sorted:
        name = metadata.get("name", plan_path.stem)
        file_name = metadata["file_name"]
        lines.append(f"- [{name}]({file_name})")

    # Write index
    output_path.write_text("\n".join(lines), encoding='utf-8')
    print(f"✅ Created index: {output_path.name}")

def create_consolidation_summary(plans: List[Tuple[Path, Dict]], output_path: Path):
    """Create a summary document with statistics and insights."""

    # Statistics
    total_plans = len(plans)
    by_date = organize_plans_by_date(plans)
    dates_count = len(by_date)

    # Extract keywords/themes
    keywords = defaultdict(int)
    for _, metadata in plans:
        name = (metadata.get("name") or "").lower()
        overview = (metadata.get("overview") or "").lower()
        text = f"{name} {overview}"

        # Common keywords
        for keyword in ["api", "ui", "pdf", "test", "integration", "refactor", "documentation",
                       "feature", "bug", "fix", "system", "architecture", "design", "workflow"]:
            if keyword in text:
                keywords[keyword] += 1

    # Generate summary
    lines = [
        "# Plans Consolidation Summary",
        "",
        f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "---",
        "",
        "## Statistics",
        "",
        f"- **Total Plans**: {total_plans}",
        f"- **Unique Dates**: {dates_count}",
        f"- **Date Range**: {min(by_date.keys())} to {max(by_date.keys())}",
        "",
        "---",
        "",
        "## Common Themes",
        "",
    ]

    # Sort keywords by frequency
    sorted_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)
    for keyword, count in sorted_keywords[:20]:  # Top 20
        lines.append(f"- **{keyword.title()}**: {count} plans")

    lines.extend([
        "",
        "---",
        "",
        "## Notes",
        "",
        "- All plans have been copied from `~/.cursor/plans/`",
        "- Original plans remain in their original location",
        "- Plans are organized by date in the index",
        "- See `00_INDEX.md` for the complete alphabetical listing",
        "",
        "---",
        "",
        "*This summary was automatically generated by `scripts/consolidate_plans.py`*",
    ])

    output_path.write_text("\n".join(lines), encoding='utf-8')
    print(f"✅ Created summary: {output_path.name}")

def main():
    """Main execution function."""
    print("\n" + "=" * 60)
    print("📋 PLANS CONSOLIDATION SCRIPT")
    print("=" * 60)
    print()

    # Check source directory
    if not CURSOR_PLANS_DIR.exists():
        print(f"❌ Source directory not found: {CURSOR_PLANS_DIR}")
        return 1

    # Create destination directory
    PLANS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"📁 Destination: {PLANS_DIR}")
    print()

    # Find all plan files
    plan_files = list(CURSOR_PLANS_DIR.glob("*.plan.md"))
    print(f"📄 Found {len(plan_files)} plan files")
    print()

    if not plan_files:
        print("⚠️  No plan files found. Nothing to consolidate.")
        return 0

    # Process each plan
    plans_data = []
    copied_count = 0
    skipped_count = 0

    print("📋 Processing plans...")
    for plan_path in sorted(plan_files):
        try:
            # Extract metadata
            metadata = extract_plan_metadata(plan_path)
            plans_data.append((plan_path, metadata))

            # Copy file
            dest_path = PLANS_DIR / plan_path.name
            if dest_path.exists():
                # File already exists, skip
                skipped_count += 1
                print(f"  ⏭️  Skipped (exists): {plan_path.name}")
            else:
                shutil.copy2(plan_path, dest_path)
                copied_count += 1
                if copied_count % 50 == 0:
                    print(f"  ✅ Copied {copied_count} plans...")

        except Exception as e:
            print(f"  ❌ Error processing {plan_path.name}: {e}")
            skipped_count += 1

    print()
    print(f"✅ Copied: {copied_count} plans")
    print(f"⏭️  Skipped: {skipped_count} plans (already exist)")
    print()

    # Create consolidated index
    print("📝 Creating consolidated index...")
    index_path = PLANS_DIR / "00_INDEX.md"
    create_consolidated_index(plans_data, index_path)

    # Create summary
    print("📊 Creating consolidation summary...")
    summary_path = PLANS_DIR / "00_SUMMARY.md"
    create_consolidation_summary(plans_data, summary_path)

    print()
    print("=" * 60)
    print("✅ CONSOLIDATION COMPLETE!")
    print("=" * 60)
    print()
    print(f"📁 Location: {PLANS_DIR.absolute()}")
    print(f"📄 Plans: {copied_count} copied, {skipped_count} skipped")
    print(f"📋 Index: {index_path.name}")
    print(f"📊 Summary: {summary_path.name}")
    print()

    return 0

if __name__ == "__main__":
    exit(main())
