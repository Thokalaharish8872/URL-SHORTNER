import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def test_flow():
    # 1. Create a link
    print("Creating link...")
    payload = {
        "long_url": "https://www.google.com",
        "tags": ["search", "test"]
    }
    resp = requests.post(f"{BASE_URL}/links", json=payload)
    print(f"Status: {resp.status_code}")
    link_data = resp.json()
    print(f"Response: {link_data}")
    code = link_data["code"]

    # 2. List links
    print("\nListing links...")
    resp = requests.get(f"{BASE_URL}/links")
    print(f"Status: {resp.status_code}")
    print(f"Total links: {len(resp.json())}")

    # 3. Test redirect
    print(f"\nTesting redirect for code: {code}")
    # We use allow_redirects=False to verify the 307/302 response
    resp = requests.get(f"{BASE_URL}/{code}", allow_redirects=False)
    print(f"Status: {resp.status_code}")
    print(f"Location: {resp.headers.get('Location')}")

if __name__ == "__main__":
    test_flow()
