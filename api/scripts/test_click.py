from sqlalchemy import select
from app.db import SessionLocal
from app.models import Link, ClickEvent
from datetime import datetime

CODE = "click-test"
LONG_URL = "https://example.com/click"
OWNER = "demo-owner"

def main() -> None:
    try:
        with SessionLocal() as session:
            # Create link
            link = Link(code=CODE, long_url=LONG_URL, created_by=OWNER)
            session.add(link)
            session.commit()
            
            # Create click event
            click = ClickEvent(link_id=link.id, ip_hash="abc", user_agent="test")
            session.add(click)
            session.commit()
            print("Successfully inserted link and click event")
            
            # Query back
            selected = session.execute(
                select(Link).join(ClickEvent).where(Link.code == CODE)
            ).scalar_one()
            print(f"Verified link with click: {selected.code}")
            
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    main()
