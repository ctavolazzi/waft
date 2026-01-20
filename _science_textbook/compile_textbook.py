#!/usr/bin/env python3
"""
Compile the hypothesis testing framework textbook to PDF.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

try:
    from src.waft.templates.latex.compiler import LaTeXCompiler
except ImportError:
    # Try alternative import
    import importlib.util

    compiler_path = project_root / "src" / "waft" / "templates" / "latex" / "compiler.py"
    spec = importlib.util.spec_from_file_location("compiler", compiler_path)
    compiler_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(compiler_module)
    LaTeXCompiler = compiler_module.LaTeXCompiler


def main():
    """Compile the textbook LaTeX file to PDF."""
    tex_file = Path(__file__).parent / "hypothesis-testing-framework.tex"
    output_pdf = Path(__file__).parent / "hypothesis-testing-framework.pdf"

    print("📚 Compiling textbook...")
    print(f"   Source: {tex_file}")
    print(f"   Output: {output_pdf}")
    print()

    try:
        compiler = LaTeXCompiler(compiler="pdflatex")
        pdf_path = compiler.compile_file(
            tex_file,
            output_pdf,
            runs=2,  # Two runs for TOC and references
        )
        print("✅ PDF generated successfully!")
        print(f"   Location: {pdf_path}")
        print()
        print("📖 Opening PDF...")

        # Open PDF
        import platform
        import subprocess

        if platform.system() == "Darwin":  # macOS
            subprocess.run(["open", str(pdf_path)])
        elif platform.system() == "Windows":
            subprocess.run(["start", str(pdf_path)], shell=True)
        else:  # Linux
            subprocess.run(["xdg-open", str(pdf_path)])

    except RuntimeError as e:
        print("❌ LaTeX compilation failed:")
        print(f"   {e}")
        print()
        print("💡 To install LaTeX:")
        print("   macOS: brew install --cask mactex")
        print("   Linux: sudo apt-get install texlive-full")
        print("   Windows: Install MiKTeX or TeX Live")
        print()
        print("   Or use the Makefile:")
        print("   cd _science_textbook && make")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
