#!/usr/bin/env python3
"""
PDF Tracing Utility

Trace PDF files to find their current location and full history.
Shows where PDFs are stored, where they've been moved, and provides
query capabilities.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.utils import StorageRegistry, trace_pdf


def main():
    """Main CLI for PDF tracing."""
    import argparse

    parser = argparse.ArgumentParser(description="Trace PDF files - find locations and history")
    parser.add_argument("pdf_path", nargs="?", help="PDF path or filename to trace")
    parser.add_argument(
        "--project-path", type=Path, help="Project root path (default: current directory)"
    )
    parser.add_argument("--list", action="store_true", help="List all PDFs in registry")
    parser.add_argument("--search", type=str, help="Search for PDFs matching pattern")
    parser.add_argument(
        "--external-only", action="store_true", help="Show only PDFs on external drive"
    )
    parser.add_argument("--stats", action="store_true", help="Show storage statistics")
    parser.add_argument("--audit", action="store_true", help="Show audit log")
    parser.add_argument("--limit", type=int, default=50, help="Limit results (default: 50)")

    args = parser.parse_args()

    project_path = args.project_path or Path.cwd()
    registry = StorageRegistry(project_path)

    # Show stats
    if args.stats:
        stats = registry.get_storage_stats()
        print("\n📊 Storage Statistics")
        print("=" * 50)
        print(f"Total Content: {stats['total_content']}")
        print(f"Total PDFs: {stats['total_pdfs']}")
        print(f"Core Content: {stats['core_content']}")
        print(f"Augmented Content: {stats['augmented_content']}")
        print(f"PDFs on External Drive: {stats['pdfs_on_external']}")
        print(f"PDFs Local: {stats['pdfs_local']}")
        print(f"External Drive Available: {stats['external_drive_available']}")
        print()
        return

    # Show audit log
    if args.audit:
        entries = registry.query_audit_log(limit=args.limit)
        print(f"\n📋 Audit Log (last {len(entries)} entries)")
        print("=" * 50)
        for entry in entries:
            timestamp = entry.get("timestamp", "")
            operation = entry.get("operation", "")
            content_path = entry.get("content_path", "")
            print(f"{timestamp} | {operation:8} | {content_path}")
            if operation == "moved":
                print(f"  From: {entry.get('old_location', '')}")
                print(f"  To:   {entry.get('new_location', '')}")
        print()
        return

    # List all PDFs
    if args.list or args.search or args.external_only:
        filters = {}
        if args.search:
            filters["pattern"] = args.search
        if args.external_only:
            filters["content_type"] = "augmented"

        pdfs = registry.find_pdfs(**filters, limit=args.limit)

        print(f"\n📄 PDFs in Registry ({len(pdfs)} found)")
        print("=" * 50)
        for pdf in pdfs:
            if not pdf.get("found"):
                continue
            print(f"\n{pdf['pdf_path']}")
            print(f"  Location: {pdf['current_location']}")
            print(f"  Type: {pdf['content_type']}")
            print(f"  Created: {pdf.get('created_at', 'unknown')}")
            if pdf.get("move_count", 0) > 0:
                print(f"  Moved: {pdf['move_count']} time(s)")
            if pdf.get("all_locations"):
                print(f"  All Locations ({len(pdf['all_locations'])}):")
                for loc in pdf["all_locations"][:3]:  # Show first 3
                    print(f"    - {loc}")
                if len(pdf["all_locations"]) > 3:
                    print(f"    ... and {len(pdf['all_locations']) - 3} more")
        print()
        return

    # Trace specific PDF
    if args.pdf_path:
        trace = trace_pdf(args.pdf_path, project_path)

        if not trace.get("found"):
            print(f"\n❌ PDF not found: {args.pdf_path}")
            print("\nTry:")
            print("  - Using just the filename")
            print("  - Using --list to see all PDFs")
            print("  - Using --search to find similar PDFs")
            return

        print(f"\n🔍 PDF Trace: {trace['pdf_path']}")
        print("=" * 50)
        print(f"Current Location: {trace['current_location']}")
        print(f"Content Type: {trace['content_type']}")
        print(f"Created: {trace.get('created_at', 'unknown')}")
        print(f"Last Operation: {trace.get('last_operation', 'unknown')}")
        print(f"Move Count: {trace.get('move_count', 0)}")

        if trace.get("all_locations"):
            print(f"\nAll Locations ({len(trace['all_locations'])}):")
            for i, loc in enumerate(trace["all_locations"], 1):
                marker = "→" if loc == trace["current_location"] else " "
                print(f"  {marker} {i}. {loc}")

        if trace.get("history"):
            print(f"\nHistory ({len(trace['history'])} operations):")
            for i, entry in enumerate(trace["history"][-10:], 1):  # Last 10
                print(
                    f"  {i}. {entry.get('operation', 'unknown')} at {entry.get('timestamp', 'unknown')}"
                )
                if entry.get("location"):
                    print(f"     Location: {entry['location']}")
                if entry.get("old_location"):
                    print(f"     From: {entry['old_location']}")
                if entry.get("new_location"):
                    print(f"     To: {entry['new_location']}")

        print()
        return

    # No arguments - show help
    parser.print_help()
    print("\nExamples:")
    print("  python scripts/trace_pdf.py session_recap_20260115.pdf")
    print("  python scripts/trace_pdf.py --list")
    print("  python scripts/trace_pdf.py --search session")
    print("  python scripts/trace_pdf.py --external-only")
    print("  python scripts/trace_pdf.py --stats")
    print("  python scripts/trace_pdf.py --audit")


if __name__ == "__main__":
    main()
