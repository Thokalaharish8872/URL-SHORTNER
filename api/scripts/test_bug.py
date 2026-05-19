from sqlalchemy import select
from app.db import SessionLocal
from app.models import Link

CODE = "break-test-1"
LONG_URL = "https://example.com/break"
OWNER = "demo-owner"

def main() -> None:
    try:
        with SessionLocal() as session:
            new_link = Link(code=CODE, long_url=LONG_URL, created_by=OWNER, tags=["break-test"])
            session.add(new_link)
            session.commit()
            print("Successfully inserted new link")
            
            selected = session.execute(select(Link).where(Link.code == CODE)).scalar_one()
            print(f"Verified: {selected.code}")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    main()
