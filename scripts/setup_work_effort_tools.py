#!/usr/bin/env python3
"""
Setup Work Effort Tool Bag

Automatically creates a tools/ folder with standard tools for a new work effort.

Usage:
    python scripts/setup_work_effort_tools.py <work_effort_path>
    
    Example:
    python scripts/setup_work_effort_tools.py _work_efforts/WE-260110-order66_order_66_execution
"""

import argparse
import shutil
from pathlib import Path
from datetime import datetime


# Template location
TEMPLATE_DIR = Path(__file__).parent.parent / "_work_efforts" / ".tool_bag_template"

# Standard tools to always include
STANDARD_TOOLS = [
    "work_effort_tracker.md",
    "verification_checklist.md",
    "README.md",
]


def create_tool_bag(work_effort_path: Path, include_optional: bool = False):
    """Create tool bag for a work effort."""
    work_effort_path = Path(work_effort_path).resolve()
    
    if not work_effort_path.exists():
        raise ValueError(f"Work effort path does not exist: {work_effort_path}")
    
    if not work_effort_path.is_dir():
        raise ValueError(f"Work effort path is not a directory: {work_effort_path}")
    
    # Create tools directory
    tools_dir = work_effort_path / "tools"
    tools_dir.mkdir(exist_ok=True)
    
    print(f"📦 Creating tool bag in: {tools_dir}")
    
    # Copy standard tools
    copied = []
    for tool_name in STANDARD_TOOLS:
        template_file = TEMPLATE_DIR / tool_name
        if template_file.exists():
            dest_file = tools_dir / tool_name
            shutil.copy2(template_file, dest_file)
            copied.append(tool_name)
            print(f"  ✅ Copied: {tool_name}")
        else:
            print(f"  ⚠️  Template not found: {tool_name}")
    
    # Create templates directory if needed
    templates_dir = tools_dir / "templates"
    templates_dir.mkdir(exist_ok=True)
    
    # Copy optional tools if requested
    if include_optional:
        optional_tools = [
            "analysis_template.md",
            "decision_matrix.py",
            "priority_matrix.py",
        ]
        
        for tool_name in optional_tools:
            template_file = TEMPLATE_DIR / tool_name
            if template_file.exists():
                dest_file = tools_dir / tool_name
                shutil.copy2(template_file, dest_file)
                copied.append(tool_name)
                print(f"  ✅ Copied (optional): {tool_name}")
    
    # Update README with work effort info
    readme_file = tools_dir / "README.md"
    if readme_file.exists():
        content = readme_file.read_text()
        content = content.replace(
            "**Template Version**: 1.0",
            f"**Work Effort**: {work_effort_path.name}\n**Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n**Template Version**: 1.0"
        )
        readme_file.write_text(content)
    
    print(f"\n✅ Tool bag created successfully!")
    print(f"   Location: {tools_dir}")
    print(f"   Tools copied: {len(copied)}")
    print(f"\n📖 See {tools_dir / 'README.md'} for tool documentation")
    
    return tools_dir


def main():
    parser = argparse.ArgumentParser(
        description="Setup tool bag for a work effort"
    )
    parser.add_argument(
        "work_effort_path",
        type=str,
        help="Path to work effort directory (e.g., _work_efforts/WE-260110-xxxx_description)"
    )
    parser.add_argument(
        "--include-optional",
        action="store_true",
        help="Include optional tools (decision matrix, priority matrix, analysis template)"
    )
    
    args = parser.parse_args()
    
    try:
        create_tool_bag(args.work_effort_path, args.include_optional)
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
