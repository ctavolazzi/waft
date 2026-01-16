#!/bin/bash
# Start Projects Dashboard - Full Stack

echo "🌊 Starting WAFT Projects Dashboard..."
echo ""

# Check if FastAPI server is already running
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "✅ FastAPI server already running on port 8000"
else
    echo "🚀 Starting FastAPI server..."
    cd "$(dirname "$0")/.."
    waft serve --dev --port 8000 > /tmp/waft_api.log 2>&1 &
    API_PID=$!
    echo "   FastAPI server started (PID: $API_PID)"
    echo "   Logs: /tmp/waft_api.log"
    sleep 2
fi

# Check if SvelteKit dev server is already running
if lsof -Pi :5173 -sTCP:LISTEN -t >/dev/null ; then
    echo "✅ SvelteKit dev server already running on port 5173"
else
    echo "🚀 Starting SvelteKit dev server..."
    cd "$(dirname "$0")/../visualizer"

    if [ ! -d "node_modules" ]; then
        echo "   Installing dependencies..."
        npm install
    fi

    npm run dev > /tmp/waft_sveltekit.log 2>&1 &
    SK_PID=$!
    echo "   SvelteKit dev server started (PID: $SK_PID)"
    echo "   Logs: /tmp/waft_sveltekit.log"
    sleep 3
fi

echo ""
echo "✅ Dashboard is ready!"
echo ""
echo "📍 Open in browser:"
echo "   http://localhost:5173/projects"
echo ""
echo "📊 API endpoints:"
echo "   http://localhost:8000/api/projects"
echo "   http://localhost:8000/api/projects/stats"
echo "   http://localhost:8000/docs (API documentation)"
echo ""
echo "Press Ctrl+C to stop (or kill processes manually)"
