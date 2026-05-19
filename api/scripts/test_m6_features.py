import httpx
import time

BASE_URL = "http://127.0.0.1:8000"

def test_graceful_fallback():
    print("Testing graceful fallback (assuming Redis is down)...")
    client = httpx.Client(timeout=10.0)
    
    # 1. Create a link
    print("Registering (might fail if exists)...")
    reg = client.post(f"{BASE_URL}/register", json={"email": "test@example.com", "password": "password123"})
    print(f"Register status: {reg.status_code}")
    
    print("Logging in...")
    response = client.post(f"{BASE_URL}/login", data={"username": "test@example.com", "password": "password123"})
    if response.status_code != 200:
        print(f"Login failed: {response.status_code} - {response.text}")
        return
        
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    print("Creating link...")
    link_in = {"long_url": "https://google.com", "custom_code": "m6test"}
    l_res = client.post(f"{BASE_URL}/links", json=link_in, headers=headers)
    print(f"Link creation status: {l_res.status_code}")
    
    # 2. Try to redirect
    print("Requesting redirect...")
    start_time = time.time()
    response = client.get(f"{BASE_URL}/m6test", follow_redirects=False)
    duration = time.time() - start_time
    
    print(f"Status: {response.status_code}")
    print(f"Location: {response.headers.get('location')}")
    print(f"Duration: {duration:.4f}s")
    
    if response.status_code == 307 and response.headers.get("location") == "https://google.com":
        print(" SUCCESS: Redirect worked even if Redis is down.")
    else:
        print(" FAILURE: Redirect failed.")

if __name__ == "__main__":
    test_graceful_fallback()
