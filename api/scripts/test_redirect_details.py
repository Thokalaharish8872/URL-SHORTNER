import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def test_redirect_details():
    # 1. Create a link
    print("Creating link...")
    long_url = "https://example.com/path?query=1#fragment"
    payload = {"long_url": long_url}
    resp = requests.post(f"{BASE_URL}/links", json=payload)
    code = resp.json()["code"]
    print(f"Code: {code}")

    # 2. Inspect redirect
    print("\nInspecting redirect...")
    resp = requests.get(f"{BASE_URL}/{code}", allow_redirects=False)
    print(f"Status Code: {resp.status_code}")
    print(f"Location Header: {resp.headers.get('Location')}")
    
    if resp.status_code in [301, 302, 307, 308]:
        print("SUCCESS: Proper redirect status code")
    else:
        print(f"FAILURE: Expected redirect status, got {resp.status_code}")
        
    if resp.headers.get('Location') == long_url:
        print("SUCCESS: Location header matches original URL")
    else:
        print(f"FAILURE: Location header mismatch. Expected {long_url}, got {resp.headers.get('Location')}")

if __name__ == "__main__":
    test_redirect_details()
