"""
Simple test script to verify the DevLift API is working.
Run this from the project root: python test_api.py
"""

import requests
import json
import time

API_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint."""
    print("Testing /health endpoint...")
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"✓ Health check: {response.status_code}")
        print(f"  Response: {response.json()}")
        return True
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False

def test_analyze():
    """Test the analyze endpoint with Express.js repo."""
    print("\nTesting /analyze endpoint with expressjs/express...")
    print("This will take 20-40 seconds as it calls GitHub API and watsonx.ai...")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{API_URL}/analyze",
            json={"repo_url": "https://github.com/expressjs/express"},
            timeout=120  # 2 minute timeout
        )
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Analysis complete in {elapsed:.1f} seconds")
            print(f"  Repository: {data['owner']}/{data['repo']}")
            print(f"  Language: {data['language']}")
            print(f"  Stars: {data['stars']}")
            print(f"  Files analyzed: {data['files_analyzed']}")
            print(f"  Readiness score: {data['readiness']['score']}/100 (Grade {data['readiness']['grade']})")
            print(f"  Kit sections: {', '.join(data['kit'].keys())}")
            return True
        else:
            print(f"✗ Analysis failed: {response.status_code}")
            print(f"  Error: {response.json()}")
            return False
            
    except requests.exceptions.Timeout:
        print("✗ Request timed out after 120 seconds")
        return False
    except Exception as e:
        print(f"✗ Analysis failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("DevLift API Test")
    print("=" * 60)
    
    # Test health endpoint
    health_ok = test_health()
    
    if health_ok:
        # Test analyze endpoint
        analyze_ok = test_analyze()
        
        if analyze_ok:
            print("\n" + "=" * 60)
            print("✓ All tests passed! The API is working correctly.")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("✗ Analysis test failed. Check backend logs for errors.")
            print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("✗ Health check failed. Is the backend running?")
        print("=" * 60)

# Made with Bob
