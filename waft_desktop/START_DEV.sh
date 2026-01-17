#!/bin/bash
# WAFT Desktop - Development Startup Script

set -e

echo "🌊 Starting WAFT Desktop Development Environment"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -d "electron" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Must run from waft_desktop directory"
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js not found. Please install Node.js 18+"
    exit 1
fi

# Check Python/WAFT
if ! command -v waft &> /dev/null; then
    echo "⚠️  Warning: WAFT command not found. Backend may not start automatically."
fi

echo "📦 Installing dependencies..."
echo ""

# Install Electron dependencies
if [ ! -d "electron/node_modules" ]; then
    echo "${YELLOW}→ Installing Electron dependencies...${NC}"
    cd electron
    npm install
    cd ..
fi

# Install Frontend dependencies
if [ ! -d "frontend/node_modules" ]; then
    echo "${YELLOW}→ Installing Frontend dependencies...${NC}"
    cd frontend
    npm install
    cd ..
fi

echo ""
echo "${GREEN}✅ Dependencies installed${NC}"
echo ""
echo "🚀 Starting development servers..."
echo ""
echo "Terminal 1: Frontend (SvelteKit)"
echo "Terminal 2: Electron (Desktop App)"
echo ""
echo "Starting Frontend dev server..."
echo ""

# Start frontend in background
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Wait a moment for frontend to start
sleep 3

# Start Electron
echo "Starting Electron app..."
cd electron
npm start
cd ..

# Cleanup on exit
trap "kill $FRONTEND_PID 2>/dev/null" EXIT
