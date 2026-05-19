#!/usr/bin/env python3
"""
Regression test to prove cache invalidation works correctly.
This test ensures that when a link is created with a custom code,
any existing stale cache for that code is properly invalidated.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import httpx
import json
import time
from sqlalchemy import select
from app.redis_client import RedisClient
from app.services import LinkService
from app.db import SessionLocal
from app.models import Link

BASE_URL = "http://127.0.0.1:8000"

def test_cache_invalidation():
    print("Testing cache invalidation...")
    
    # Create a test link directly in the database first
    db = SessionLocal()
    try:
        # Clean up any existing test data
        existing = db.execute(select(Link).where(Link.code == "cachetest")).scalar_one_or_none()
        if existing:
            db.delete(existing)
            db.commit()
        
        # Create a test link
        test_link = Link(
            code="cachetest",
            long_url="https://example.com/old",
            created_by="test_user"
        )
        db.add(test_link)
        db.commit()
        print("✓ Created test link in database")
        
    except Exception as e:
        print(f"✗ Failed to create test link: {e}")
        return False
    finally:
        db.close()
    
    # Step 1: Populate cache by accessing the link
    print("Step 1: Populating cache...")
    try:
        client = httpx.Client(timeout=10.0)
        response = client.get(f"{BASE_URL}/cachetest", follow_redirects=False)
        if response.status_code == 307:
            print("✓ Cache populated successfully")
        else:
            print(f"✗ Unexpected response: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Failed to populate cache: {e}")
        return False
    
    # Step 2: Verify cache exists
    print("Step 2: Verifying cache exists...")
    cached_data = RedisClient.get("link:cachetest")
    if cached_data:
        print("✓ Cache entry exists")
        data = json.loads(cached_data)
        if data["long_url"] == "https://example.com/old":
            print("✓ Cache contains old URL")
        else:
            print(f"✗ Cache has unexpected URL: {data['long_url']}")
            return False
    else:
        print("✗ Cache entry not found")
        return False
    
    # Step 3: Create a new link with same code via API (should invalidate cache)
    print("Step 3: Creating new link with same code...")
    try:
        # Register and login first
        reg = client.post(f"{BASE_URL}/register", json={"email": "cache@test.com", "password": "password123"})
        login = client.post(f"{BASE_URL}/login", data={"username": "cache@test.com", "password": "password123"})
        if login.status_code != 200:
            print(f"✗ Login failed: {login.status_code}")
            return False
        
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create new link with same custom code
        link_data = {
            "long_url": "https://example.com/NEW",
            "custom_code": "cachetest"
        }
        create_response = client.post(f"{BASE_URL}/links", json=link_data, headers=headers)
        if create_response.status_code == 400 and "already exists" in create_response.text:
            print("✗ Link already exists (cache invalidation not tested)")
            return False
        elif create_response.status_code == 200:
            print("✓ New link created successfully")
        else:
            print(f"✗ Failed to create link: {create_response.status_code} - {create_response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Failed to create new link: {e}")
        return False
    
    # Step 4: Verify cache was invalidated and repopulated with new data
    print("Step 4: Verifying cache invalidation...")
    time.sleep(1)  # Allow cache to be repopulated
    
    # Access the link again to trigger cache repopulation
    try:
        response = client.get(f"{BASE_URL}/cachetest", follow_redirects=False)
        if response.status_code != 307:
            print(f"✗ Redirect failed: {response.status_code}")
            return False
        
        # Check cache content
        cached_data = RedisClient.get("link:cachetest")
        if cached_data:
            data = json.loads(cached_data)
            if data["long_url"] == "https://example.com/NEW":
                print("✓ Cache successfully invalidated and repopulated with new URL")
                return True
            else:
                print(f"✗ Cache still contains old URL: {data['long_url']}")
                return False
        else:
            print("✗ Cache not repopulated")
            return False
            
    except Exception as e:
        print(f"✗ Failed to verify cache invalidation: {e}")
        return False

if __name__ == "__main__":
    success = test_cache_invalidation()
    if success:
        print("\n🎉 SUCCESS: Cache invalidation works correctly!")
    else:
        print("\n❌ FAILURE: Cache invalidation test failed!")
    exit(0 if success else 1)
