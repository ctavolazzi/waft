#!/usr/bin/env python3
"""
Initialize Demo from Template

Copies the demo_template folder to create a new demo instance.
"""

import argparse
import shutil
from pathlib import Path


def init_demo(demo_name: str, template_path: Path = None) -> Path:
    """
    Initialize a new demo from template.

    Args:
        demo_name: Name for the new demo folder
        template_path: Path to template (defaults to demo_template/)

    Returns:
        Path to the new demo folder
    """
    if template_path is None:
        template_path = Path(__file__).parent.parent / "demo_template"

    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    project_root = Path(__file__).parent.parent
    new_demo_path = project_root / demo_name

    if new_demo_path.exists():
        raise FileExistsError(f"Demo already exists: {new_demo_path}")

    print(f"📋 Copying template from {template_path}")
    print(f"📁 Creating demo: {new_demo_path}")

    # Copy template
    shutil.copytree(template_path, new_demo_path)

    print(f"✅ Demo created: {new_demo_path}")
    print("\n📖 Next steps:")
    print(f"  1. Seed the demo: python3 scripts/seed_reincarnation_demo.py --demo-path {demo_name}")
    print(f"  2. Review: {new_demo_path}/README.md")

    return new_demo_path


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Initialize demo from template")
    parser.add_argument("demo_name", type=str, help="Name for the new demo folder")
    parser.add_argument(
        "--template",
        type=str,
        default=None,
        help="Path to template folder (defaults to demo_template/)",
    )

    args = parser.parse_args()

    template_path = Path(args.template) if args.template else None

    try:
        init_demo(args.demo_name, template_path)
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return 1
    except FileExistsError as e:
        print(f"❌ Error: {e}")
        print("   Use --reset flag with seed script to reset existing demo")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
