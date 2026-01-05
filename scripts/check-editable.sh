#!/bin/bash
# Check if waft is installed in editable mode

set -e

WAFT_PATH=$(which waft 2>/dev/null || echo "")
if [ -z "$WAFT_PATH" ]; then
    echo "❌ waft command not found"
    exit 1
fi

# Check if it's a symlink (editable install) or regular file
if [ -L "$WAFT_PATH" ]; then
    echo "✅ waft is installed in editable mode (symlink)"
    echo "   Code changes will be automatically reflected"
    exit 0
else
    echo "⚠️  waft is NOT installed in editable mode"
    echo "   Run: uv tool install --editable ."
    echo "   Or: ./scripts/dev-reinstall.sh"
    exit 1
fi

