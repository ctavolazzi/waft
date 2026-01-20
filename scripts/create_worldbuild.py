#!/usr/bin/env python3
"""
Worldbuilding Document Creator CLI
===================================

Command-line interface for creating worldbuilding documents (fantasy or factual)
with Foundation/TM formatting elements.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.worldbuild import WorldbuildDocument, create_worldbuild_document


def parse_args(args: list) -> dict:
    """Parse command line arguments."""
    kwargs = {}
    content = None
    content_type = None

    i = 0
    while i < len(args):
        arg = args[i]

        if arg.startswith("file:"):
            file_path = Path(arg[5:])
            if file_path.exists():
                content = file_path.read_text()
                content_type = "file"
            else:
                print(f"⚠️ File not found: {file_path}")
        elif arg.startswith("text:"):
            content = arg[5:]
            content_type = "text"
        elif arg.startswith("markdown:"):
            content = arg[9:]
            content_type = "markdown"
        elif arg.startswith("json:"):
            try:
                content = json.loads(arg[5:])
                content_type = "dict"
            except json.JSONDecodeError:
                print(f"⚠️ Invalid JSON: {arg[5:]}")
        elif arg.startswith("title:"):
            kwargs["title"] = arg[6:]
        elif arg.startswith("doc-id:"):
            kwargs["doc_id"] = arg[7:]
        elif arg.startswith("subtitle:"):
            kwargs["subtitle"] = arg[9:]
        elif arg.startswith("classification:"):
            kwargs["classification"] = arg[16:]
        elif arg.startswith("issued-by:"):
            kwargs["issued_by"] = arg[10:]
        elif arg.startswith("output:"):
            kwargs["output_path"] = Path(arg[7:])
        elif not arg.startswith("-"):
            if content is None:
                content = arg
                content_type = "text"
        else:
            print(f"⚠️ Unknown option: {arg}")

        i += 1

    if content is None:
        return None

    return {"content": content, "content_type": content_type, **kwargs}


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: create_worldbuild.py [content] [options]")
        print()
        print("Examples:")
        print(
            "  create_worldbuild.py title:'Character Profile' text:'# Character Name\\n\\nDescription'"
        )
        print(
            "  create_worldbuild.py file:character.md title:'Character Profile' doc-id:'CHAR-001'"
        )
        print(
            "  create_worldbuild.py title:'Location Guide' markdown:'# Location\\n\\nDescription'"
        )
        print()
        print("Options:")
        print("  file:path          - Load content from file")
        print("  text:content       - Plain text content")
        print("  markdown:content   - Markdown content")
        print("  json:content       - JSON structured content")
        print("  title:title        - Document title (required)")
        print("  doc-id:id          - Document ID (e.g., 'WB-001', 'TM-ARCH-009')")
        print("  subtitle:subtitle  - Document subtitle")
        print("  classification:cls - Classification (default: INTERNAL)")
        print("  issued-by:org      - Issuing organization")
        print("  output:path        - Output PDF path")
        sys.exit(1)

    parsed = parse_args(sys.argv[1:])

    if parsed is None or "title" not in parsed:
        print("❌ Error: Title is required")
        print("   Use: title:'Your Document Title'")
        sys.exit(1)

    title = parsed.pop("title")
    content = parsed.pop("content")
    content_type = parsed.pop("content_type", "text")
    output_path = parsed.pop("output_path", None)

    try:
        # Create document
        if content_type == "file" or content_type == "markdown":
            # Treat as markdown
            doc = WorldbuildDocument(title, **parsed)
            doc.add_markdown(content)
            output = doc.generate(output_path)
        elif content_type == "dict":
            # Structured content
            output = create_worldbuild_document(title, content, **parsed)
        else:
            # Plain text
            doc = WorldbuildDocument(title, **parsed)
            doc.add_text(content)
            output = doc.generate(output_path)

        print("=" * 60)
        print("✅ Worldbuilding Document Created!")
        print("=" * 60)
        print(f"📄 Output: {output}")
        print()
        print("Ready for printing and binder storage!")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
