#!/usr/bin/env python3
"""
Test script for PROJECT LIGHTCONE document generation.

Verifies:
1. All imports work
2. Module can be imported
3. Generators can be called
4. PDFs are created successfully
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("=" * 80)
print("PROJECT LIGHTCONE - Local Test Script")
print("=" * 80)
print()

# Test 1: Import verification
print("Test 1: Import Verification")
print("-" * 80)
try:
    from fpdf import FPDF
    print("✅ fpdf2 imported successfully")
except ImportError as e:
    print(f"❌ fpdf2 import failed: {e}")
    sys.exit(1)

try:
    from waft.foundation import (
        DocumentConfig,
        DocumentEngine,
        SectionHeader,
        TextBlock,
        KeyValueBlock,
        LogBlock,
        WarningBlock,
        SignatureBlock,
    )
    print("✅ DocumentEngine and blocks imported successfully")
except ImportError as e:
    print(f"❌ DocumentEngine import failed: {e}")
    sys.exit(1)

try:
    from src.waft.generate_lightcone_docs import (
        generate_tm_vis_001,
        generate_tm_memo_042,
        generate_tm_eng_004,
        generate_tm_eng_114,
        generate_all_lightcone_docs,
    )
    print("✅ Lightcone generators imported successfully")
except ImportError as e:
    print(f"❌ Generator import failed: {e}")
    sys.exit(1)

print()

# Test 2: Module structure verification
print("Test 2: Module Structure Verification")
print("-" * 80)
import src.waft.generate_lightcone_docs as gen_module

functions = [
    'generate_tm_vis_001',
    'generate_tm_memo_042',
    'generate_tm_eng_004',
    'generate_tm_eng_114',
    'generate_all_lightcone_docs',
]

for func_name in functions:
    if hasattr(gen_module, func_name):
        print(f"✅ {func_name} exists")
    else:
        print(f"❌ {func_name} missing")
        sys.exit(1)

print()

# Test 3: Generate test output directory
print("Test 3: Output Directory Setup")
print("-" * 80)
test_output = project_root / "_work_efforts" / "lightcone_binder" / "test_output"
test_output.mkdir(parents=True, exist_ok=True)
print(f"✅ Test output directory: {test_output}")
print()

# Test 4: Generate one simple document (TM-MEMO-042)
print("Test 4: Generate Test Document (TM-MEMO-042)")
print("-" * 80)
try:
    pdf_path, md_path = generate_tm_memo_042(test_output)
    
    if pdf_path.exists():
        size_kb = pdf_path.stat().st_size / 1024
        print(f"✅ PDF generated: {pdf_path.name} ({size_kb:.1f} KB)")
    else:
        print(f"❌ PDF file not found: {pdf_path}")
        sys.exit(1)
    
    if md_path.exists():
        print(f"✅ Markdown generated: {md_path.name}")
    else:
        print(f"⚠️  Markdown file not found: {md_path}")
    
except Exception as e:
    print(f"❌ Generation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 5: Generate MSDS (TM-ENG-004)
print("Test 5: Generate MSDS Document (TM-ENG-004)")
print("-" * 80)
try:
    pdf_path, md_path = generate_tm_eng_004(test_output)
    
    if pdf_path.exists():
        size_kb = pdf_path.stat().st_size / 1024
        print(f"✅ PDF generated: {pdf_path.name} ({size_kb:.1f} KB)")
    else:
        print(f"❌ PDF file not found: {pdf_path}")
        sys.exit(1)
    
except Exception as e:
    print(f"❌ Generation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 6: Generate Lazarus Protocol (TM-ENG-114)
print("Test 6: Generate Lazarus Protocol (TM-ENG-114)")
print("-" * 80)
try:
    pdf_path, md_path = generate_tm_eng_114(test_output)
    
    if pdf_path.exists():
        size_kb = pdf_path.stat().st_size / 1024
        print(f"✅ PDF generated: {pdf_path.name} ({size_kb:.1f} KB)")
    else:
        print(f"❌ PDF file not found: {pdf_path}")
        sys.exit(1)
    
except Exception as e:
    print(f"❌ Generation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 7: List generated files
print("Test 7: Generated Files Summary")
print("-" * 80)
pdf_dir = test_output / "pdf"
if pdf_dir.exists():
    pdf_files = list(pdf_dir.rglob("*.pdf"))
    print(f"✅ Generated {len(pdf_files)} PDF files:")
    for pdf_file in sorted(pdf_files):
        size_kb = pdf_file.stat().st_size / 1024
        rel_path = pdf_file.relative_to(test_output)
        print(f"   - {rel_path} ({size_kb:.1f} KB)")
else:
    print("⚠️  PDF directory not found")

print()

# Summary
print("=" * 80)
print("TEST SUMMARY")
print("=" * 80)
print("✅ All imports successful")
print("✅ All generator functions exist")
print("✅ Test documents generated successfully")
print()
print(f"📁 Test output location: {test_output}")
print("📄 Generated PDFs are ready for review")
print()
print("Next steps:")
print("1. Open generated PDFs to verify appearance")
print("2. Check style consistency")
print("3. If satisfied, proceed with full generation")
print("=" * 80)
