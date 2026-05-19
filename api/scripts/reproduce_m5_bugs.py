from fastapi.testclient import TestClient
from app.main import app
import os
import sys

# Add the parent directory to sys.path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

client = TestClient(app)

def test_repro_bugs():
    print("--- 1. Testing Authentication Bypass on GET /links ---")
    response = client.get("/links")
    if response.status_code == 200:
        print("BUG REPRODUCED: GET /links is accessible without authentication!")
        print(f"Response: {response.json()[:2]} ...") # Show only first 2 items
    else:
        print(f"GET /links returned {response.status_code}. If this is 401, the bug might be fixed.")

    print("\n--- 2. Testing Stack Trace Leak and Request ID ---")
    # Trigger an error by accessing a non-existent link and forcing log_click to fail (which it currently does)
    # Actually, let's create a link first so we can try to redirect to it
    
    # Need to register/login for this if we want to be clean, but let's just trigger a generic error
    # The log_click failure in redirect_to_link will happen if the link exists.
    # But wait, let's just try to create a link without a required field to trigger a validation error if possible,
    # or just rely on the log_click failure.
    
    # Create a link first
    reg_response = client.post("/register", json={"email": "repro@example.com", "password": "password"})
    login_response = client.post("/login", data={"username": "repro@example.com", "password": "password"})
    token = login_response.json()["access_token"]
    
    link_response = client.post(
        "/links", 
        json={"long_url": "https://example.com", "custom_code": "repro-link"},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if link_response.status_code != 200:
        print(f"Failed to create link for testing: {link_response.json()}")
    else:
        print("Link created. Triggering redirect to test log_click failure...")
        # Trigger redirect which calls log_click
        redirect_response = client.get("/repro-link", follow_redirects=False)
        
        if redirect_response.status_code == 500:
            content = redirect_response.json()
            error = content.get("error", {})
            print("✓ Caught 500 error as expected.")
            
            if "stack_trace" in error:
                print("BUG REPRODUCED: Stack trace is present in the response!")
                # print(f"Stack trace sample: {error['stack_trace'][:100]}...")
            else:
                print("Stack trace is NOT present in the response.")
                
            if error.get("request_id") == "TODO":
                print("BUG REPRODUCED: request_id is still 'TODO'!")
            else:
                print(f"request_id is: {error.get('request_id')}")
        else:
            print(f"Redirect returned {redirect_response.status_code}, expected 500 due to log_click failure.")

if __name__ == "__main__":
    test_repro_bugs()
