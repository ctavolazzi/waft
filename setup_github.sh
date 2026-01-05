#!/bin/bash
# Setup script to initialize git and prepare for GitHub

set -e

cd "$(dirname "$0")"

echo "🌊 Initializing Waft repository for GitHub..."

# Initialize git if not already initialized
if [ ! -d .git ]; then
    echo "→ Initializing git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✓ Git repository already initialized"
fi

# Add all files
echo "→ Staging files..."
git add .

# Create initial commit
echo "→ Creating initial commit..."
git commit -m "Initial commit: Waft v0.1.0

- Ambient meta-framework for Python projects
- Orchestrates uv, _pyrite, and crewai
- CLI commands: waft new, waft verify"

echo ""
echo "✅ Repository ready for GitHub!"
echo ""
echo "Next steps:"
echo "  1. Create a new repository on GitHub: https://github.com/new"
echo "     Repository name: waft"
echo "     Owner: ctavolazzi"
echo "     Description: Waft - Ambient, self-modifying Meta-Framework for Python"
echo ""
echo "  2. After creating the repo, run:"
echo "     git remote add origin https://github.com/ctavolazzi/waft.git"
echo "     git branch -M main"
echo "     git push -u origin main"
echo ""

