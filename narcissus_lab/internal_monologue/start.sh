#!/bin/bash
# Start TheGuide Homebase
# Usage: ./start.sh [--test]

cd "$(dirname "$0")"

echo "🏠 TheGuide Homebase Launcher"
echo "============================="

if [ "$1" == "--test" ]; then
    echo "🧪 Running browser tests..."
    echo ""
    
    # Start server in background
    uv run python theguide_hello.py &
    SERVER_PID=$!
    sleep 3
    
    # Run tests
    uv run python test_browser.py
    TEST_EXIT=$?
    
    # Stop server
    kill $SERVER_PID 2>/dev/null
    
    exit $TEST_EXIT
else
    echo "🚀 Starting server on http://localhost:8008"
    echo ""
    uv run python theguide_hello.py
fi
