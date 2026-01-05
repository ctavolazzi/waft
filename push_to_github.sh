#!/bin/bash
# Push Waft repository to GitHub

set -e

cd "$(dirname "$0")"

echo "🌊 Preparing Waft for GitHub push..."

# Initialize git if not already initialized
if [ ! -d .git ]; then
    echo "→ Initializing git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✓ Git repository already initialized"
fi

# Check if remote exists
if git remote get-url origin >/dev/null 2>&1; then
    echo "✓ Remote 'origin' already configured"
    REMOTE_URL=$(git remote get-url origin)
    echo "  URL: $REMOTE_URL"
else
    echo "→ Adding GitHub remote..."
    git remote add origin https://github.com/ctavolazzi/waft.git
    echo "✅ Remote added"
fi

# Add all files
echo "→ Staging files..."
git add .

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo "✓ No changes to commit"
else
    echo "→ Creating commit..."
    git commit -m "Initial commit: Waft v0.1.0

- Ambient meta-framework for Python projects
- Orchestrates uv, _pyrite, and crewai
- CLI commands: waft new, waft verify
- Full project scaffolding with templates"
    echo "✅ Commit created"
fi

# Set main branch
git branch -M main 2>/dev/null || true

# Push to GitHub
echo ""
echo "→ Pushing to GitHub..."
echo "  Repository: https://github.com/ctavolazzi/waft"
echo ""
git push -u origin main

echo ""
echo "✅ Successfully pushed to GitHub!"
echo "   View at: https://github.com/ctavolazzi/waft"
echo ""

