#!/usr/bin/env python3
"""
The Big Bad Wolf - Stress Testing the Decision Engine Fortress.

This script attacks the API with invalid data, logic bombs, and massive payloads
to verify the layered defense architecture stands strong.
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8001/api/decision"
HEADERS = {"Content-Type": "application/json"}


def huff_and_puff(name, payload, expected_code):
    """The Wolf's attack - huff and puff and see if the house stands."""
    print(f"\n🐺 ATTACK: {name}...")
    try:
        start = time.time()
        response = requests.post(f"{BASE_URL}/analyze", json=payload, headers=HEADERS)
        duration = time.time() - start
        
        status = response.status_code
        try:
            body = response.json()
        except:
            body = response.text

        if status == expected_code:
            print(f"🧱 BLOCKED! (Status {status}) - The House Stands.")
            if isinstance(body, dict) and "detail" in body:
                print(f"   Error: {body['detail'][:100]}...")
            else:
                print(f"   Response: {str(body)[:100]}...")
        elif status == 200 and expected_code == 200:
            print(f"✅ SUCCESS! (Status 200) - Handled correctly in {duration:.4f}s")
            if isinstance(body, dict) and "recommendation" in body:
                print(f"   Winner: {body['recommendation']}")
        else:
            print(f"💥 CRASH! (Status {status}, Expected {expected_code}) - THE HOUSE FELL DOWN!")
            print(f"   Response: {str(body)[:200]}")
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to server! Is it running?")
    except Exception as e:
        print(f"💀 CRITICAL FAILURE: {e}")


# ==========================================
# ATTACK 1: THE NEGATIVE WEIGHT NUKE
# ==========================================
# We bypass the Pydantic type check (it allows floats) 
# but the Iron Core should catch the logical impossibility.
# EXPECTED: 400 Bad Request (Iron Core validation catches it)
payload_nuke = {
    "problem": "Nuclear Test",
    "alternatives": ["A", "B"],
    "criteria": {"Cost": -1.0, "Speed": 2.0},  # Sums to 1.0, but negative!
    "scores": {"A": {"Cost": 10, "Speed": 10}, "B": {"Cost": 5, "Speed": 5}}
}

# ==========================================
# ATTACK 2: THE TYPE MISMATCH (Straw House)
# ==========================================
# Sending a string where a float is expected.
# Pydantic (Layer 1) should catch this before it even hits the Core.
# EXPECTED: 422 Unprocessable Entity (Pydantic validation)
payload_straw = {
    "problem": "Type Test",
    "alternatives": ["A", "B"],
    "criteria": {"Cost": "five_hundred", "Speed": 0.5}, 
    "scores": {"A": {"Cost": 10, "Speed": 10}, "B": {"Cost": 5, "Speed": 5}}
}

# ==========================================
# ATTACK 3: THE MASSIVE LOAD (Brick Test)
# ==========================================
# Can it handle 1,000 alternatives without choking?
# This tests performance, not just validity.
# EXPECTED: 200 OK (should succeed, just slow)
many_alts = [f"Option_{i}" for i in range(1000)]
many_scores = {f"Option_{i}": {"Cost": i % 10, "Speed": (i*2) % 10} for i in range(1000)}

payload_heavy = {
    "problem": "Stress Test - 1,000 Alternatives",
    "alternatives": many_alts,
    "criteria": {"Cost": 0.5, "Speed": 0.5},
    "scores": many_scores
}

# ==========================================
# ATTACK 4: THE MISSING DATA BOMB
# ==========================================
# Missing scores for one alternative
# EXPECTED: 400 Bad Request (Iron Core completeness check)
payload_missing = {
    "problem": "Missing Data Test",
    "alternatives": ["A", "B", "C"],
    "criteria": {"Cost": 0.5, "Speed": 0.5},
    "scores": {
        "A": {"Cost": 10, "Speed": 10},
        "B": {"Cost": 5, "Speed": 5}
        # Missing C!
    }
}

