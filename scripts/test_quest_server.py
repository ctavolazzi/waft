#!/usr/bin/env python3
"""
Quick test script for the quest server.

Tests that the server can start and basic endpoints work.
"""

import requests
import time
import subprocess
import sys
from pathlib import Path

def test_quest_server():
    """Test the quest server."""
    print("🧪 Testing Quest Server...\n")
    
    # Start server in background
    print("1. Starting server...")
    server_process = subprocess.Popen(
        [sys.executable, "scripts/quest_server.py", "--port", "8002"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=Path(__file__).parent.parent
    )
    
    # Wait for server to start
    time.sleep(2)
    
    base_url = "http://localhost:8002/api/quests"
    
    try:
        # Test root endpoint
        print("2. Testing root endpoint...")
        response = requests.get("http://localhost:8002/", timeout=5)
        assert response.status_code == 200
        print("   ✅ Root endpoint works")
        
        # Test status endpoint
        print("3. Testing status endpoint...")
        response = requests.get(f"{base_url}/status", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert "total_quests" in data
        assert "completed" in data
        print(f"   ✅ Status: {data['completed']}/{data['total_quests']} quests completed")
        
        # Test list quests
        print("4. Testing list quests endpoint...")
        response = requests.get(f"{base_url}", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert "quests" in data
        assert len(data["quests"]) > 0
        print(f"   ✅ Found {len(data['quests'])} quests")
        
        # Test get quest
        print("5. Testing get quest endpoint...")
        quest_id = data["quests"][0]["quest_id"]
        response = requests.get(f"{base_url}/{quest_id}", timeout=5)
        assert response.status_code == 200
        quest_data = response.json()
        assert quest_data["quest_id"] == quest_id
        print(f"   ✅ Retrieved quest: {quest_data['name']}")
        
        print("\n✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False
    finally:
        # Stop server
        print("\n6. Stopping server...")
        server_process.terminate()
        server_process.wait(timeout=5)
        print("   ✅ Server stopped")


if __name__ == "__main__":
    success = test_quest_server()
    sys.exit(0 if success else 1)
