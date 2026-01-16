# Installing LaTeX to Compile the Textbook

To compile the hypothesis testing framework textbook to PDF, you need a LaTeX distribution installed.

## Quick Install (macOS)

```bash
# Install MacTeX (full LaTeX distribution)
brew install --cask mactex

# Or install BasicTeX (smaller, ~100MB)
brew install --cask basictex

# If using BasicTeX, install additional packages:
sudo tlmgr update --self
sudo tlmgr install collection-latexextra
```

## Quick Install (Linux)

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install texlive-full

# Or minimal installation
sudo apt-get install texlive-latex-base texlive-latex-extra
```

## Quick Install (Windows)

1. Download and install [MiKTeX](https://miktex.org/download) or [TeX Live](https://www.tug.org/texlive/)
2. Follow the installer instructions
3. Restart your terminal/command prompt

## After Installation

Once LaTeX is installed, compile the textbook:

```bash
cd _science_textbook
python3 compile_textbook.py
```

Or use the Makefile:

```bash
cd _science_textbook
make
```

## Alternative: Online LaTeX Compiler

If you don't want to install LaTeX locally, you can use:

- [Overleaf](https://www.overleaf.com/) - Online LaTeX editor
  1. Create a free account
  2. Create a new project
  3. Copy the contents of `hypothesis-testing-framework.tex`
  4. Compile online

- [ShareLaTeX](https://www.sharelatex.com/) - Similar to Overleaf

## Current Status

✅ LaTeX source file created: `hypothesis-testing-framework.tex`
❌ LaTeX compiler not installed
📝 Ready to compile once LaTeX is installed
