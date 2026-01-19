#!/bin/bash
# Upload Wiki Content to GitHub Wiki
# GitHub wiki is a separate git repository

set -e

REPO="ctavolazzi/waft"
WIKI_DIR=".wiki-temp"

echo "📚 Uploading Wiki Content to GitHub"
echo "===================================="
echo ""

# Check if wiki files exist
if [ ! -f "WIKI_HOME.md" ]; then
    echo "❌ Wiki files not found. Run from project root."
    exit 1
fi

# Clone wiki repo
if [ -d "$WIKI_DIR" ]; then
    echo "📂 Wiki directory exists, updating..."
    cd "$WIKI_DIR"
    git pull
    cd ..
else
    echo "📂 Cloning wiki repository..."
    git clone "https://github.com/${REPO}.wiki.git" "$WIKI_DIR"
fi

# Copy and rename wiki files
echo "📋 Copying wiki files..."

# Home page
cp WIKI_HOME.md "$WIKI_DIR/Home.md"

# Other pages
cp WIKI_Getting_Started.md "$WIKI_DIR/Getting-Started.md"
cp WIKI_Evolutionary_Iteration_Process.md "$WIKI_DIR/Evolutionary-Iteration-Process.md"
cp WIKI_PDF_Generation_Guide.md "$WIKI_DIR/PDF-Generation-Guide.md"
cp WIKI_PDF_PNG_Conversion.md "$WIKI_DIR/PDF-PNG-Conversion.md"

echo "✅ Wiki files copied"
echo ""

# Commit and push
cd "$WIKI_DIR"

if git diff --quiet && git diff --cached --quiet; then
    echo "ℹ️  No changes to commit"
else
    echo "💾 Committing wiki changes..."
    git add .
    git commit -m "Update wiki content to v0.9.3

- Home page with quick start (updated to v0.9.3)
- Getting Started guide (updated to v0.9.3)
- Evolutionary Iteration Process documentation
- PDF Generation Guide
- PDF/PNG Conversion guide"
    
    echo "🚀 Pushing to GitHub..."
    git push
    
    echo ""
    echo "✅ Wiki content uploaded!"
    echo "   View at: https://github.com/${REPO}/wiki"
fi

cd ..

echo ""
echo "✅ Wiki upload complete!"
