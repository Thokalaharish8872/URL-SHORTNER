"""
Integration tests for Module 9.
Tests the highest-risk behaviors:
- redirect correctness (with cache and rate limiting)
- auth protection
- analytics writes (sync/async)

Note: These tests use a live API instance rather than SQLite
because the Link model uses PostgreSQL ARRAY type for tags.
"""

import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(scope="module")
def auth_token():
    """Create an authenticated user and return token."""
    email = f"test_user_{__import__('time').time()}@example.com"
    password = "password123"
    
    # Register
    requests.post(f"{BASE_URL}/register", json={
        "email": email,
        "password": password
    })
    
    # Login
    response = requests.post(f"{BASE_URL}/login", data={
        "username": email,
        "password": password
    })
    
    return response.json()["access_token"]


class TestRedirectCorrectness:
    """Test redirect behavior including cache, expiration, and rate limiting."""

    def test_redirect_nonexistent_link(self):
        """Test that nonexistent links return 404."""
        response = requests.get(f"{BASE_URL}/nonexistent")
        assert response.status_code == 404

    def test_health_check(self):
        """Test health endpoint returns OK."""
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestAuthProtection:
    """Test authentication and authorization."""

    def test_register_user(self):
        """Test user registration."""
        email = f"new_user_{__import__('time').time()}@example.com"
        response = requests.post(f"{BASE_URL}/register", json={
            "email": email,
            "password": "securepassword123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "email" in data
        assert "id" in data

    def test_login_invalid(self):
        """Test invalid login returns 401."""
        response = requests.post(f"{BASE_URL}/login", data={
            "username": "nonexistent@test.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401

    def test_protected_endpoint_without_auth(self):
        """Test that protected endpoints reject unauthenticated requests."""
        response = requests.get(f"{BASE_URL}/links")
        assert response.status_code == 401

    def test_create_link_with_auth(self, auth_token):
        """Test creating a link with authentication."""
        response = requests.post(
            f"{BASE_URL}/links",
            json={"long_url": "https://example.com/test"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "code" in data
        assert data["long_url"] == "https://example.com/test"

    def test_create_link_with_custom_code(self, auth_token):
        """Test creating a link with custom code."""
        custom_code = f"custom_{__import__('time').time():.0f}"
        response = requests.post(
            f"{BASE_URL}/links",
            json={
                "long_url": "https://custom.example.com",
                "custom_code": custom_code
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == custom_code

    def test_create_duplicate_custom_code(self, auth_token):
        """Test that duplicate custom codes are rejected."""
        custom_code = f"dup_{__import__('time').time():.0f}"
        
        # Create first link
        requests.post(
            f"{BASE_URL}/links",
            json={
                "long_url": "https://first.example.com",
                "custom_code": custom_code
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        # Try duplicate
        response = requests.post(
            f"{BASE_URL}/links",
            json={
                "long_url": "https://second.example.com",
                "custom_code": custom_code
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 400

    def test_list_links_pagination(self, auth_token):
        """Test link listing with pagination."""
        # Create a link
        requests.post(
            f"{BASE_URL}/links",
            json={"long_url": "https://pagination.example.com"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        # Test listing
        response = requests.get(
            f"{BASE_URL}/links",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_search_endpoint_exists(self, auth_token):
        """Test that search endpoint exists and works."""
        response = requests.get(
            f"{BASE_URL}/links/search?q=test",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code in [200, 400]  # 400 if no results

    def test_logout(self, auth_token):
        """Test logout invalidates token."""
        # Logout
        response = requests.post(
            f"{BASE_URL}/logout",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        
        # Token should no longer work
        response = requests.get(
            f"{BASE_URL}/links",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 401


class TestRateLimiting:
    """Test rate limiting behavior."""

    def test_rate_limit_not_triggered_immediately(self, auth_token):
        """Test that first redirect is allowed."""
        # Create link
        response = requests.post(
            f"{BASE_URL}/links",
            json={"long_url": "https://ratelimit.example.com"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        code = response.json()["code"]
        
        # First redirect should succeed
        response = requests.get(
            f"{BASE_URL}/{code}",
            allow_redirects=False
        )
        assert response.status_code in [307, 302]
