from sqlalchemy import select

from app.db import SessionLocal
from app.models import Link


CODE = "hello123"
LONG_URL = "https://example.com/hello"
OWNER = "demo-owner"


def main() -> None:
    with SessionLocal() as session:
        existing = session.execute(select(Link).where(Link.code == CODE)).scalar_one_or_none()
        if existing is None:
            existing = Link(code=CODE, long_url=LONG_URL, created_by=OWNER, tags=["demo", "module-02"])
            session.add(existing)
            session.commit()

        selected = session.execute(select(Link).where(Link.code == CODE)).scalar_one()

        print(f"inserted code: {CODE}")
        print(f"selected code: {selected.code}")
        print(f"matched long_url: {selected.long_url}")


if __name__ == "__main__":
    main()
