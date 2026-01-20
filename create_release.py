#!/usr/bin/env python3
"""Create v0.0.1 release on GitHub."""

import os
import subprocess
import sys


# Get GitHub token from environment or git config
def get_github_token():
    """Get GitHub token from environment or git config."""
    token = os.getenv("GITHUB_TOKEN")
    if token:
        return token

    # Try to get from gh CLI
    try:
        result = subprocess.run(
            ["gh", "auth", "token"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    return None


def create_release():
    """Create GitHub release using GitHub CLI or API."""
    token = get_github_token()

    if not token:
        print("❌ No GitHub token found. Please set GITHUB_TOKEN or use 'gh auth login'")
        sys.exit(1)

    release_data = {
        "tag_name": "v0.0.1",
        "name": "v0.0.1 - Initial Release",
        "body": """# Waft v0.0.1 - Initial Release

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

---

**Full Changelog**: https://github.com/ctavolazzi/waft/compare/v0.0.1...main
""",
        "draft": False,
        "prerelease": False,
    }

    # Try using gh CLI first (simpler)
    try:
        print("→ Creating release using GitHub CLI...")
        result = subprocess.run(
            [
                "gh",
                "release",
                "create",
                "v0.0.1",
                "--title",
                release_data["name"],
                "--notes",
                release_data["body"],
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        print("✅ Release created successfully!")
        print("   View at: https://github.com/ctavolazzi/waft/releases/tag/v0.0.1")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("→ GitHub CLI not available, trying API...")

    # Fallback to API
    import requests

    url = "https://api.github.com/repos/ctavolazzi/waft/releases"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    response = requests.post(url, headers=headers, json=release_data)

    if response.status_code == 201:
        print("✅ Release created successfully!")
        release = response.json()
        print(f"   View at: {release['html_url']}")
        return True
    else:
        print(f"❌ Failed to create release: {response.status_code}")
        print(f"   Response: {response.text}")
        return False


if __name__ == "__main__":
    create_release()
