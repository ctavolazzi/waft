#!/bin/bash
# Start script for Being test environment

echo "🚀 Starting WAFT Being Test Environment"
echo ""

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Must run from project root"
    exit 1
fi

# Start API server in background
echo "📡 Starting API server on port 8000..."
uvicorn src.waft.api.main:app --reload --port 8000 &
API_PID=$!

# Wait a moment for API to start
sleep 2

# Start React app
echo "⚛️  Starting React app on port 3000..."
cd react-being-test
npm run dev &
REACT_PID=$!

echo ""
echo "✅ Services started!"
echo "   API: http://localhost:8000"
echo "   React: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user interrupt
trap "kill $API_PID $REACT_PID; exit" INT TERM
wait
