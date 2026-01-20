#!/usr/bin/env python3
"""
One-Pager Creator CLI
====================

Command-line interface for creating one-pagers from any content.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.one_pager import OnePager


def parse_args(args: list) -> dict:
    """Parse command line arguments."""
    kwargs = {}
    content = None
    content_type = None
    is_briefing = False

    i = 0
    while i < len(args):
        arg = args[i]

        if arg == "--briefing" or arg == "-b":
            # Briefing mode
            is_briefing = True
        elif arg.startswith("file:"):
            # File path
            file_path = arg[5:]
            kwargs["content"] = Path(file_path)
            content_type = "file"
        elif arg.startswith("text:"):
            # Plain text
            content = arg[5:]
            content_type = "text"
        elif arg.startswith("markdown:"):
            # Markdown
            content = arg[9:]
            content_type = "markdown"
        elif arg.startswith("json:"):
            # JSON string
            content = json.loads(arg[5:])
            content_type = "dict"
        elif arg.startswith("dict:"):
            # Dictionary (JSON)
            content = json.loads(arg[5:])
            content_type = "dict"
        elif arg.startswith("title:"):
            kwargs["title"] = arg[6:]
        elif arg.startswith("subtitle:"):
            kwargs["subtitle"] = arg[9:]
        elif arg.startswith("output:"):
            kwargs["output_path"] = Path(arg[7:])
        elif arg.startswith("series:"):
            kwargs["series"] = arg[7:]
        elif arg.startswith("number:"):
            kwargs["number"] = arg[7:]
        elif arg.startswith("classification:"):
            kwargs["classification"] = arg[16:]
        elif arg.startswith("issued-by:"):
            kwargs["issued_by"] = arg[10:]
        elif not arg.startswith("-"):
            # Positional: content
            if content is None:
                content = arg
                content_type = "text"
        else:
            # Unknown option
            print(f"⚠️ Unknown option: {arg}")

        i += 1

    # If briefing mode, return briefing flag
    if is_briefing:
        return {"briefing": True, **kwargs}

    if content is None and "content" not in kwargs:
        return None

    if content_type == "file" and "content" in kwargs:
        return {"content": kwargs.pop("content"), **kwargs}
    elif content_type == "markdown":
        return {"content": content, "content_type": "markdown", **kwargs}
    elif content_type == "dict":
        return {"content": content, "content_type": "dict", **kwargs}
    else:
        return {"content": content, "content_type": "text", **kwargs}


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: create_one_pager.py [content] [options]")
        print()
        print("Examples:")
        print("  create_one_pager.py file:README.md title:'README One-Pager'")
        print("  create_one_pager.py text:'# Title\\n\\nContent' title:'My Doc'")
        print("  create_one_pager.py markdown:'# Title\\n\\nContent'")
        print("  create_one_pager.py json:'{\"key\": \"value\"}' title:'Config'")
        print("  create_one_pager.py --briefing title:'Session Briefing'")
        print()
        print("Options:")
        print("  --briefing, -b     - Generate briefing document (system status + chat context)")
        print("  file:path          - Load content from file")
        print("  text:content       - Plain text content")
        print("  markdown:content   - Markdown content")
        print("  json:content       - JSON content (converted to dict)")
        print("  dict:content       - Dictionary content (JSON)")
        print("  title:title        - Document title")
        print("  subtitle:subtitle  - Document subtitle")
        print("  output:path        - Output PDF path")
        print("  series:name        - Briefing series name (default: BRIEFING)")
        print("  number:num         - Briefing number (default: BG-YYYYMMDD)")
        print("  classification:cls - Classification (default: INTERNAL)")
        print("  issued-by:org      - Issuing organization (default: WAFT System)")
        sys.exit(1)

    parsed = parse_args(sys.argv[1:])

    if parsed is None:
        print("❌ Error: No content provided")
        sys.exit(1)

    # Create one-pager based on type
    try:
        # Check if briefing mode
        if parsed.get("briefing", False):
            # Briefing mode - gather chat context from environment or defaults
            chat_context = {}
            # Try to get from environment or use defaults
            # In a real implementation, this could read from conversation history
            pager = OnePager.from_briefing(
                chat_context=chat_context,
                include_system_status=True,
                **{k: v for k, v in parsed.items() if k != "briefing"},
            )
        else:
            content = parsed.pop("content")
            content_type = parsed.pop("content_type", None)

            if isinstance(content, Path):
                pager = OnePager.from_file(content, **parsed)
            elif content_type == "markdown":
                pager = OnePager.from_markdown(content, **parsed)
            elif content_type == "dict":
                pager = OnePager.from_dict(content, **parsed)
            else:
                pager = OnePager.from_text(content, **parsed)

        output = pager.generate()

        # Check page count
        from pypdf import PdfReader

        reader = PdfReader(str(output))
        page_count = len(reader.pages)

        print("=" * 60)
        print("✅ One-Pager Created!")
        print("=" * 60)
        print(f"📄 Output: {output}")
        print(f"📊 Pages: {page_count} (target: 2)")

        if page_count == 2:
            print("✅ Perfect 2-page document!")
        else:
            print(f"⚠️ Generated {page_count} pages (expected 2)")

        print()
        print("Ready for printing and binder storage!")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
