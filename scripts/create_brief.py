#!/usr/bin/env python3
"""
Brief Document Creator CLI
===========================

Command-line interface for creating full binder-ready brief documents
with TM-ARCH-009 style cover page and briefing content.
"""

import sys
import json
from pathlib import Path
from typing import Optional
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.brief import BriefDocument, create_brief


def parse_args(args: list) -> dict:
    """Parse command line arguments."""
    kwargs = {}
    chat_context = {}
    
    i = 0
    while i < len(args):
        arg = args[i]
        
        if arg.startswith('title:'):
            kwargs['title'] = arg[6:]
        elif arg.startswith('doc-id:'):
            kwargs['doc_id'] = arg[7:]
        elif arg.startswith('subtitle:'):
            kwargs['subtitle'] = arg[9:]
        elif arg.startswith('classification:'):
            kwargs['classification'] = arg[16:]
        elif arg.startswith('cover-header:'):
            kwargs['cover_header'] = arg[13:]
        elif arg.startswith('cover-metadata:'):
            try:
                kwargs['cover_metadata'] = json.loads(arg[15:])
            except json.JSONDecodeError:
                print(f"⚠️ Invalid JSON for cover-metadata: {arg[15:]}")
        elif arg.startswith('cover-warning:'):
            try:
                kwargs['cover_warning'] = json.loads(arg[14:])
            except json.JSONDecodeError:
                print(f"⚠️ Invalid JSON for cover-warning: {arg[14:]}")
        elif arg.startswith('cover-signature:'):
            try:
                kwargs['cover_signature'] = json.loads(arg[16:])
            except json.JSONDecodeError:
                print(f"⚠️ Invalid JSON for cover-signature: {arg[16:]}")
        elif arg.startswith('cover-footer:'):
            kwargs['cover_footer'] = arg[13:]
        elif arg.startswith('current-task:'):
            chat_context['current_task'] = arg[13:]
        elif arg.startswith('recent-topics:'):
            try:
                chat_context['recent_topics'] = json.loads(arg[14:])
            except json.JSONDecodeError:
                chat_context['recent_topics'] = [arg[14:]]
        elif arg.startswith('key-decisions:'):
            try:
                chat_context['key_decisions'] = json.loads(arg[14:])
            except json.JSONDecodeError:
                chat_context['key_decisions'] = [arg[14:]]
        elif arg.startswith('next-steps:'):
            try:
                chat_context['next_steps'] = json.loads(arg[11:])
            except json.JSONDecodeError:
                chat_context['next_steps'] = [arg[11:]]
        elif arg.startswith('output:'):
            kwargs['output_path'] = Path(arg[7:])
        elif arg == '--no-status':
            kwargs['include_system_status'] = False
        elif not arg.startswith('-'):
            # Unknown positional
            pass
        else:
            print(f"⚠️ Unknown option: {arg}")
        
        i += 1
    
    if chat_context:
        kwargs['chat_context'] = chat_context
    
    return kwargs


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: create_brief.py [options]")
        print()
        print("Examples:")
        print("  create_brief.py title:'Session Brief'")
        print("  create_brief.py title:'Project Brief' doc-id:'BRIEF-001' cover-header:'TELEPORT MASSIVE'")
        print("  create_brief.py title:'Status Brief' current-task:'Implementing feature X'")
        print()
        print("Options:")
        print("  title:title              - Document title (required)")
        print("  doc-id:id                - Document ID (e.g., 'BRIEF-001', 'TM-ARCH-009')")
        print("  subtitle:subtitle        - Document subtitle")
        print("  classification:cls       - Classification (default: INTERNAL)")
        print("  cover-header:text        - Cover page header (e.g., 'TELEPORT MASSIVE')")
        print("  cover-metadata:json      - Cover metadata (JSON dict)")
        print("  cover-warning:json       - Cover warning (JSON: {'message': '...', 'severity': 'CRITICAL'})")
        print("  cover-signature:json     - Cover signature (JSON: {'role': '...', 'name': '...', 'date': '...'})")
        print("  cover-footer:text        - Cover footer text")
        print("  current-task:text        - Current task for chat context")
        print("  recent-topics:json       - Recent topics (JSON array)")
        print("  key-decisions:json       - Key decisions (JSON array)")
        print("  next-steps:json          - Next steps (JSON array)")
        print("  output:path              - Output PDF path")
        print("  --no-status              - Skip system status gathering")
        print()
        print("Cover Metadata Example:")
        print('  cover-metadata:\'{"OPERATIONAL MANUAL": "09-14", "CODENAME": "W.A.F.T."}\'')
        sys.exit(1)
    
    parsed = parse_args(sys.argv[1:])
    
    if 'title' not in parsed:
        print("❌ Error: Title is required")
        print("   Use: title:'Your Brief Title'")
        sys.exit(1)
    
    title = parsed.pop('title')
    
    try:
        # Create brief
        output = create_brief(title, **parsed)
        
        print("=" * 60)
        print("✅ Brief Document Created!")
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
