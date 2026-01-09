#!/usr/bin/env python3
"""
Version Bumper Script

Reads pyproject.toml, increments the version, updates the file, and commits.
"""

import tomlkit
import subprocess
import sys
from pathlib import Path


def bump_version(increment_type="minor"):
    """Bump version in pyproject.toml."""
    pyproject_path = Path("pyproject.toml")
    
    if not pyproject_path.exists():
        raise FileNotFoundError("pyproject.toml not found")
    
    # 1. Read the file
    with open(pyproject_path, "r", encoding="utf-8") as f:
        data = tomlkit.load(f)
    
    current_version = data["project"]["version"]
    print(f"Current version: {current_version}")
    
    # 2. Calculate new version
    major, minor, patch = map(int, current_version.split("."))
    
    if increment_type == "minor":
        new_version = f"{major}.{minor + 1}.0"
    elif increment_type == "patch":
        new_version = f"{major}.{minor}.{patch + 1}"
    elif increment_type == "major":
        new_version = f"{major + 1}.0.0"
    else:
        raise ValueError(f"Invalid increment_type: {increment_type}. Use 'major', 'minor', or 'patch'")
        
    print(f"New version:     {new_version}")
    
    # 3. Update the data object
    data["project"]["version"] = new_version
    
    # 4. Write back to file (preserves formatting and comments)
    with open(pyproject_path, "w", encoding="utf-8") as f:
        tomlkit.dump(data, f)
    
    print(f"✅ Updated pyproject.toml")
        
    return new_version


def git_commit(version):
    """Stage and commit the version change."""
    try:
        # Stage the file
        subprocess.run(["git", "add", "pyproject.toml"], check=True, capture_output=True)
        
        # Commit with message
        msg = f"chore: bump version to {version}"
        subprocess.run(["git", "commit", "-m", msg], check=True, capture_output=True)
        print(f"✅ Committed: {msg}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Git operation failed: {e}")
        print("   Version updated in pyproject.toml, but commit was not created.")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Bump version in pyproject.toml")
    parser.add_argument(
        "--type",
        choices=["major", "minor", "patch"],
        default="minor",
        help="Version increment type (default: minor)"
    )
    parser.add_argument(
        "--no-commit",
        action="store_true",
        help="Update version but don't commit"
    )
    
    args = parser.parse_args()
    
    try:
        new_ver = bump_version(increment_type=args.type)
        
        if not args.no_commit:
            git_commit(new_ver)
        else:
            print("⚠️  Version updated but not committed (--no-commit flag)")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
