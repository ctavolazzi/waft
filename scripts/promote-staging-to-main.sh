#!/bin/bash
# Promote staging branch to main (production release)
# This script automates the staging → main promotion process with validation

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
STAGING_BRANCH="staging"
MAIN_BRANCH="main"
DRY_RUN=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --version)
            VERSION="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--dry-run] [--version VERSION]"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}🚀 Promoting ${STAGING_BRANCH} → ${MAIN_BRANCH}${NC}\n"

# Step 1: Ensure we're on a clean state
echo -e "${YELLOW}Step 1: Checking git status...${NC}"
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${RED}❌ Working directory is not clean. Please commit or stash changes.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Working directory is clean${NC}\n"

# Step 2: Fetch latest from remote
echo -e "${YELLOW}Step 2: Fetching latest from remote...${NC}"
git fetch origin
echo -e "${GREEN}✅ Fetched latest changes${NC}\n"

# Step 3: Checkout staging and ensure it's up to date
echo -e "${YELLOW}Step 3: Checking out ${STAGING_BRANCH}...${NC}"
git checkout "${STAGING_BRANCH}"
git pull origin "${STAGING_BRANCH}" || echo -e "${YELLOW}⚠️  No remote ${STAGING_BRANCH} branch yet${NC}"
echo -e "${GREEN}✅ On ${STAGING_BRANCH} branch${NC}\n"

# Step 4: Run validation checks
echo -e "${YELLOW}Step 4: Running validation checks...${NC}"

# 4.1: Run tests
echo -e "  → Running tests..."
if ! uv run pytest; then
    echo -e "${RED}❌ Tests failed. Fix issues before promoting.${NC}"
    exit 1
fi
echo -e "${GREEN}  ✅ Tests passed${NC}"

# 4.2: Run linting
echo -e "  → Running linting..."
if ! uv run ruff check .; then
    echo -e "${RED}❌ Linting failed. Fix issues before promoting.${NC}"
    exit 1
fi
echo -e "${GREEN}  ✅ Linting passed${NC}"

# 4.3: Check formatting
echo -e "  → Checking formatting..."
if ! uv run ruff format --check .; then
    echo -e "${RED}❌ Formatting check failed. Run 'ruff format .' to fix.${NC}"
    exit 1
fi
echo -e "${GREEN}  ✅ Formatting check passed${NC}"

# 4.4: Verify project structure
echo -e "  → Verifying project structure..."
if ! waft verify; then
    echo -e "${RED}❌ Project verification failed. Fix issues before promoting.${NC}"
    exit 1
fi
echo -e "${GREEN}  ✅ Project verification passed${NC}\n"

# Step 5: Show what will be merged
echo -e "${YELLOW}Step 5: Reviewing changes to be merged...${NC}"
git checkout "${MAIN_BRANCH}"
git pull origin "${MAIN_BRANCH}"

COMMITS_AHEAD=$(git rev-list --count "${MAIN_BRANCH}..${STAGING_BRANCH}")
if [ "$COMMITS_AHEAD" -eq 0 ]; then
    echo -e "${YELLOW}⚠️  No new commits in ${STAGING_BRANCH} compared to ${MAIN_BRANCH}${NC}"
    echo -e "${YELLOW}   Nothing to promote.${NC}"
    exit 0
fi

echo -e "${BLUE}📋 Commits to be merged (${COMMITS_AHEAD} commits):${NC}"
git log --oneline "${MAIN_BRANCH}..${STAGING_BRANCH}"
echo ""

# Step 6: Confirm promotion
if [ "$DRY_RUN" = false ]; then
    read -p "Proceed with promotion? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        echo -e "${YELLOW}Promotion cancelled.${NC}"
        exit 0
    fi
fi

# Step 7: Merge staging into main
echo -e "${YELLOW}Step 6: Merging ${STAGING_BRANCH} into ${MAIN_BRANCH}...${NC}"
if [ "$DRY_RUN" = true ]; then
    echo -e "${BLUE}[DRY RUN] Would merge ${STAGING_BRANCH} into ${MAIN_BRANCH}${NC}"
else
    git merge --no-ff "${STAGING_BRANCH}" -m "chore: promote ${STAGING_BRANCH} to ${MAIN_BRANCH}"
    echo -e "${GREEN}✅ Merged ${STAGING_BRANCH} into ${MAIN_BRANCH}${NC}\n"
fi

# Step 8: Tag release (if version provided)
if [ -n "$VERSION" ] && [ "$DRY_RUN" = false ]; then
    echo -e "${YELLOW}Step 7: Creating release tag ${VERSION}...${NC}"
    git tag -a "${VERSION}" -m "Release ${VERSION}"
    echo -e "${GREEN}✅ Created tag ${VERSION}${NC}\n"
fi

# Step 9: Push to remote
if [ "$DRY_RUN" = false ]; then
    echo -e "${YELLOW}Step 8: Pushing to remote...${NC}"
    read -p "Push ${MAIN_BRANCH} to origin? (yes/no): " push_confirm
    if [ "$push_confirm" = "yes" ]; then
        git push origin "${MAIN_BRANCH}"
        if [ -n "$VERSION" ]; then
            git push origin "${VERSION}"
        fi
        echo -e "${GREEN}✅ Pushed to origin${NC}\n"
    else
        echo -e "${YELLOW}⚠️  Not pushing. You can push manually later.${NC}\n"
    fi
fi

echo -e "${GREEN}🎉 Promotion complete!${NC}"
if [ "$DRY_RUN" = true ]; then
    echo -e "${BLUE}[DRY RUN] No changes were made${NC}"
fi

