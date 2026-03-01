#!/usr/bin/env python3
"""
Test script for OpenAI GPT integration
Run this after adding your API key to .env file
"""

import requests
import json
import sys

API_BASE = "http://localhost:5000/api"

def test_query(query, description=""):
    """Test a single query"""
    print(f"\n{'='*80}")
    print(f"TEST: {description}")
    print(f"Query: '{query}'")
    print(f"{'='*80}")
    
    try:
        response = requests.post(
            f"{API_BASE}/query",
            json={"query": query},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                answer = data['response']['answer']
                print(f"\n✓ SUCCESS\n")
                print(answer[:500])  # First 500 chars
                
                if data['response'].get('visualization'):
                    viz = data['response']['visualization']
                    print(f"\n📊 Visualization: {viz['type']} - {viz.get('title', 'N/A')}")
                
                return True
            else:
                print(f"\n✗ FAILED: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"\n✗ HTTP {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("\n✗ CONNECTION ERROR: Is the backend running? (python3 app.py)")
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        return False

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║         InsightX OpenAI Integration Test Suite              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    # Check if server is running
    try:
        health = requests.get(f"{API_BASE}/health", timeout=5)
        if health.status_code != 200:
            print("✗ Backend is not healthy. Please start it first.")
            sys.exit(1)
        print("✓ Backend is running")
    except:
        print("✗ Cannot connect to backend. Please run: python3 app.py")
        sys.exit(1)
    
    # Test queries (from simple to complex)
    tests = [
        # Basic queries
        ("count", "Simple count query"),
        ("what is the total?", "Natural language total"),
        ("average transaction amount", "Basic average"),
        
        # Category-specific
        ("average food transaction", "Category filter - Food"),
        ("how much do people spend on entertainment?", "Natural category question"),
        
        # Device comparisons
        ("compare iOS vs Android", "Device comparison"),
        ("which device is better?", "Implicit comparison"),
        
        # Network analysis
        ("show me 5G vs WiFi performance", "Network comparison"),
        
        # Complex queries
        ("what are peak transaction hours for food category?", "Multi-filter peak time"),
        ("average android food transactions on weekends", "Multiple filters"),
        
        # Fraud and failures
        ("fraud analysis", "Fraud detection"),
        ("failure rate", "Failure analysis"),
        
        # Natural variations
        ("tell me about the data", "General overview"),
        ("what's going on with shopping?", "Casual question"),
        ("top performers", "Top analysis"),
    ]
    
    passed = 0
    failed = 0
    
    for query, description in tests:
        if test_query(query, description):
            passed += 1
        else:
            failed += 1
        input("\nPress Enter to continue to next test...")
    
    # Summary
    print(f"\n\n{'='*80}")
    print(f"TEST SUMMARY")
    print(f"{'='*80}")
    print(f"✓ Passed: {passed}/{len(tests)}")
    print(f"✗ Failed: {failed}/{len(tests)}")
    print(f"Success Rate: {(passed/len(tests)*100):.1f}%")
    
    if failed == 0:
        print("\n🎉 All tests passed! OpenAI integration is working perfectly!")
    elif passed > len(tests) * 0.8:
        print("\n✓ Most tests passed. OpenAI is working well!")
    else:
        print("\n⚠️ Many tests failed. Check your OpenAI API key and backend logs.")

if __name__ == "__main__":
    main()
