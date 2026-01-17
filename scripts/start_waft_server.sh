#!/bin/bash
# Start WAFT API server

set -e

# Get project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Check if we're in a WAFT project
if [ ! -d "_pyrite" ]; then
    echo "❌ Not a WAFT project: _pyrite directory not found"
    exit 1
fi

# Default values
PORT=${1:-8000}
HOST=${2:-localhost}
DEV=${3:-false}

echo "🌊 Starting WAFT API Server"
echo "📍 Port: $PORT"
echo "🌐 Host: $HOST"
echo "🔄 Dev mode: $DEV"
echo ""

# Start server
if [ "$DEV" = "true" ]; then
    waft serve --port "$PORT" --host "$HOST" --dev
else
    waft serve --port "$PORT" --host "$HOST"
fi
