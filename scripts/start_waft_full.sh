#!/bin/bash
# Start both WAFT API server and UI

set -e

# Get project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🌊 Starting WAFT Full Stack${NC}"
echo ""

# Start API server in background
echo -e "${GREEN}🚀 Starting API server on port 8000...${NC}"
bash "$PROJECT_ROOT/scripts/start_waft_server.sh" 8000 localhost false > /tmp/waft_api.log 2>&1 &
API_PID=$!

# Wait for API to be ready
echo "⏳ Waiting for API to be ready..."
sleep 3

# Check if API is responding
for i in {1..10}; do
    if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ API server is ready${NC}"
        break
    fi
    if [ $i -eq 10 ]; then
        echo -e "${YELLOW}⚠️  API server may not be ready, but continuing...${NC}"
    fi
    sleep 1
done

# Start UI
echo -e "${GREEN}🎨 Starting UI on port 8781...${NC}"
cd "$PROJECT_ROOT/visualizer"
npm run dev &
UI_PID=$!

# Trap to kill both processes on exit
trap "echo ''; echo '👋 Shutting down...'; kill $API_PID $UI_PID 2>/dev/null; exit" INT TERM

echo ""
echo -e "${BLUE}✅ WAFT is running!${NC}"
echo -e "${GREEN}📍 API: http://localhost:8000${NC}"
echo -e "${GREEN}📍 API Docs: http://localhost:8000/docs${NC}"
echo -e "${GREEN}📍 UI: http://localhost:8781${NC}"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for either process to exit
wait
