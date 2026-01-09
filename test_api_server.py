#!/usr/bin/env python3
"""
Quick verification script for Decision Engine API.

Tests the API endpoints to verify the server is working correctly.
"""

import requests
import json
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"


def test_health():
    """Test the health endpoint."""
    print("🔍 Testing /api/decision/health...")
    response = requests.get(f"{BASE_URL}/api/decision/health")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Health check passed: {data}")
        return True
    else:
        print(f"❌ Health check failed: {response.status_code}")
        return False


def test_analyze():
    """Test the analyze endpoint with PorchRoot scenario."""
    print("\n🔍 Testing /api/decision/analyze...")
    
    request_data = {
        "problem": "Q1 Strategy",
        "alternatives": ["PorchRoot", "FogSift"],
        "criteria": {
            "Cash Flow": 0.6,
            "Joy": 0.4
        },
        "scores": {
            "PorchRoot": {"Cash Flow": 4, "Joy": 10},
            "FogSift": {"Cash Flow": 9, "Joy": 6}
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/api/decision/analyze",
        json=request_data
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Analysis successful!")
        print(f"   Winner: {data['recommendation']}")
        print(f"   Top Score: {data['rankings'][0]['score']}")
        print(f"   Rankings:")
        for rank in data['rankings']:
            print(f"     {rank['rank']}. {rank['name']}: {rank['score']:.2f}")
        print(f"   Robust: {data['is_robust']}")
        return True
    else:
        print(f"❌ Analysis failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return False


def main():
    """Run all API tests."""
    print("=" * 60)
    print("🚀 Decision Engine API Verification")
    print("=" * 60)
    print(f"\nTesting server at: {BASE_URL}")
    print("Make sure the server is running: waft serve\n")
    
    try:
        health_ok = test_health()
        analyze_ok = test_analyze()
        
        print("\n" + "=" * 60)
        if health_ok and analyze_ok:
            print("✅ All tests passed! The API is working correctly.")
        else:
            print("❌ Some tests failed. Check the output above.")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to server!")
        print("   Make sure the server is running:")
        print("   $ waft serve")
        print("   or")
        print("   $ uvicorn src.waft.api.main:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
