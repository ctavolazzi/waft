#!/bin/bash
# Start WAFT SvelteKit UI

set -e

# Get project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT/visualizer"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

echo "🎨 Starting WAFT Visualizer UI"
echo "📍 http://localhost:8781"
echo ""

npm run dev
