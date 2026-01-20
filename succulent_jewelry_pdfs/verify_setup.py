#!/usr/bin/env python3
"""
Verify Setup
============

Quick verification that all components are in place.
"""

import sys
from pathlib import Path

SUCCULENT_PDFS_ROOT = Path(__file__).parent


def verify_structure():
    """Verify directory structure exists."""
    required_dirs = [
        "templates",
        "content/guides",
        "content/poetry",
        "generated/guides",
        "generated/poetry",
        "scripts",
        "config",
    ]

    missing = []
    for dir_path in required_dirs:
        full_path = SUCCULENT_PDFS_ROOT / dir_path
        if not full_path.exists():
            missing.append(dir_path)

    if missing:
        print(f"❌ Missing directories: {', '.join(missing)}")
        return False

    print("✅ Directory structure OK")
    return True


def verify_files():
    """Verify required files exist."""
    required_files = [
        "templates/guide_template.py",
        "templates/poetry_template.py",
        "scripts/generate_guide.py",
        "scripts/batch_generate.py",
        "scripts/gumroad_prep.py",
        "scripts/security.py",
        "scripts/validation.py",
        "scripts/resource_manager.py",
        "config/guide_config.json",
        "config/gumroad_metadata.json",
        "content/guides/template.md",
        "README.md",
        ".gitignore",
        "requirements.txt",
    ]

    missing = []
    for file_path in required_files:
        full_path = SUCCULENT_PDFS_ROOT / file_path
        if not full_path.exists():
            missing.append(file_path)

    if missing:
        print(f"❌ Missing files: {', '.join(missing)}")
        return False

    print("✅ Required files present")
    return True


def verify_imports():
    """Verify Python imports work (may fail if dependencies not installed)."""
    sys.path.insert(0, str(SUCCULENT_PDFS_ROOT))

    try:
        from templates.guide_template import generate_guide
        from templates.poetry_template import generate_poetry

        print("✅ Template imports OK")
        return True
    except ImportError as e:
        print(f"⚠️  Template import issue (may need dependencies): {e}")
        return False


def verify_dependencies():
    """Check if dependencies are installed."""
    dependencies = {
        "weasyprint": "WeasyPrint",
        "markdown": "Markdown",
        "bleach": "Bleach",
        "PyPDF2": "PyPDF2",
    }

    missing = []
    for module, name in dependencies.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(name)

    if missing:
        print(f"⚠️  Missing dependencies: {', '.join(missing)}")
        print("   Install with: pip install -r requirements.txt")
        return False

    print("✅ All dependencies installed")
    return True


def main():
    """Run all verification checks."""
    print("Verifying Succulent Jewelry PDF System Setup\n")
    print("=" * 60)

    checks = [
        ("Directory Structure", verify_structure),
        ("Required Files", verify_files),
        ("Python Imports", verify_imports),
        ("Dependencies", verify_dependencies),
    ]

    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        result = check_func()
        results.append((name, result))

    print("\n" + "=" * 60)
    print("\nSummary:")

    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {name}")
        if not result:
            all_passed = False

    if all_passed:
        print("\n🎉 All checks passed! System is ready to use.")
        return 0
    else:
        print("\n⚠️  Some checks failed. Review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
