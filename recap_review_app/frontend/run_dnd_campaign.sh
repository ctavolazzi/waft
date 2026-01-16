#!/bin/bash
# Run Electron app in DnD Campaign mode

cd "$(dirname "$0")"

echo "🎲 Starting Electron app in DnD Campaign mode..."
echo ""

# Check if Docker is running
if docker info > /dev/null 2>&1; then
    echo "🐳 Docker is running - starting containers..."
    
    # Start backend if not running
    if ! docker ps | grep -q recap-review-backend; then
        echo "   Starting backend..."
        docker-compose up -d backend
        sleep 3
    fi
    
    # Start Electron app with campaign mode
    DND_CAMPAIGN=1 npm start
else
    echo "⚠️  Docker not running - using local mode"
    echo "   Make sure backend is running: cd ../backend && uvicorn main:app --reload"
    echo ""
    
    # Start Electron locally with campaign mode
    DND_CAMPAIGN=1 npm start
fi
