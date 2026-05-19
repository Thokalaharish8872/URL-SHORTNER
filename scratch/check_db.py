from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv("api/.env")
db_url = os.getenv("DATABASE_URL")
print(f"Connecting to: {db_url}")

try:
    engine = create_engine(db_url)
    with engine.connect() as conn:
        print("Successfully connected to the database!")
except Exception as e:
    print(f"Failed to connect: {e}")
