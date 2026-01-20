#!/usr/bin/env python3
"""
Verify Python Version for Waft Project

This script ensures we're using Python 3.12 for the Waft project,
which is required for Empirica integration.
"""

import subprocess
import sys
from pathlib import Path

REQUIRED_PYTHON_VERSION = (3, 12)
REQUIRED_PYTHON_VERSION_STR = "3.12"


def check_python_version():
    """Check if we're using the correct Python version."""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}"

    print(f"Current Python version: {version_str}")
    print(f"Required Python version: {REQUIRED_PYTHON_VERSION_STR}+")

    if version.major == REQUIRED_PYTHON_VERSION[0] and version.minor >= REQUIRED_PYTHON_VERSION[1]:
        print("✅ Python version is correct!")
        return True
    else:
        print(f"❌ Python version mismatch! Need {REQUIRED_PYTHON_VERSION_STR}+")
        return False


def check_empirica():
    """Check if Empirica is available and using correct Python."""
    # Try Python 3.12's empirica first
    empirica_path = "/Library/Frameworks/Python.framework/Versions/3.12/bin/empirica"

    if Path(empirica_path).exists():
        try:
            result = subprocess.run(
                [empirica_path, "--version"], capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                print(f"✅ Empirica found: {empirica_path}")
                print(f"   {result.stdout.strip()}")
                return True
        except Exception as e:
            print(f"⚠️  Empirica path exists but failed to run: {e}")

    # Try system empirica
    try:
        result = subprocess.run(
            ["empirica", "--version"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            print("✅ Empirica found in PATH")
            print(f"   {result.stdout.strip()}")
            # Check if it's using Python 3.12
            if "3.12" in result.stdout or "3.11" in result.stdout:
                return True
            else:
                print("⚠️  Empirica is using a different Python version")
                return False
    except FileNotFoundError:
        print("❌ Empirica not found")
        return False
    except Exception as e:
        print(f"❌ Error checking Empirica: {e}")
        return False


def check_empirica_initialized():
    """Check if Empirica is initialized in this project."""
    project_root = Path(__file__).parent.parent
    empirica_config = project_root / ".empirica" / "config.yaml"

    if empirica_config.exists():
        print("✅ Empirica is initialized in this project")
        return True
    else:
        print("⚠️  Empirica not initialized (run: empirica project-init)")
        return False


def main():
    """Run all checks."""
    print("=" * 60)
    print("Waft Python Version Verification")
    print("=" * 60)
    print()

    python_ok = check_python_version()
    print()

    empirica_ok = check_empirica()
    print()

    empirica_init_ok = check_empirica_initialized()
    print()

    print("=" * 60)
    if python_ok and empirica_ok and empirica_init_ok:
        print("✅ All checks passed!")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
