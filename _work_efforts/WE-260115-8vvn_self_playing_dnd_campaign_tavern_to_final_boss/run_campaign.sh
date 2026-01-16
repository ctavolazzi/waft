#!/bin/bash
# Quick runner for the self-playing DnD campaign

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_ROOT"

echo "🎲 Starting Self-Playing DnD Campaign with Electron Window..."
echo ""
echo "💡 An Electron window will open showing the game playing in real-time!"
echo ""

python3 "$SCRIPT_DIR/SELF_PLAYING_CAMPAIGN_ELECTRON.py"

echo ""
echo "✅ Campaign complete! Check the Electron window and output directory for your PDF!"
