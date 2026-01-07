#!/usr/bin/env python3
"""Create v0.0.1 release on GitHub using GitHub CLI."""

import subprocess
import sys

def main():
    """Create the release using gh CLI."""
    release_notes = """# Waft v0.0.1 - Initial Release

🌊 **Waft** - Ambient, self-modifying Meta-Framework for Python

## What's New

This is the initial release of Waft, a meta-framework that orchestrates:
- **Environment** (`uv`) - Python package management
- **Memory** (`_pyrite`) - Persistent project structure
- **Agents** (`crewai`) - AI agent capabilities

## Features

- ✅ `waft new <name>` - Create new projects with full structure
- ✅ `waft verify` - Verify project structure
- ✅ Automatic `_pyrite` folder creation
- ✅ Template generation (Justfile, CI, CrewAI agents)
- ✅ Full `uv` integration

## Installation

```bash
uv tool install waft
```

## Quick Start

```bash
waft new my_project
cd my_project
waft verify
```

## Documentation

See [README.md](https://github.com/ctavolazzi/waft/blob/main/README.md) for full documentation.
"""

    try:
        print("🌊 Creating v0.0.1 release on GitHub...\n")

        # Use gh CLI to create release
        result = subprocess.run(
            [
                "gh", "release", "create", "v0.0.1",
                "--title", "v0.0.1 - Initial Release",
                "--notes", release_notes,
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        print("✅ Release created successfully!")
        print("   View at: https://github.com/ctavolazzi/waft/releases/tag/v0.0.1\n")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create release:")
        print(f"   {e.stderr}")
        print("\n💡 Alternative: Create release manually at:")
        print("   https://github.com/ctavolazzi/waft/releases/new")
        return False
    except FileNotFoundError:
        print("❌ GitHub CLI (gh) not found.")
        print("\n💡 Install it with: brew install gh")
        print("   Or create release manually at:")
        print("   https://github.com/ctavolazzi/waft/releases/new")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)


