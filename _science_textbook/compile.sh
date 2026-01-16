#!/bin/bash
# Compile hypothesis-testing-framework.tex to PDF with enhanced code styling

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

TEX_FILE="hypothesis-testing-framework.tex"
PDF_FILE="hypothesis-testing-framework.pdf"

echo "🔨 Compiling LaTeX document with enhanced code block styling..."
echo ""

# Check if pdflatex is available
if ! command -v pdflatex &> /dev/null; then
    echo "❌ pdflatex not found!"
    echo ""
    echo "Please install LaTeX first:"
    echo "  1. Download MacTeX from: https://www.tug.org/mactex/mactex-download.html"
    echo "  2. Install the .pkg file"
    echo "  3. Restart your terminal or run: eval \"\$(/usr/libexec/path_helper)\""
    echo ""
    exit 1
fi

echo "✅ pdflatex found: $(pdflatex --version | head -1)"
echo ""

# Compile (run twice for references, TOC, etc.)
echo "📝 First pass..."
pdflatex -interaction=nonstopmode "$TEX_FILE" > /dev/null

echo "📝 Second pass (for references)..."
pdflatex -interaction=nonstopmode "$TEX_FILE" > /dev/null

# Clean up auxiliary files
echo "🧹 Cleaning up auxiliary files..."
rm -f *.aux *.log *.out *.toc *.idx *.ilg *.ind 2>/dev/null || true

if [ -f "$PDF_FILE" ]; then
    echo ""
    echo "✅ PDF generated successfully!"
    echo "📄 Output: $PDF_FILE"
    echo ""
    
    # Get file size
    SIZE=$(ls -lh "$PDF_FILE" | awk '{print $5}')
    echo "📊 File size: $SIZE"
    echo ""
    
    # Open PDF
    echo "🔍 Opening PDF..."
    open "$PDF_FILE"
else
    echo "❌ PDF not generated. Check for LaTeX errors above."
    exit 1
fi
