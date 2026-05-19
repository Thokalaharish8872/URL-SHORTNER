from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from sqlalchemy import text

from app.config import settings


engine = create_engine(settings.database_url, future=True, connect_args={"connect_timeout": 5})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    try:
        db = SessionLocal()
        # Test connection
        db.execute(text("SELECT 1"))
        yield db
    except Exception as e:
        # Return None if database is not available
        yield None
    finally:
        try:
            if 'db' in locals() and db:
                db.close()
        except:
            pass
