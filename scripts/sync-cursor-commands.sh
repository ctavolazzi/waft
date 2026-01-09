#!/bin/bash
# Sync Cursor Commands to Global Location
#
# This script syncs Cursor commands from the waft project to the global
# Cursor commands directory (~/.cursor/commands/) so they're available
# in all Cursor instances.

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Paths
PROJECT_COMMANDS_DIR="$(cd "$(dirname "$0")/../.cursor/commands" && pwd)"
GLOBAL_COMMANDS_DIR="$HOME/.cursor/commands"

echo -e "${BLUE}🔄 Syncing Cursor Commands${NC}"
echo ""

# Create global commands directory if it doesn't exist
if [ ! -d "$GLOBAL_COMMANDS_DIR" ]; then
    echo -e "${YELLOW}Creating global commands directory...${NC}"
    mkdir -p "$GLOBAL_COMMANDS_DIR"
fi

# Count commands to sync
COMMAND_COUNT=$(find "$PROJECT_COMMANDS_DIR" -name "*.md" -type f | wc -l | tr -d ' ')

echo -e "${BLUE}Source:${NC} $PROJECT_COMMANDS_DIR"
echo -e "${BLUE}Destination:${NC} $GLOBAL_COMMANDS_DIR"
echo -e "${BLUE}Commands found:${NC} $COMMAND_COUNT"
echo ""

# Sync each command file
SYNCED=0
SKIPPED=0

for cmd_file in "$PROJECT_COMMANDS_DIR"/*.md; do
    if [ -f "$cmd_file" ]; then
        cmd_name=$(basename "$cmd_file")
        dest_file="$GLOBAL_COMMANDS_DIR/$cmd_name"
        
        # Check if file exists and is different
        if [ -f "$dest_file" ]; then
            if cmp -s "$cmd_file" "$dest_file"; then
                echo -e "  ${YELLOW}⏭️  $cmd_name${NC} (unchanged)"
                ((SKIPPED++))
            else
                cp "$cmd_file" "$dest_file"
                echo -e "  ${GREEN}✅ $cmd_name${NC} (updated)"
                ((SYNCED++))
            fi
        else
            cp "$cmd_file" "$dest_file"
            echo -e "  ${GREEN}✅ $cmd_name${NC} (new)"
            ((SYNCED++))
        fi
    fi
done

echo ""
echo -e "${GREEN}✨ Sync complete!${NC}"
echo -e "  ${GREEN}Synced:${NC} $SYNCED"
echo -e "  ${YELLOW}Skipped:${NC} $SKIPPED"
echo -e "  ${BLUE}Total:${NC} $COMMAND_COUNT"
echo ""
echo -e "${BLUE}Commands are now available globally in all Cursor instances!${NC}"
