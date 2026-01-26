#!/bin/bash
# AutoPlayer Test Runner with Screenshots
# Uses Playwright to run the game and capture screenshots

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GAME_DIR="$(dirname "$SCRIPT_DIR")"
SCREENSHOT_DIR="$GAME_DIR/screenshots/autoplayer_test"

echo "🎬 Starting AutoPlayer test with screenshots..."
echo "📂 Game directory: $GAME_DIR"
echo "📸 Screenshot directory: $SCREENSHOT_DIR"

# Create screenshot directory
mkdir -p "$SCREENSHOT_DIR"

# Run the test script
cd "$GAME_DIR"
node scripts/test_autoplayer_with_screenshots.js

# Generate PDF report
if [ -f "$GAME_DIR/scripts/autoplayer_screenshot_report.py" ]; then
    echo "📄 Generating PDF report..."
    python3 "$GAME_DIR/scripts/autoplayer_screenshot_report.py"
    echo "✅ Report generated: $GAME_DIR/AUTOPLAYER_TEST_REPORT.pdf"
fi

echo ""
echo "✅ Test complete!"
echo "📸 Screenshots: $SCREENSHOT_DIR"
echo "📄 Report: $GAME_DIR/AUTOPLAYER_TEST_REPORT.pdf"
