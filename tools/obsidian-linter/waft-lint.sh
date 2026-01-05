#!/bin/bash
# Waft Obsidian Linter Wrapper
#
# Wrapper script for pyrite's Obsidian linter.
# This script provides easy access to the linter from the waft project.
#
# Usage:
#   ./tools/obsidian-linter/waft-lint.sh [options]
#
# Options:
#   --scope DIR     Limit to specific directory (default: _work_efforts)
#   --fix           Apply auto-fixes
#   --dry-run       Preview fixes without applying
#   --strict        Enable stricter checking
#   --help          Show this help message

set -e

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PYRITE_LINTER="/Users/ctavolazzi/Code/active/_pyrite/tools/obsidian-linter"

# Check if pyrite linter exists
if [ ! -d "$PYRITE_LINTER" ]; then
    echo "❌ Error: Pyrite linter not found at: $PYRITE_LINTER" >&2
    echo "   Please ensure the pyrite project exists at that location." >&2
    exit 1
fi

# Default scope
SCOPE="_work_efforts"

# Parse arguments
ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        --scope)
            SCOPE="$2"
            ARGS+=("--scope" "$SCOPE")
            shift 2
            ;;
        --fix|--dry-run|--strict|--help)
            ARGS+=("$1")
            shift
            ;;
        *)
            ARGS+=("$1")
            shift
            ;;
    esac
done

# If no scope specified and no other args, add default scope
if [[ ! " ${ARGS[@]} " =~ " --scope " ]]; then
    ARGS+=("--scope" "$SCOPE")
fi

# Change to project root
cd "$PROJECT_ROOT"

# Run the linter
echo "🔍 Running Obsidian linter from pyrite project..."
echo "   Source: $PYRITE_LINTER"
echo "   Scope: $SCOPE"
echo ""

python3 "$PYRITE_LINTER/lint.py" "${ARGS[@]}"

