#!/bin/bash
# Start Recap and Review Docker services

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(dirname "$SCRIPT_DIR")"

cd "$APP_DIR"

echo "🐳 Starting Recap and Review Docker services..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check for development flag
if [ "$1" == "--dev" ] || [ "$1" == "-d" ]; then
    echo "📦 Building development backend..."
    docker-compose --profile dev build backend-dev
    
    echo "🚀 Starting development backend (port 8001)..."
    docker-compose --profile dev up -d backend-dev
    
    echo ""
    echo "✅ Development backend started!"
    echo "   URL: http://localhost:8001"
    echo "   Logs: docker-compose --profile dev logs -f backend-dev"
else
    echo "📦 Building backend..."
    docker-compose build backend
    
    echo "🚀 Starting backend (port 8000)..."
    docker-compose up -d backend
    
    echo ""
    echo "✅ Backend started!"
    echo "   URL: http://localhost:8000"
    echo "   Logs: docker-compose logs -f backend"
fi

echo ""
echo "📋 Next steps:"
echo "   1. Start Electron frontend: cd frontend && npm start"
echo "   2. Check health: curl http://localhost:8000/api/health"
echo "   3. View logs: docker-compose logs -f backend"
echo ""
