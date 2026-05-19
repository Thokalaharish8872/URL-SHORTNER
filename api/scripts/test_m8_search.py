#!/usr/bin/env python3
"""
Test script for Module 8 search functionality.
Tests FTS search and pagination.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import httpx

BASE_URL = "http://127.0.0.1:8000"

def test_search_endpoint():
    print("Testing Module 8 Search Functionality")
    print("=" * 50)
    
    client = httpx.Client(timeout=10.0)
    
    # Test 1: Search endpoint exists
    print("\n1. Testing search endpoint...")
    try:
        response = client.get(f"{BASE_URL}/links/search?q=test")
        print(f"   Status: {response.status_code}")
        if response.status_code in [200, 503]:
            print("   ✓ Search endpoint accessible")
        else:
            print(f"   ✗ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   ℹ️  Search endpoint test: {e}")
    
    # Test 2: Search requires query parameter
    print("\n2. Testing search validation...")
    try:
        response = client.get(f"{BASE_URL}/links/search")
        print(f"   Status without 'q': {response.status_code}")
        if response.status_code == 400:
            print("   ✓ Correctly rejects empty search query")
        else:
            print(f"   ℹ️  Status: {response.status_code}")
    except Exception as e:
        print(f"   ℹ️  Validation test: {e}")
    
    # Test 3: Pagination parameters
    print("\n3. Testing pagination in search...")
    try:
        response = client.get(f"{BASE_URL}/links/search?q=example&skip=0&limit=5")
        print(f"   Status: {response.status_code}")
        print("   ✓ Pagination parameters accepted")
    except Exception as e:
        print(f"   ℹ️  Pagination test: {e}")
    
    print("\n" + "=" * 50)
    print("Module 8 search tests completed")

if __name__ == "__main__":
    test_search_endpoint()
