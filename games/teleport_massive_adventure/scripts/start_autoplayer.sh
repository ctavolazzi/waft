#!/bin/bash
# Quick script to start AutoPlayer
# Usage: ./start_autoplayer.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GAME_DIR="$(dirname "$SCRIPT_DIR")"

echo "🎮 Starting game with AutoPlayer..."

# Check if server is running
if ! curl -s http://localhost:8000/index_v2.html > /dev/null 2>&1; then
    echo "⚠️  Server not running. Starting server..."
    cd "$GAME_DIR"
    python3 -m http.server 8000 > /tmp/game_server.log 2>&1 &
    SERVER_PID=$!
    echo "✅ Server started (PID: $SERVER_PID)"
    sleep 2
fi

# Start AutoPlayer via Node script
cd "$GAME_DIR"
node scripts/start_autoplayer.js
