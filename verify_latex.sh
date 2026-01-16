#!/bin/bash
# Verify LaTeX Installation and Test Plans Report Generation

echo "🔍 Verifying LaTeX Installation..."
echo ""

# Check if pdflatex is available
if command -v pdflatex &> /dev/null; then
    echo "✅ pdflatex found!"
    pdflatex --version | head -1
    echo ""
else
    echo "❌ pdflatex not found in PATH"
    echo ""
    echo "If you just installed MacTeX, you may need to:"
    echo "1. Restart your terminal, OR"
    echo "2. Run: eval \"\$(/usr/libexec/path_helper)\""
    echo ""
    echo "MacTeX installs to: /usr/local/texlive/2025"
    echo "PATH should include: /Library/TeX/texbin"
    echo ""
    exit 1
fi

# Check other common LaTeX tools
echo "📦 Checking LaTeX tools..."
for tool in latex xelatex lualatex; do
    if command -v $tool &> /dev/null; then
        echo "  ✅ $tool found"
    else
        echo "  ⚠️  $tool not found (may not be needed)"
    fi
done

echo ""
echo "🧪 Testing LaTeX compilation..."
cat > /tmp/test_latex.tex << 'TEXEOF'
\documentclass{article}
\usepackage[utf8]{inputenc}
\begin{document}
\title{LaTeX Test}
\author{W.A.F.T. System}
\maketitle

Hello, LaTeX! This is a test document.

If you can read this, LaTeX is working correctly.
\end{document}
TEXEOF

cd /tmp
if pdflatex -interaction=nonstopmode test_latex.tex > /dev/null 2>&1; then
    if [ -f test_latex.pdf ]; then
        echo "✅ LaTeX compilation test successful!"
        echo "   Test PDF created at: /tmp/test_latex.pdf"
        rm -f test_latex.aux test_latex.log test_latex.tex
        # Keep PDF for user to verify
    else
        echo "⚠️  Compilation ran but PDF not found"
    fi
else
    echo "❌ LaTeX compilation test failed"
    echo "   Check /tmp/test_latex.log for errors"
fi

echo ""
echo "📊 Ready to generate Plans Reports with LaTeX!"
echo ""
echo "To generate the Plans Report, run:"
echo "  python3 scripts/create_plans_report.py"
echo ""
