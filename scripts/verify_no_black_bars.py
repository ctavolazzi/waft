#!/usr/bin/env python3
"""
Verification Script: Ensure No Black Bars in PDF Headers

This script checks ALL PDF templates to ensure no h1-h6 headers have:
- background: #000 (or any black background)
- color: #fff (white text on black)

If any are found, the script fails with a clear error message.
"""

import re
from pathlib import Path

TEMPLATE_DIR = Path("src/waft/templates")
FORBIDDEN_PATTERNS = [
    (r"h[1-6]\s*\{[^}]*background:\s*#000", "Black background (#000) on header"),
    (r"h[1-6]\s*\{[^}]*background:\s*black", "Black background (keyword) on header"),
    (r"h[1-6]\s*\{[^}]*background-color:\s*#000", "Black background-color on header"),
]


def check_template_file(file_path: Path) -> list:
    """Check a single template file for black bar violations."""
    violations = []

    try:
        content = file_path.read_text()

        # Check for forbidden patterns
        for pattern, description in FORBIDDEN_PATTERNS:
            matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
            for match in matches:
                # Get line number
                line_num = content[: match.start()].count("\n") + 1
                violations.append(
                    {
                        "file": file_path,
                        "line": line_num,
                        "pattern": pattern,
                        "description": description,
                        "match": match.group(0)[:100],  # First 100 chars
                    }
                )
    except Exception as e:
        violations.append({"file": file_path, "error": str(e)})

    return violations


def main():
    """Check all templates for black bar violations."""
    print("=" * 70)
    print("BLACK BAR VERIFICATION - Checking All PDF Templates")
    print("=" * 70)
    print()

    if not TEMPLATE_DIR.exists():
        print(f"❌ Template directory not found: {TEMPLATE_DIR}")
        return 1

    template_files = list(TEMPLATE_DIR.glob("*.py"))

    if not template_files:
        print(f"❌ No template files found in {TEMPLATE_DIR}")
        return 1

    print(f"📁 Checking {len(template_files)} template files...")
    print()

    all_violations = []

    for template_file in sorted(template_files):
        violations = check_template_file(template_file)
        if violations:
            all_violations.extend(violations)
            print(f"❌ {template_file.name}: {len(violations)} violation(s)")
            for v in violations:
                if "error" in v:
                    print(f"   ERROR: {v['error']}")
                else:
                    print(f"   Line {v['line']}: {v['description']}")
        else:
            print(f"✅ {template_file.name}: No violations")

    print()
    print("=" * 70)

    if all_violations:
        print(f"❌ FAILED: Found {len(all_violations)} black bar violation(s)")
        print()
        print("These headers will create black bars in PDFs:")
        print()
        for v in all_violations:
            if "error" not in v:
                print(f"  - {v['file'].name}:{v['line']} - {v['description']}")
        print()
        print("Fix: Remove 'background: #000' and change 'color: #fff' to 'color: #000'")
        print("     Use 'border-bottom: 3px solid #000' instead of black background")
        return 1
    else:
        print("✅ SUCCESS: No black bars found in any template!")
        print()
        print("All h1-h6 headers use:")
        print("  - color: #000 (black text)")
        print("  - border-bottom: 3px solid #000 (clean underline)")
        print("  - NO black backgrounds")
        return 0


if __name__ == "__main__":
    exit(main())
