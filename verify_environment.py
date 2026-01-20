#!/usr/bin/env python3
"""
PROJECT LIGHTCONE Environment Verification Script

Checks that your local environment is ready to generate PDFs.
Run this before attempting PDF generation.

Usage: python verify_environment.py
"""

import sys
from pathlib import Path


def print_header(text):
    """Print a section header."""
    print()
    print("=" * 60)
    print(text)
    print("=" * 60)


def print_check(passed, message):
    """Print a check result."""
    icon = "✅" if passed else "❌"
    print(f"{icon} {message}")
    return passed


def check_python_version():
    """Check Python version >= 3.10."""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    if version.major >= 3 and version.minor >= 10:
        return print_check(True, f"Python {version_str} detected (>= 3.10 required)")
    else:
        print_check(False, f"Python {version_str} detected (3.10+ required)")
        print("   Please upgrade Python: https://www.python.org/downloads/")
        return False


def check_repository_structure():
    """Check that we're in the waft repository."""
    required_paths = [
        Path("src/waft"),
        Path("_work_efforts"),
        Path("pyproject.toml"),
    ]

    all_exist = all(p.exists() for p in required_paths)

    if all_exist:
        return print_check(True, "Repository structure valid")
    else:
        print_check(False, "Repository structure invalid")
        print("   Make sure you're in the waft root directory")
        print(f"   Current directory: {Path.cwd()}")
        return False


def check_branch():
    """Check git branch."""
    try:
        import subprocess

        result = subprocess.run(
            ["git", "branch", "--show-current"], capture_output=True, text=True, check=True
        )
        branch = result.stdout.strip()

        if "claude/update-plan-merge-gFm6u" in branch:
            return print_check(True, f"Branch: {branch}")
        else:
            print_check(False, f"Branch: {branch}")
            print("   Expected: claude/update-plan-merge-gFm6u")
            print("   Run: git checkout claude/update-plan-merge-gFm6u")
            return False
    except Exception as e:
        print_check(False, f"Could not check git branch: {e}")
        return False


def check_fpdf2():
    """Check fpdf2 installation."""
    try:
        import fpdf
        from fpdf import FPDF

        version = getattr(fpdf, "__version__", "unknown")
        return print_check(True, f"fpdf2 installed (version: {version})")
    except ImportError:
        print_check(False, "fpdf2 not installed")
        print("   Install with: pip install fpdf2>=2.7.0")
        return False


def check_document_engine():
    """Check DocumentEngine imports."""
    try:
        from waft.foundation import (
            DocumentConfig,
            DocumentEngine,
            KeyValueBlock,
            LogBlock,
            SectionHeader,
            SignatureBlock,
            TextBlock,
            WarningBlock,
        )

        return print_check(True, "DocumentEngine imports successful")
    except ImportError as e:
        print_check(False, "DocumentEngine imports failed")
        print(f"   Error: {e}")
        print("   Try: pip install -e .")
        return False


def check_generation_module():
    """Check that the generation module exists."""
    module_path = Path("src/waft/generate_lightcone_docs.py")

    if module_path.exists():
        size = module_path.stat().st_size
        with open(module_path) as f:
            lines = len(f.readlines())
        return print_check(True, f"Generation module found ({lines} lines, {size} bytes)")
    else:
        print_check(False, "Generation module not found")
        print(f"   Expected: {module_path}")
        return False


def check_markdown_sources():
    """Check that markdown sources exist."""
    markdown_dir = Path("_work_efforts/lightcone_binder/markdown")

    if not markdown_dir.exists():
        print_check(False, "Markdown sources directory not found")
        return False

    # Count markdown files
    md_files = list(markdown_dir.rglob("*.md"))

    if len(md_files) >= 13:
        return print_check(True, f"Markdown sources found ({len(md_files)} files)")
    else:
        print_check(False, f"Markdown sources incomplete ({len(md_files)}/13 files)")
        print("   Run: git pull origin claude/update-plan-merge-gFm6u")
        return False


def check_style_reference():
    """Check that style reference exists."""
    ref_path = Path("_fracture/ARTIFACT_001_GENESIS.pdf")

    if ref_path.exists():
        return print_check(True, "Style reference found (ARTIFACT_001_GENESIS.pdf)")
    else:
        print_check(False, "Style reference not found")
        print("   This is optional - generation will still work")
        return True  # Non-critical


def main():
    """Run all checks."""
    print_header("🔍 PROJECT LIGHTCONE Environment Verification")

    checks = [
        ("Python Version", check_python_version),
        ("Repository Structure", check_repository_structure),
        ("Git Branch", check_branch),
        ("fpdf2 Library", check_fpdf2),
        ("DocumentEngine", check_document_engine),
        ("Generation Module", check_generation_module),
        ("Markdown Sources", check_markdown_sources),
        ("Style Reference", check_style_reference),
    ]

    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print_check(False, f"{name} check failed: {e}")
            results.append((name, False))

    # Summary
    print_header("Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)

    print(f"Passed: {passed}/{total} checks")

    if passed == total:
        print_header("🎉 ALL CHECKS PASSED - Ready to generate PDFs!")
        print()
        print("Next step:")
        print("  python -m src.waft.generate_lightcone_docs")
        print()
        return 0
    else:
        print_header("❌ Some checks failed - see above for fixes")
        print()
        print("Common fixes:")
        print("  1. Install fpdf2: pip install fpdf2>=2.7.0")
        print("  2. Install waft: pip install -e .")
        print("  3. Checkout branch: git checkout claude/update-plan-merge-gFm6u")
        print("  4. Pull latest: git pull origin claude/update-plan-merge-gFm6u")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