# ==========================================
# ATTACK 5: THE NAN INFECTION
# ==========================================
# Attempting to inject NaN values
# Note: JSON doesn't support NaN, so we'll send it as a string and let InputTransformer handle it
# EXPECTED: 400 Bad Request (Iron Core NaN check after InputTransformer converts)
# Actually, we'll skip this one since JSON can't represent NaN
# Instead, we'll test with a very large number that might cause issues
payload_nan = {
    "problem": "Extreme Value Test",
    "alternatives": ["A", "B"],
    "criteria": {"Cost": 0.5, "Speed": 0.5},
    "scores": {
        "A": {"Cost": 1e308, "Speed": 10},  # Very large number
        "B": {"Cost": 5, "Speed": 5}
    }
}

# ==========================================
# ATTACK 6: THE WEIGHT SUM BOMB
# ==========================================
# Weights don't sum to 1.0 (loose tolerance test)
# EXPECTED: 400 Bad Request (Iron Core strict tolerance)
payload_loose = {
    "problem": "Loose Tolerance Test",
    "alternatives": ["A", "B"],
    "criteria": {"Cost": 0.99, "Speed": 0.01},  # Sums to 1.0 exactly - should PASS
    "scores": {"A": {"Cost": 10, "Speed": 10}, "B": {"Cost": 5, "Speed": 5}}
}

# Actually test loose tolerance - weights sum to 0.99 (off by 0.01, > 1e-6)
payload_loose_real = {
    "problem": "Loose Tolerance Test (Real)",
    "alternatives": ["A", "B"],
    "criteria": {"Cost": 0.99, "Speed": 0.0},  # Sums to 0.99, not 1.0
    "scores": {"A": {"Cost": 10, "Speed": 10}, "B": {"Cost": 5, "Speed": 5}}
}

# ==========================================
# EXECUTE THE ATTACKS
# ==========================================
if __name__ == "__main__":
    print("=" * 60)
    print("🌪️  THE BIG BAD WOLF IS COMING...")
    print("=" * 60)
    
    # Ensure server is running first!
    try:
        health_response = requests.get(f"{BASE_URL}/health", timeout=2)
        if health_response.status_code == 200:
            print("✅ Server is running and healthy")
        else:
            print(f"⚠️  Server responded with status {health_response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to server!")
        print("   Start the server first:")
        print("   $ uvicorn src.waft.api.main:app --reload")
        print("   or")
        print("   $ waft serve")
        exit(1)
    except Exception as e:
        print(f"❌ Error checking server: {e}")
        exit(1)
    
    print("\n" + "=" * 60)
    print("🐺 BEGINNING ATTACKS...")
    print("=" * 60)
    
    # Attack 1: Negative Weights
    # TRICK QUESTION: If we did our job, this should be a 400 (Iron Core catches it)
    # If it's a 500, we failed to catch the ValueError in the API route.
    huff_and_puff("Negative Weights (Logic Bomb)", payload_nuke, 400)
    
    # Attack 2: Invalid Types
    # Pydantic (Layer 1) should block this before it hits the Core
    huff_and_puff("Invalid Types (Straw House)", payload_straw, 422)
    
    # Attack 3: Massive Load
    # Should succeed, just slow - tests performance
    huff_and_puff("1,000 Alternatives (Brick Test)", payload_heavy, 200)
    
    # Attack 4: Missing Data
    # Iron Core completeness check should catch this
    huff_and_puff("Missing Scores (Data Bomb)", payload_missing, 400)
    
    # Attack 5: Extreme Values
    # Tests handling of very large numbers
    huff_and_puff("Extreme Values (Large Numbers)", payload_nan, 200)
    
    # Attack 6: Loose Tolerance (should pass - sums to 1.0)
    huff_and_puff("Weight Sum = 1.0 (Should Pass)", payload_loose, 200)
    
    # Attack 7: Real Loose Tolerance (should fail - sums to 0.99)
    huff_and_puff("Loose Weight Sum (Tolerance Bomb)", payload_loose_real, 400)
    
    print("\n" + "=" * 60)
    print("🏁 ATTACKS COMPLETE")
    print("=" * 60)
    print("\n📊 Summary:")
    print("   - If all attacks were BLOCKED or SUCCESS (expected status),")
    print("     the Fortress stands strong! 🧱")
    print("   - If any attack resulted in CRASH (500 or unexpected status),")
    print("     the House fell down! 💥")
    print("\n")
