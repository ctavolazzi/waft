#!/bin/bash

# Typst Demo Web App Startup Script
# Run this from the typst-webapp directory

echo "🚀 Starting Typst Demo Web App..."
echo ""

# Check for Typst
if ! command -v typst &> /dev/null; then
    echo "❌ Typst not found. Please install: brew install typst"
    exit 1
fi

echo "✅ Typst found: $(which typst)"

# Start backend
echo ""
echo "📦 Starting FastAPI backend..."
cd backend

# Create venv if needed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

# Start backend in background
python main.py &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID) at http://localhost:8000"

cd ..

# Start frontend
echo ""
echo "🎨 Starting SvelteKit frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Start frontend
npm run dev &
FRONTEND_PID=$!
echo "✅ Frontend started (PID: $FRONTEND_PID) at http://localhost:5173"

echo ""
echo "=========================================="
echo "🎉 Typst Demo App is running!"
echo ""
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo "=========================================="

# Wait and cleanup on exit
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
