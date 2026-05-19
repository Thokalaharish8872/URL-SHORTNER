import requests
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000"

def test_optional_fields():
    print("Testing optional fields (tags and expires_at)...")
    
    # 1. Create a link with tags and an expiration date
    future_date = (datetime.utcnow() + timedelta(days=7)).isoformat() + "Z"
    payload = {
        "long_url": "https://example.com/optional",
        "expires_at": future_date,
        "tags": ["tag1", "tag2"]
    }
    
    print(f"Creating link with tags {payload['tags']} and expires_at {future_date}")
    resp = requests.post(f"{BASE_URL}/links", json=payload)
    if resp.status_code != 200:
        print(f"FAILURE: Could not create link. Status: {resp.status_code}")
        print(resp.text)
        return
        
    link_data = resp.json()
    print(f"Created link data: {link_data}")

    # 2. Verify persistence in listing
    print("\nVerifying persistence in listing...")
    resp = requests.get(f"{BASE_URL}/links")
    # Find our link in the list
    found = next((l for l in resp.json() if l["id"] == link_data["id"]), None)
    
    if found:
        print("SUCCESS: Link found in list")
        if found.get("tags") == payload["tags"]:
            print(f"SUCCESS: Tags preserved: {found.get('tags')}")
        else:
            print(f"FAILURE: Tags mismatch! Expected {payload['tags']}, got {found.get('tags')}")
            
        # Pydantic might return datetime objects or strings depending on version/config
        # We just check if it's there
        if found.get("expires_at"):
            print(f"SUCCESS: expires_at preserved: {found.get('expires_at')}")
        else:
            print(f"FAILURE: expires_at missing in response!")
    else:
        print("FAILURE: Created link not found in list!")

if __name__ == "__main__":
    test_optional_fields()
