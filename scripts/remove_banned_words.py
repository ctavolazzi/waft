#!/usr/bin/env python3
"""
Remove Banned Words Tool

Scans the codebase for banned words and replaces them.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.waft.core.banned_words import BannedWordsSystem

def main():
    """Main function to scan and replace banned words."""
    print("🔍 Scanning for banned words...")
    print()
    
    # Initialize banned words system
    ban_system = BannedWordsSystem(project_root)
    
    # Scan directory
    violations = ban_system.scan_directory(project_root)
    
    if not violations:
        print("✅ No banned words found!")
        return
    
    print(f"⚠️  Found {len(violations)} violations:")
    print()
    
    # Group by file
    by_file = {}
    for v in violations:
        if "error" in v:
            print(f"❌ Error in {v.get('file', 'unknown')}: {v['error']}")
            continue
        
        file_path = v.get("file", "unknown")
        if file_path not in by_file:
            by_file[file_path] = []
        by_file[file_path].append(v)
    
    # Show violations
    for file_path, file_violations in by_file.items():
        print(f"📄 {file_path}:")
        for v in file_violations:
            print(f"   Line {v['line']}: '{v['word']}' → '{v['replacement']}'")
            print(f"   Context: {v['context'][:80]}...")
        print()
    
    # Ask for confirmation
    response = input(f"Replace all {len(violations)} instances? (yes/no): ")
    if response.lower() != "yes":
        print("❌ Cancelled.")
        return
    
    # Replace in files
    print()
    print("🔄 Replacing banned words...")
    
    files_modified = set()
    for file_path in by_file.keys():
        path = Path(file_path)
        if ban_system.replace_in_file(path):
            files_modified.add(file_path)
            print(f"✅ Updated: {file_path}")
    
    print()
    print(f"✅ Done! Modified {len(files_modified)} files.")
    
    # Verify
    print()
    print("🔍 Verifying replacements...")
    remaining = ban_system.scan_directory(project_root)
    if remaining:
        print(f"⚠️  Still found {len(remaining)} violations:")
        for v in remaining[:10]:  # Show first 10
            print(f"   {v.get('file', 'unknown')}: Line {v.get('line', '?')}")
    else:
        print("✅ All banned words removed!")

if __name__ == "__main__":
    main()
