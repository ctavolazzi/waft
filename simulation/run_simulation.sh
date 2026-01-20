#!/bin/bash
# Run Thoth Realm Simulator

cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -q fastapi uvicorn websockets

# Run server
echo "Starting Thoth Realm Simulator..."
echo "Open http://localhost:8000 in your browser"
python simulation_server.py
