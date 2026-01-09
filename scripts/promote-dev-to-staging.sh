#!/bin/bash
# Promote dev branch to staging (stable dev)
# This script automates the dev → staging promotion process

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DEV_BRANCH="dev"
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
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--dry-run]"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}🚀 Promoting ${DEV_BRANCH} → ${STAGING_BRANCH}${NC}\n"

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

# Step 3: Checkout dev and ensure it's up to date
echo -e "${YELLOW}Step 3: Checking out ${DEV_BRANCH}...${NC}"
git checkout "${DEV_BRANCH}"
git pull origin "${DEV_BRANCH}" || echo -e "${YELLOW}⚠️  No remote ${DEV_BRANCH} branch yet${NC}"
echo -e "${GREEN}✅ On ${DEV_BRANCH} branch${NC}\n"

# Step 4: Run basic validation
echo -e "${YELLOW}Step 4: Running basic validation...${NC}"

# 4.1: Run tests
echo -e "  → Running tests..."
if ! uv run pytest; then
    echo -e "${RED}❌ Tests failed. Fix issues before promoting.${NC}"
    exit 1
fi
echo -e "${GREEN}  ✅ Tests passed${NC}"

# 4.2: Verify project structure
echo -e "  → Verifying project structure..."
if ! waft verify; then
    echo -e "${RED}❌ Project verification failed. Fix issues before promoting.${NC}"
    exit 1
fi
echo -e "${GREEN}  ✅ Project verification passed${NC}\n"

# Step 5: Show what will be merged
echo -e "${YELLOW}Step 5: Reviewing changes to be merged...${NC}"
git checkout "${STAGING_BRANCH}" 2>/dev/null || git checkout -b "${STAGING_BRANCH}" "${MAIN_BRANCH}"
git pull origin "${STAGING_BRANCH}" 2>/dev/null || true

COMMITS_AHEAD=$(git rev-list --count "${STAGING_BRANCH}..${DEV_BRANCH}" 2>/dev/null || echo "0")
if [ "$COMMITS_AHEAD" -eq 0 ]; then
    echo -e "${YELLOW}⚠️  No new commits in ${DEV_BRANCH} compared to ${STAGING_BRANCH}${NC}"
    echo -e "${YELLOW}   Nothing to promote.${NC}"
    exit 0
fi

echo -e "${BLUE}📋 Commits to be merged (${COMMITS_AHEAD} commits):${NC}"
git log --oneline "${STAGING_BRANCH}..${DEV_BRANCH}"
echo ""

# Step 6: Confirm promotion
if [ "$DRY_RUN" = false ]; then
    read -p "Proceed with promotion? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        echo -e "${YELLOW}Promotion cancelled.${NC}"
        exit 0
    fi
fi

# Step 7: Merge dev into staging
echo -e "${YELLOW}Step 6: Merging ${DEV_BRANCH} into ${STAGING_BRANCH}...${NC}"
if [ "$DRY_RUN" = true ]; then
    echo -e "${BLUE}[DRY RUN] Would merge ${DEV_BRANCH} into ${STAGING_BRANCH}${NC}"
else
    git merge --no-ff "${DEV_BRANCH}" -m "chore: promote ${DEV_BRANCH} to ${STAGING_BRANCH}"
    echo -e "${GREEN}✅ Merged ${DEV_BRANCH} into ${STAGING_BRANCH}${NC}\n"
fi

# Step 8: Push to remote
if [ "$DRY_RUN" = false ]; then
    echo -e "${YELLOW}Step 7: Pushing to remote...${NC}"
    read -p "Push ${STAGING_BRANCH} to origin? (yes/no): " push_confirm
    if [ "$push_confirm" = "yes" ]; then
        git push origin "${STAGING_BRANCH}"
        echo -e "${GREEN}✅ Pushed to origin${NC}\n"
    else
        echo -e "${YELLOW}⚠️  Not pushing. You can push manually later.${NC}\n"
    fi
fi

echo -e "${GREEN}🎉 Promotion complete!${NC}"
if [ "$DRY_RUN" = true ]; then
    echo -e "${BLUE}[DRY RUN] No changes were made${NC}"
fi

