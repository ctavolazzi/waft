#!/bin/bash
# LaTeX Installation Script for macOS
# Run this script to install BasicTeX and required packages

set -e

echo "🔧 Installing BasicTeX via Homebrew..."
brew install --cask basictex

echo ""
echo "✅ BasicTeX installed!"
echo ""
echo "📝 Updating PATH..."
eval "$(/usr/libexec/path_helper)"

echo ""
echo "🔍 Verifying installation..."
if command -v pdflatex &> /dev/null; then
    echo "✅ pdflatex found!"
    pdflatex --version | head -1
else
    echo "⚠️  pdflatex not in PATH yet. Please restart your terminal or run:"
    echo "   eval \"\$(/usr/libexec/path_helper)\""
    exit 1
fi

echo ""
echo "📦 Installing recommended LaTeX packages..."
echo "   (This may take a few minutes and requires sudo password)"
sudo tlmgr update --self
sudo tlmgr install collection-fontsrecommended collection-latexextra

echo ""
echo "✅ LaTeX installation complete!"
echo ""
echo "🧪 Testing with a simple document..."
cat > /tmp/test_latex.tex << 'TEXEOF'
\documentclass{article}
\begin{document}
Hello, LaTeX!
\end{document}
TEXEOF

cd /tmp
pdflatex -interaction=nonstopmode test_latex.tex > /dev/null 2>&1

if [ -f test_latex.pdf ]; then
    echo "✅ LaTeX compilation test successful!"
    rm -f test_latex.*
else
    echo "⚠️  LaTeX compilation test failed. Check the output above."
fi

echo ""
echo "🎉 Ready to generate Plans Reports with LaTeX!"
