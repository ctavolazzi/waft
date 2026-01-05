#!/bin/bash
# Reinstall waft in editable mode for development
# This ensures code changes are immediately available

set -e

echo "🔄 Reinstalling waft in editable mode..."
cd "$(dirname "$0")/.."
uv tool install --editable .
echo "✅ Waft reinstalled successfully!"
echo "   Code changes will now be reflected when running 'waft' commands"

