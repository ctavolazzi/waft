#!/usr/bin/env python3
"""
Test One-Pager Tool
===================

Quick test of the one-pager creator with various content types.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.one_pager import OnePager, create_one_pager


def test_markdown():
    """Test with markdown."""
    markdown = """# WAFT One-Pager Test

## Overview
This is a test of the one-pager creator with markdown content.

## Features
- Automatic formatting
- 2-page constraint
- Printer-friendly

## Code Example

```python
def hello():
    print("Hello, World!")
```

## Conclusion
This should create a perfect 2-page document.
"""

    output = create_one_pager(
        markdown,
        title="Markdown One-Pager Test",
        output_path=Path("_work_efforts/one_pagers/test_markdown.pdf"),
    )
    print(f"✅ Generated: {output}")
    return output


def test_dict():
    """Test with dictionary."""
    data = {
        "title": "WAFT Configuration",
        "version": "0.5.0",
        "features": [
            "Self-modification",
            "Evolutionary tracking",
            "Fitness testing",
            "Scientific data collection",
        ],
        "commands": {
            "new": "Create new project",
            "verify": "Check system health",
            "status": "Show current state",
            "spawn": "Create agent variant",
            "eval": "Evaluate fitness",
            "evolve": "Adopt best variant",
        },
        "philosophy": "Physical constellation of crystallized knowledge",
    }

    output = create_one_pager(
        data,
        title="Dictionary One-Pager Test",
        output_path=Path("_work_efforts/one_pagers/test_dict.pdf"),
    )
    print(f"✅ Generated: {output}")
    return output


def test_file():
    """Test with file path."""
    # Use README as test
    readme_path = Path("README.md")
    if readme_path.exists():
        output = OnePager.from_file(
            readme_path,
            title="README One-Pager",
            output_path=Path("_work_efforts/one_pagers/test_readme.pdf"),
        ).generate()
        print(f"✅ Generated: {output}")
        return output
    else:
        print("⚠️ README.md not found, skipping file test")
        return None


def main():
    """Run all tests."""
    print("=" * 60)
    print("🧪 One-Pager Tool Tests")
    print("=" * 60)
    print()

    print("Test 1: Markdown")
    print("-" * 60)
    test_markdown()
    print()

    print("Test 2: Dictionary")
    print("-" * 60)
    test_dict()
    print()

    print("Test 3: File Path")
    print("-" * 60)
    test_file()
    print()

    print("=" * 60)
    print("✅ All tests complete!")
    print("=" * 60)
    print()
    print("Check outputs in _work_efforts/one_pagers/")


if __name__ == "__main__":
    main()
