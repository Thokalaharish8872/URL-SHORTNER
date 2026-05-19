import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def test_encoding():
    # 1. Create a link with complex characters
    print("Testing complex URL encoding...")
    long_url = "https://example.com/search?q=fastapi+%26+sqlalchemy&lang=en#results_1"
    payload = {"long_url": long_url}
    
    print(f"Creating link for: {long_url}")
    resp = requests.post(f"{BASE_URL}/links", json=payload)
    if resp.status_code != 200:
        print(f"FAILURE: Could not create link. Status: {resp.status_code}")
        print(resp.text)
        return
        
    code = resp.json()["code"]
    print(f"Created code: {code}")

    # 2. Verify redirect
    print("\nVerifying redirect...")
    # allow_redirects=False to catch the Location header
    resp = requests.get(f"{BASE_URL}/{code}", allow_redirects=False)
    location = resp.headers.get("Location")
    print(f"Redirect Status: {resp.status_code}")
    print(f"Redirect Location: {location}")
    
    if location == long_url:
        print("SUCCESS: Complex URL preserved exactly")
    else:
        print(f"FAILURE: URL mismatch!")
        print(f"Expected: {long_url}")
        print(f"Actual:   {location}")

if __name__ == "__main__":
    test_encoding()
