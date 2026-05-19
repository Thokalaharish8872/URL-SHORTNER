import requests
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def test_auth_flow():
    email = f"test_fix_{datetime.now().timestamp()}@example.com"
    password = "testpassword"

    print(f"Testing with user: {email}")

    # 1. Register
    response = requests.post(f"{BASE_URL}/register", json={"email": email, "password": password})
    if response.status_code != 200:
        print(f"Registration failed: {response.json()}")
        return
    print("✓ Registered")

    # 2. Login
    response = requests.post(f"{BASE_URL}/login", data={"username": email, "password": password})
    if response.status_code != 200:
        print(f"Login failed: {response.json()}")
        return
    token = response.json()["access_token"]
    print("✓ Logged in")

    # 3. Verify token works (create a link)
    response = requests.post(
        f"{BASE_URL}/links", 
        json={"long_url": "https://google.com"},
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code != 200:
        print(f"Token verification failed: {response.json()}")
        return
    print("✓ Token works before logout")

    # 4. Logout
    response = requests.post(f"{BASE_URL}/logout", headers={"Authorization": f"Bearer {token}"})
    if response.status_code != 200:
        print(f"Logout failed: {response.json()}")
        return
    print("✓ Logged out successfully")

    # 5. Verify token no longer works
    response = requests.post(
        f"{BASE_URL}/links", 
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
