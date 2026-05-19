import requests

BASE_URL = "http://127.0.0.1:8000"

def test_pagination():
    print("Testing pagination...")
    
    # 1. Get total links
    resp = requests.get(f"{BASE_URL}/links")
    all_links = resp.json()
    total = len(all_links)
    print(f"Total links: {total}")
    
    if total < 2:
        print("Creating more links for pagination test...")
        for i in range(3):
            requests.post(f"{BASE_URL}/links", json={"long_url": f"https://example.com/{i}"})
        resp = requests.get(f"{BASE_URL}/links")
        all_links = resp.json()
        total = len(all_links)
        print(f"New total: {total}")

    # 2. Test skip/limit
    limit = 2
    resp = requests.get(f"{BASE_URL}/links?skip=0&limit={limit}")
    page1 = resp.json()
    print(f"Page 1 (limit={limit}): {len(page1)} links")
    
    resp = requests.get(f"{BASE_URL}/links?skip=2&limit={limit}")
    page2 = resp.json()
    print(f"Page 2 (skip=2, limit={limit}): {len(page2)} links")
    
    if len(page1) == limit and len(page2) > 0:
        print("SUCCESS: Pagination seems working")
    else:
        print("FAILURE: Pagination anomaly detected")

if __name__ == "__main__":
    test_pagination()
