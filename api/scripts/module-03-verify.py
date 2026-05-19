import requests
import time
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker
import sys
import os

# Add the project root to sys.path to import app
sys.path.append(os.getcwd())

from app.models import ClickEvent

# Database setup for verification
DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/upsk_sdf"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

BASE_URL = "http://127.0.0.1:8000"

def verify():
    # 1. Conflict Handling: Duplicate Custom Code
    print("Testing Conflict Handling...")
    custom_code = f"custom-{int(time.time())}"
    payload = {"long_url": "https://example.com/1", "custom_code": custom_code}
    
    # First insert
    requests.post(f"{BASE_URL}/links", json=payload)
    
    # Second insert (Duplicate)
    resp = requests.post(f"{BASE_URL}/links", json=payload)
    print(f"Duplicate Insert Status: {resp.status_code}")
    if resp.status_code == 400:
        print("SUCCESS: Duplicate custom code blocked with 400")
    else:
        print(f"FAILURE: Expected 400, got {resp.status_code}")

    # 2. Analytics Logging: ClickEvent Creation
    print("\nTesting Analytics Logging...")
    with SessionLocal() as db:
        # Get current click count
        before_count = db.execute(select(func.count(ClickEvent.id))).scalar() or 0
        print(f"Clicks before redirect: {before_count}")
        
        # Trigger redirect
        requests.get(f"{BASE_URL}/{custom_code}", allow_redirects=False)
        
        # Get new click count
        after_count = db.execute(select(func.count(ClickEvent.id))).scalar() or 0
        print(f"Clicks after redirect: {after_count}")
        
        if after_count == before_count + 1:
            print("SUCCESS: ClickEvent successfully logged in database")
        else:
            print("FAILURE: ClickEvent count did not increment")

if __name__ == "__main__":
    verify()
