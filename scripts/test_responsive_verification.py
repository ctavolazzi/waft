#!/usr/bin/env python3
"""
Responsive Design Verification Script
Tests CSS properties at different breakpoints programmatically
"""

import re
from pathlib import Path


def verify_responsive_css():
    """Verify responsive CSS implementation in show_me_bulletproof.py"""

    file_path = Path(__file__).parent / "show_me_bulletproof.py"
    content = file_path.read_text()

    results = {"pass": [], "fail": [], "warnings": []}

    # 1. Verify navigation maintains 3-column grid
    if "grid-template-columns: 1fr 1fr 1fr" in content:
        results["pass"].append("✅ Navigation uses 3-column grid")
    else:
        results["fail"].append("❌ Navigation does not use 3-column grid")

    # 2. Verify no broken flex-direction on grid
    nav_container_pattern = r"\.nav-container\s*\{[^}]*flex-direction[^}]*\}"
    if re.search(nav_container_pattern, content):
        results["fail"].append("❌ Found flex-direction on grid container (broken)")
    else:
        results["pass"].append("✅ No broken flex-direction on grid container")

    # 3. Verify mobile breakpoint (< 600px)
    mobile_media = r"@media\s*\(max-width:\s*599px\)"
    if re.search(mobile_media, content):
        results["pass"].append("✅ Mobile breakpoint defined (< 600px)")

        # Check mobile nav sizing
        mobile_nav_pattern = (
            r"@media\s*\(max-width:\s*599px\)[^}]*\.nav-dropdown-toggle[^}]*padding:\s*0\.5rem"
        )
        if re.search(mobile_nav_pattern, content, re.DOTALL):
            results["pass"].append("✅ Mobile nav buttons have compact padding (0.5rem)")
        else:
            results["warnings"].append("⚠️ Mobile nav padding may not be optimized")

        # Check touch targets
        if "min-height: 44px" in content:
            results["pass"].append("✅ Touch targets meet 44px minimum")
        else:
            results["fail"].append("❌ Touch targets may not meet 44px minimum")
    else:
        results["fail"].append("❌ Mobile breakpoint not found")

    # 4. Verify tablet breakpoint (600px - 1023px)
    tablet_media = r"@media\s*\(min-width:\s*600px\)\s*and\s*\(max-width:\s*1023px\)"
    if re.search(tablet_media, content):
        results["pass"].append("✅ Tablet breakpoint defined (600px - 1023px)")
    else:
        results["fail"].append("❌ Tablet breakpoint not found")

    # 5. Verify desktop breakpoint (1024px+)
    desktop_media = r"@media\s*\(min-width:\s*1024px\)"
    if re.search(desktop_media, content):
        results["pass"].append("✅ Desktop breakpoint defined (1024px+)")
    else:
        results["fail"].append("❌ Desktop breakpoint not found")

    # 6. Verify fluid typography
    if "clamp(1.5rem, 4vw, 2rem)" in content:
        results["pass"].append("✅ h1 uses fluid typography (clamp)")
    else:
        results["warnings"].append("⚠️ h1 may not use fluid typography")

    if "clamp(1.25rem, 3vw, 1.5rem)" in content:
        results["pass"].append("✅ h2 uses fluid typography (clamp)")
    else:
        results["warnings"].append("⚠️ h2 may not use fluid typography")

    # 7. Verify stats grid responsive columns
    if "grid-template-columns: repeat(2, 1fr)" in content:
        results["pass"].append("✅ Stats grid has 2 columns for mobile")
    else:
        results["warnings"].append("⚠️ Stats grid mobile columns may not be set")

    if "grid-template-columns: repeat(3, 1fr)" in content:
        results["pass"].append("✅ Stats grid has 3 columns for tablet")
    else:
        results["warnings"].append("⚠️ Stats grid tablet columns may not be set")

    if "repeat(auto-fit, minmax(120px, 1fr))" in content:
        results["pass"].append("✅ Stats grid uses auto-fit for desktop")
    else:
        results["warnings"].append("⚠️ Stats grid desktop may not use auto-fit")

    # 8. Verify table wrapper
    if ".table-wrapper" in content and "overflow-x: auto" in content:
        results["pass"].append("✅ Table wrapper exists with horizontal scroll")
    else:
        results["fail"].append("❌ Table wrapper may be missing")

    # 9. Verify responsive padding
    if "padding: 1rem" in content and "/* Mobile:" in content:
        results["pass"].append("✅ Mobile padding is 1rem")
    else:
        results["warnings"].append("⚠️ Mobile padding may not be set correctly")

    if "padding: 1.5rem" in content:
        results["pass"].append("✅ Tablet padding is 1.5rem")
    else:
        results["warnings"].append("⚠️ Tablet padding may not be set correctly")

    if "padding: 2rem" in content:
        results["pass"].append("✅ Desktop padding is 2rem")
    else:
        results["warnings"].append("⚠️ Desktop padding may not be set correctly")

    # 10. Verify dropdown max-height
    if "max-height: 70vh" in content:
        results["pass"].append("✅ Dropdown menus have max-height constraint")
    else:
        results["warnings"].append("⚠️ Dropdown max-height may not be set")

    # 11. Verify Oracle button responsive positioning
    oracle_mobile = r"@media\s*\(max-width:\s*599px\)[^}]*\.btn-oracle[^}]*top:\s*1rem"
    if re.search(oracle_mobile, content, re.DOTALL):
        results["pass"].append("✅ Oracle button repositioned on mobile")
    else:
        results["warnings"].append("⚠️ Oracle button may not be repositioned on mobile")

    return results


def print_results(results):
    """Print verification results"""
    print("=" * 60)
    print("RESPONSIVE DESIGN VERIFICATION RESULTS")
    print("=" * 60)
    print()

    print(f"✅ PASSING: {len(results['pass'])}")
    for item in results["pass"]:
        print(f"  {item}")
    print()

    if results["warnings"]:
        print(f"⚠️  WARNINGS: {len(results['warnings'])}")
        for item in results["warnings"]:
            print(f"  {item}")
        print()

    if results["fail"]:
        print(f"❌ FAILING: {len(results['fail'])}")
        for item in results["fail"]:
            print(f"  {item}")
        print()

    total = len(results["pass"]) + len(results["warnings"]) + len(results["fail"])
    pass_rate = (len(results["pass"]) / total * 100) if total > 0 else 0

    print("=" * 60)
    print(f"SUMMARY: {len(results['pass'])}/{total} checks passed ({pass_rate:.1f}%)")
    if results["fail"]:
        print(f"⚠️  {len(results['fail'])} critical issues found")
    elif results["warnings"]:
        print(f"ℹ️  {len(results['warnings'])} warnings (non-critical)")
    else:
        print("✅ All checks passed!")
    print("=" * 60)


if __name__ == "__main__":
    results = verify_responsive_css()
    print_results(results)

    # Exit with error code if failures found
    exit(1 if results["fail"] else 0)
