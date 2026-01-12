#!/usr/bin/env python3
"""
One-Pager Creator CLI
====================

Command-line interface for creating one-pagers from any content.
"""

import sys
import json
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.one_pager import OnePager, create_one_pager


def parse_args(args: list) -> dict:
    """Parse command line arguments."""
    kwargs = {}
    content = None
    content_type = None
    
    i = 0
    while i < len(args):
        arg = args[i]
        
        if arg.startswith('file:'):
            # File path
            file_path = arg[5:]
            kwargs['content'] = Path(file_path)
            content_type = 'file'
        elif arg.startswith('text:'):
            # Plain text
            content = arg[5:]
            content_type = 'text'
        elif arg.startswith('markdown:'):
            # Markdown
            content = arg[9:]
            content_type = 'markdown'
        elif arg.startswith('json:'):
            # JSON string
            content = json.loads(arg[5:])
            content_type = 'dict'
        elif arg.startswith('dict:'):
            # Dictionary (JSON)
            content = json.loads(arg[5:])
            content_type = 'dict'
        elif arg.startswith('title:'):
            kwargs['title'] = arg[6:]
        elif arg.startswith('subtitle:'):
            kwargs['subtitle'] = arg[9:]
        elif arg.startswith('output:'):
            kwargs['output_path'] = Path(arg[7:])
        elif not arg.startswith('-'):
            # Positional: content
            if content is None:
                content = arg
                content_type = 'text'
        else:
            # Unknown option
            print(f"⚠️ Unknown option: {arg}")
        
        i += 1
    
    if content is None and 'content' not in kwargs:
        return None
    
    if content_type == 'file' and 'content' in kwargs:
        return {'content': kwargs.pop('content'), **kwargs}
    elif content_type == 'markdown':
        return {'content': content, 'content_type': 'markdown', **kwargs}
    elif content_type == 'dict':
        return {'content': content, 'content_type': 'dict', **kwargs}
    else:
        return {'content': content, 'content_type': 'text', **kwargs}


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
        print()
        print("Options:")
        print("  file:path          - Load content from file")
        print("  text:content       - Plain text content")
        print("  markdown:content   - Markdown content")
        print("  json:content       - JSON content (converted to dict)")
        print("  dict:content       - Dictionary content (JSON)")
        print("  title:title        - Document title")
        print("  subtitle:subtitle  - Document subtitle")
        print("  output:path        - Output PDF path")
        sys.exit(1)
    
    parsed = parse_args(sys.argv[1:])
    
    if parsed is None:
        print("❌ Error: No content provided")
        sys.exit(1)
    
    content = parsed.pop('content')
    content_type = parsed.pop('content_type', None)
    
    # Create one-pager based on type
    try:
        if isinstance(content, Path):
            pager = OnePager.from_file(content, **parsed)
        elif content_type == 'markdown':
            pager = OnePager.from_markdown(content, **parsed)
        elif content_type == 'dict':
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
