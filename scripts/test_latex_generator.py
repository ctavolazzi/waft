#!/usr/bin/env python3
"""
Test LaTeX Generator using WAFT's own testing approach

Tests the LaTeX generator we just built to ensure it works correctly.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.waft.evolution.latex_generator import LaTeXGenerator, generate_latex


def test_latex_generator():
    """Test LaTeX generator functionality."""
    print("🧪 Testing LaTeX Generator\n")

    test_content = """# Test Document

This is a test document to verify LaTeX generation works correctly.

## Features to Test

- Markdown to LaTeX conversion
- LaTeX character escaping
- Multiple sections
- Lists and formatting

### Code Example

```python
def hello():
    print("Hello, World!")
```

## Conclusion

LaTeX generation is working!
"""

    # Test 1: Basic generation
    print("1️⃣ Testing basic LaTeX generation...")
    try:
        latex_path = generate_latex(
            content=test_content,
            title="LaTeX Generator Test",
            document_class="article",
            style="clinical_standard",
            compile_pdf=False,
        )
        print(f"   ✅ Generated: {latex_path}")

        # Verify file exists and has content
        if latex_path.exists():
            content = latex_path.read_text()
            assert "\\documentclass" in content, "Missing documentclass"
            assert "\\begin{document}" in content, "Missing begin document"
            assert "LaTeX Generator Test" in content, "Missing title"
            print("   ✅ LaTeX content validated")
        else:
            raise AssertionError("LaTeX file not created")

    except Exception as e:
        print(f"   ❌ Failed: {e}")
        import traceback

        traceback.print_exc()
        return False

    # Test 2: Character escaping
    print("\n2️⃣ Testing LaTeX character escaping...")
    try:
        special_chars = "# Test with $pecial & Characters %"
        escaped = LaTeXGenerator.from_content(
            content=special_chars, title="Special Characters Test"
        )._escape_latex(special_chars)

        assert "\\#" in escaped, "Hash not escaped"
        assert "\\$" in escaped, "Dollar not escaped"
        assert "\\&" in escaped, "Ampersand not escaped"
        assert "\\%" in escaped, "Percent not escaped"
        print("   ✅ Character escaping works")

    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False

    # Test 3: Integration with ChatDistiller
    print("\n3️⃣ Testing ChatDistiller integration...")
    try:
        generator = LaTeXGenerator.from_content(content=test_content, title="Integration Test")

        assert generator.distilled_chat is not None, "DistilledChat not created"
        assert generator.distilled_chat.title == "Integration Test", "Title mismatch"
        assert len(generator.distilled_chat.ideas) > 0, "No ideas extracted"
        print(f"   ✅ Extracted {len(generator.distilled_chat.ideas)} ideas")

    except Exception as e:
        print(f"   ❌ Failed: {e}")
        import traceback

        traceback.print_exc()
        return False

    # Test 4: StylingGenome integration
    print("\n4️⃣ Testing StylingGenome integration...")
    try:
        generator = LaTeXGenerator.from_content(
            content=test_content, title="Styling Test", style="clinical_standard"
        )

        assert generator.styling_genome is not None, "StylingGenome not created"
        assert generator.styling_genome.genes.font.size_body > 0, "Font size not set"
        assert generator.styling_genome.genes.margin.top > 0, "Margin not set"
        print("   ✅ StylingGenome integrated correctly")

    except Exception as e:
        print(f"   ❌ Failed: {e}")
        import traceback

        traceback.print_exc()
        return False

    # Test 5: Full document generation
    print("\n5️⃣ Testing full document generation...")
    try:
        latex_content = generator.generate()

        assert "\\documentclass" in latex_content, "Missing documentclass"
        assert "\\begin{document}" in latex_content, "Missing begin document"
        assert "\\maketitle" in latex_content, "Missing maketitle"
        assert "\\end{document}" in latex_content, "Missing end document"
        print("   ✅ Full document structure correct")

    except Exception as e:
        print(f"   ❌ Failed: {e}")
        import traceback

        traceback.print_exc()
        return False

    print("\n" + "=" * 60)
    print("✅ All LaTeX generator tests passed!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_latex_generator()
    sys.exit(0 if success else 1)
