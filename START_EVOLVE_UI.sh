#!/bin/bash
# Quick start script to see the Evolve UI Monitor

echo "🎨 Starting Evolve UI Monitor..."
echo ""

# Check if backend is running
if ! curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "⚠️  Backend not running. Starting it..."
    cd "$(dirname "$0")"
    waft serve --port 8000 --host localhost --dev > /tmp/waft_backend.log 2>&1 &
    echo "⏳ Waiting for backend to start..."
    sleep 3
fi

# Start frontend
echo "🚀 Starting frontend..."
cd visualizer
npm run dev

echo ""
echo "✅ Open: http://localhost:8781/evolve-ui-monitor"