from sqlalchemy import select
from app.db import SessionLocal
from app.models import Link
from sqlalchemy.exc import IntegrityError

CODE = "conflict-test"
LONG_URL_1 = "https://example.com/1"
LONG_URL_2 = "https://example.com/2"
OWNER = "demo-owner"

def main() -> None:
    # 1. Clean up
    with SessionLocal() as session:
        session.query(Link).filter(Link.code == CODE).delete()
        session.commit()

    # 2. First insert
    print(f"Attempting first insert of code: {CODE}")
    try:
        with SessionLocal() as session:
            link1 = Link(code=CODE, long_url=LONG_URL_1, created_by=OWNER)
            session.add(link1)
            session.commit()
            print("First insert SUCCESS")
    except Exception as e:
        print(f"First insert FAILED: {e}")
        return

    # 3. Second insert (Conflict!)
    print(f"\nAttempting second insert of SAME code: {CODE}")
    try:
        with SessionLocal() as session:
            link2 = Link(code=CODE, long_url=LONG_URL_2, created_by=OWNER)
            session.add(link2)
            session.commit()
            print("Second insert SUCCESS (Wait, this should have failed!)")
    except IntegrityError:
        print("Second insert FAILED with IntegrityError (Expected behavior)")
    except Exception as e:
        print(f"Second insert FAILED with unexpected error: {e}")

if __name__ == "__main__":
    main()
