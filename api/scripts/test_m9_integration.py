#!/usr/bin/env python3
"""
Module 9 Integration Tests
Tests highest-risk behaviors against running API server.

Usage:
    1. Start the API server: python -m uvicorn app.main:app --reload
    2. Run tests: python scripts/test_m9_integration.py
"""

import sys
import os
import requests
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = "http://127.0.0.1:8000"


class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.token = None
        
    def run_all(self):
        print("=" * 60)
        print("Module 9 Integration Tests")
        print("Testing highest-risk behaviors")
        print("=" * 60)
        
        self.test_health_check()
        self.test_auth_flow()
        self.test_link_crud()
        self.test_redirect()
        self.test_search()
        
        print("\n" + "=" * 60)
        print(f"Results: {self.passed} passed, {self.failed} failed")
        print("=" * 60)
        
        return self.failed == 0
    
    def assert_eq(self, actual, expected, msg=""):
        if actual == expected:
            self.passed += 1
            print(f"  ✓ {msg}")
            return True
        else:
            self.failed += 1
            print(f"  ✗ {msg} (expected {expected}, got {actual})")
            return False
    
    def test_health_check(self):
        print("\n📋 Testing Health Check")
        response = requests.get(f"{BASE_URL}/health")
        self.assert_eq(response.status_code, 200, "Health check returns 200")
        self.assert_eq(response.json().get("status"), "ok", "Health status is ok")
    
    def test_auth_flow(self):
        print("\n🔐 Testing Authentication Flow")
        
        # Register
        email = f"test_{time.time()}@example.com"
        response = requests.post(f"{BASE_URL}/register", json={
            "email": email,
            "password": "password123"
        })
        self.assert_eq(response.status_code, 200, "Registration succeeds")
        
        # Login
        response = requests.post(f"{BASE_URL}/login", data={
            "username": email,
            "password": "password123"
        })
        self.assert_eq(response.status_code, 200, "Login succeeds")
        self.token = response.json().get("access_token")
        
        # Access protected endpoint
        response = requests.get(
            f"{BASE_URL}/links",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assert_eq(response.status_code, 200, "Authenticated access works")
        
        # Logout
        response = requests.post(
            f"{BASE_URL}/logout",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assert_eq(response.status_code, 200, "Logout succeeds")
        
        # Verify token invalidation
        response = requests.get(
            f"{BASE_URL}/links",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assert_eq(response.status_code, 401, "Token invalidated after logout")
    
    def test_link_crud(self):
        print("\n🔗 Testing Link CRUD Operations")
        
        # Register and login
        email = f"link_test_{time.time()}@example.com"
        requests.post(f"{BASE_URL}/register", json={
            "email": email,
            "password": "password123"
        })
        response = requests.post(f"{BASE_URL}/login", data={
            "username": email,
            "password": "password123"
        })
        token = response.json()["access_token"]
        
        # Create link
        response = requests.post(
            f"{BASE_URL}/links",
            json={"long_url": "https://example.com/test"},
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assert_eq(response.status_code, 200, "Create link succeeds")
        code = response.json().get("code")
        
        # Create with custom code
        response = requests.post(
            f"{BASE_URL}/links",
            json={
                "long_url": "https://custom.example.com",
                "custom_code": f"custom_{time.time():.0f}"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assert_eq(response.status_code, 200, "Create link with custom code")
        
        # List links
        response = requests.get(
            f"{BASE_URL}/links",
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assert_eq(response.status_code, 200, "List links succeeds")
        self.assert_eq(isinstance(response.json(), list), True, "List returns array")
    
    def test_redirect(self):
        print("\n🔄 Testing Redirect Behavior")
        
        # Register and login
        email = f"redirect_{time.time()}@example.com"
        requests.post(f"{BASE_URL}/register", json={
            "email": email,
            "password": "password123"
        })
        response = requests.post(f"{BASE_URL}/login", data={
            "username": email,
            "password": "password123"
        })
        token = response.json()["access_token"]
        
        # Create link
        response = requests.post(
            f"{BASE_URL}/links",
            json={"long_url": "https://redirect.example.com"},
            headers={"Authorization": f"Bearer {token}"}
        )
        code = response.json().get("code")
        
        # Test redirect
        response = requests.get(
            f"{BASE_URL}/{code}",
            allow_redirects=False
        )
        self.assert_eq(response.status_code, 307, "Redirect returns 307")
        
        # Test nonexistent link
        response = requests.get(f"{BASE_URL}/nonexistent123")
        self.assert_eq(response.status_code, 404, "Nonexistent link returns 404")
    
    def test_search(self):
        print("\n🔍 Testing Search Functionality")
        
        # Register and login
        email = f"search_{time.time()}@example.com"
        requests.post(f"{BASE_URL}/register", json={
            "email": email,
            "password": "password123"
        })
        response = requests.post(f"{BASE_URL}/login", data={
            "username": email,
            "password": "password123"
        })
        token = response.json()["access_token"]
        
        # Create link
        requests.post(
            f"{BASE_URL}/links",
            json={"long_url": "https://searchable.example.com"},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Search
        response = requests.get(
            f"{BASE_URL}/links/search?q=searchable",
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assert_eq(response.status_code, 200, "Search endpoint works")
        self.assert_eq(isinstance(response.json(), list), True, "Search returns array")


if __name__ == "__main__":
    runner = TestRunner()
    success = runner.run_all()
    sys.exit(0 if success else 1)
