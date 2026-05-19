import requests
import sys

BASE_URL = "http://localhost:8000"

def test_session_invalidation():
    # 1. Register a new user
    user_data = {"email": "bugtest@example.com", "password": "password123"}
    print(f"Registering user: {user_data['email']}...")
    resp = requests.post(f"{BASE_URL}/register", json=user_data)
    if resp.status_code != 200 and "already registered" not in resp.text:
        print(f"Registration failed: {resp.text}")
        return

    # 2. Login to get a token
    print("Logging in...")
    resp = requests.post(f"{BASE_URL}/login", data={"username": user_data["email"], "password": user_data["password"]})
    if resp.status_code != 200:
        print(f"Login failed: {resp.text}")
        return
    
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"Token acquired: {token[:20]}...")

    # 3. Verify access works
    print("Verifying access works...")
    link_data = {"long_url": "https://google.com"}
    resp = requests.post(f"{BASE_URL}/links", json=link_data, headers=headers)
    if resp.status_code == 200:
        print("Success: Initial access works.")
    else:
        print(f"Error: Initial access failed: {resp.text}")
        return

    # 4. Logout
    print("Logging out...")
    resp = requests.post(f"{BASE_URL}/logout", headers=headers)
    if resp.status_code == 200:
        print("Success: Logged out.")
    else:
        print(f"Error: Logout failed: {resp.text}")
        return

    # 5. Verify access is DENIED (This is where the bug should show up)
    print("Verifying access is denied after logout...")
    resp = requests.post(f"{BASE_URL}/links", json=link_data, headers=headers)
    
    if resp.status_code == 401:
        print("VERIFICATION PASSED: Access was denied after logout. (No bug)")
    else:
        print(f"VERIFICATION FAILED: Access was GRANTED after logout (Status: {resp.status_code}).")
        print("!!! SECURITY VULNERABILITY DETECTED: Sessions are not being invalidated in the DB. !!!")

if __name__ == "__main__":
    test_session_invalidation()
