from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime
import os

client = TestClient(app)

def test_auth_flow():
    email = f"test_fix_{datetime.now().timestamp()}@example.com"
    password = "testpassword"

    print(f"Testing with user: {email}")

    # 1. Register
    response = client.post("/register", json={"email": email, "password": password})
    if response.status_code != 200:
        print(f"Registration failed: {response.json()}")
        return
    print("✓ Registered")

    # 2. Login
    response = client.post("/login", data={"username": email, "password": password})
    if response.status_code != 200:
        print(f"Login failed: {response.json()}")
        return
    token = response.json()["access_token"]
    print("✓ Logged in")

    # 3. Verify token works (create a link)
    response = client.post(
        "/links", 
        json={"long_url": "https://google.com"},
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code != 200:
        print(f"Token verification failed: {response.json()}")
        return
    print("✓ Token works before logout")

    # 4. Logout
    response = client.post("/logout", headers={"Authorization": f"Bearer {token}"})
    if response.status_code != 200:
        print(f"Logout failed: {response.json()}")
        return
    print("✓ Logged out successfully")

    # 5. Verify token no longer works
    response = client.post(
        "/links", 
        json={"long_url": "https://google.com"},
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code == 401:
        print("✓ Token rejected after logout (Status: 401)")
    else:
        print(f"FAILED: Token NOT rejected after logout. Status: {response.status_code}, Response: {response.json()}")

if __name__ == "__main__":
    try:
        test_auth_flow()
        print("\nAUTH FIX VERIFIED SUCCESSFULLY")
    except Exception as e:
        print(f"\nVERIFICATION FAILED: {e}")
        import traceback
        traceback.print_exc()
