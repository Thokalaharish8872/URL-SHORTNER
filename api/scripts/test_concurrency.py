import requests
import concurrent.futures
import time

BASE_URL = "http://127.0.0.1:8000"

def create_link(custom_code):
    payload = {
        "long_url": "https://example.com/concurrency",
        "custom_code": custom_code
    }
    resp = requests.post(f"{BASE_URL}/links", json=payload)
    return resp.status_code

def test_concurrency():
    print("Testing concurrency on duplicate custom code...")
    custom_code = f"race-{int(time.time())}"
    
    # Send 10 simultaneous requests for the SAME custom code
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda _: create_link(custom_code), range(10)))
        
    print(f"Results: {results}")
    
    success_count = results.count(200)
    conflict_count = results.count(400)
    
    print(f"Success (200): {success_count}")
    print(f"Conflict (400): {conflict_count}")
    
    if success_count == 1:
        print("SUCCESS: Atomic constraint enforced correctly under concurrency")
    else:
        print(f"FAILURE: Expected exactly 1 success, got {success_count}!")

if __name__ == "__main__":
    test_concurrency()
