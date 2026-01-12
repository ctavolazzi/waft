#!/bin/bash
# Prepare v0.5.2 Release
# This script helps prepare and create the GitHub release

set -e

VERSION="0.5.2"
REPO="ctavolazzi/waft"
BRANCH="release/v0.5.2"

echo "🚀 Preparing WAFT v${VERSION} Release"
echo "======================================"
echo ""

# Check we're on the right branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "$BRANCH" ]; then
    echo "⚠️  Warning: Not on $BRANCH branch (currently on $CURRENT_BRANCH)"
    echo "   Run: git checkout $BRANCH"
    exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  Warning: Uncommitted changes detected"
    echo "   Commit or stash changes before creating release"
    exit 1
fi

echo "✅ Branch: $CURRENT_BRANCH"
echo "✅ Version: $VERSION"
echo ""

# Read release notes
if [ -f "RELEASE_NOTES_v${VERSION}.md" ]; then
    echo "📄 Release notes found: RELEASE_NOTES_v${VERSION}.md"
else
    echo "❌ Release notes not found: RELEASE_NOTES_v${VERSION}.md"
    exit 1
fi

# Check version consistency
PYPROJECT_VERSION=$(grep '^version = ' pyproject.toml | cut -d'"' -f2)
INIT_VERSION=$(grep '__version__ = ' src/waft/__init__.py | cut -d'"' -f2)

if [ "$PYPROJECT_VERSION" != "$VERSION" ] || [ "$INIT_VERSION" != "$VERSION" ]; then
    echo "❌ Version mismatch:"
    echo "   pyproject.toml: $PYPROJECT_VERSION"
    echo "   __init__.py: $INIT_VERSION"
    echo "   Expected: $VERSION"
    exit 1
fi

echo "✅ Version consistency check passed"
echo ""

# Generate release notes summary
echo "📋 Release Summary:"
echo "-------------------"
head -20 "RELEASE_NOTES_v${VERSION}.md" | grep -E "^##|^###|^- " | head -10
echo ""

# Check if PR exists
echo "🔍 Checking for PR..."
PR_URL=$(gh pr list --head "$BRANCH" --json url --jq '.[0].url' 2>/dev/null || echo "")
if [ -n "$PR_URL" ]; then
    echo "✅ PR found: $PR_URL"
else
    echo "⚠️  No PR found for $BRANCH"
    echo "   Create PR: gh pr create --title 'Release v${VERSION}' --body-file RELEASE_NOTES_v${VERSION}.md"
fi
echo ""

# Wiki upload instructions
echo "📚 Wiki Upload Instructions:"
echo "-------------------------"
echo "GitHub wiki is a separate git repository. To upload wiki content:"
echo ""
echo "1. Clone wiki repo:"
echo "   git clone https://github.com/$REPO.wiki.git"
echo ""
echo "2. Copy wiki files:"
echo "   cp WIKI_*.md <wiki-repo>/"
echo "   # Rename as needed (e.g., WIKI_HOME.md -> Home.md)"
echo ""
echo "3. Commit and push:"
echo "   cd <wiki-repo>"
echo "   git add ."
echo "   git commit -m 'Add v${VERSION} wiki content'"
echo "   git push"
echo ""

# Release creation instructions
echo "🎯 Next Steps:"
echo "-------------"
echo "1. Merge PR: $PR_URL"
echo "2. Create GitHub release:"
echo "   gh release create v${VERSION} \\"
echo "     --title 'v${VERSION}: Evolutionary Iteration Process' \\"
echo "     --notes-file RELEASE_NOTES_v${VERSION}.md \\"
echo "     --target main"
echo ""
echo "3. Upload wiki content (see instructions above)"
echo ""

echo "✅ Release preparation complete!"
echo ""
echo "📝 Files ready:"
echo "   - RELEASE_NOTES_v${VERSION}.md"
echo "   - WIKI_*.md (wiki content)"
echo "   - CHANGELOG.md (updated)"
echo ""
