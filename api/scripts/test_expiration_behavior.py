import requests
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000"

def test_expiration_behavior():
    print("Testing behavior of expired links...")
    
    # 1. Create a link that expired 1 hour ago
    expired_date = (datetime.utcnow() - timedelta(hours=1)).isoformat() + "Z"
    payload = {
        "long_url": "https://example.com/expired",
        "expires_at": expired_date
    }
    
    print(f"Creating link that expired at: {expired_date}")
    resp = requests.post(f"{BASE_URL}/links", json=payload)
    code = resp.json()["code"]
    
    # 2. Try to redirect
    print(f"Attempting to redirect to expired code: {code}")
    resp = requests.get(f"{BASE_URL}/{code}", allow_redirects=False)
    print(f"Status Code: {resp.status_code}")
    
    if resp.status_code == 307:
        print("ALERT: Expired link still redirects! This might be our bug.")
    elif resp.status_code in [404, 410]:
        print(f"SUCCESS: Expired link correctly returns {resp.status_code}")
    else:
        print(f"Unexpected status code: {resp.status_code}")

if __name__ == "__main__":
    test_expiration_behavior()
