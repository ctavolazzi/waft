#!/bin/bash
# Open the campaign display in Electron or browser

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
HTML_FILE="$SCRIPT_DIR/output/campaign_display.html"

if [ ! -f "$HTML_FILE" ]; then
    echo "⚠️  Campaign HTML not found. Run the campaign first:"
    echo "   ./run_campaign_electron.sh"
    exit 1
fi

echo "🎲 Opening campaign display..."

# Try Electron first
if command -v electron &> /dev/null || command -v npx &> /dev/null; then
    echo "   Using Electron..."
    npx electron "$HTML_FILE" 2>/dev/null || electron "$HTML_FILE" 2>/dev/null || {
        echo "   Falling back to browser..."
        open "$HTML_FILE"
    }
else
    echo "   Opening in browser..."
    open "$HTML_FILE"
fi

echo "✅ Window opened!"
