import random
import string
import os
from datetime import datetime, timedelta, timezone
import json
from typing import Optional, List
from app.redis_client import RedisClient
import bcrypt
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Link, ClickEvent, User, SessionToken
from app.schemas import LinkCreate, UserCreate
from sqlalchemy.exc import IntegrityError
from jose import jwt, JWTError

from sqlalchemy import or_


# Auth Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-for-dev-only")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def get_password_hash(password: str):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    @staticmethod
    def create_access_token(db: Session, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        # Store in DB for stateful validation
        session = SessionToken(
            token=encoded_jwt,
            user_id=data["sub"],
            expires_at=expire
        )
        db.add(session)
        db.commit()
        
        return encoded_jwt

    @staticmethod
    def create_user(db: Session, user_in: UserCreate) -> User:
        hashed_password = AuthService.get_password_hash(user_in.password)
        user = User(email=user_in.email, hashed_password=hashed_password)
        db.add(user)
        try:
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError:
            db.rollback()
            raise ValueError("Email already registered")

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        user = db.execute(select(User).where(User.email == email)).scalar_one_or_none()
        if not user:
            return None
        if not AuthService.verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def validate_session(db: Session, token: str) -> Optional[int]:
        session = db.execute(
            select(SessionToken).where(SessionToken.token == token)
        ).scalar_one_or_none()

        if not session:
            return None

        if session.expires_at < datetime.utcnow():
            db.delete(session)
            db.commit()
            return None

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload.get("sub")
        except JWTError:
            return None

    @staticmethod
    def logout(db: Session, token: str):
        session = db.execute(select(SessionToken).where(SessionToken.token == token)).scalar_one_or_none()
        if session:
            db.delete(session)
            db.commit()


class LinkService:
    @staticmethod
    def generate_code(length: int = 6) -> str:
        chars = string.ascii_letters + string.digits
        return "".join(random.choice(chars) for _ in range(length))

    @staticmethod
    def create_link(db: Session, link_in: LinkCreate, creator: str) -> Link:
        # If custom code is provided, try to use it
        if link_in.custom_code:
            # Invalidate cache for this custom code to prevent stale data
            cache_key = f"link:{link_in.custom_code}"
            # RedisClient.delete(cache_key)
            
            link = Link(
                code=link_in.custom_code,
                long_url=str(link_in.long_url),
                created_by=creator,
                expires_at=link_in.expires_at,
                tags=link_in.tags
            )
            db.add(link)
            try:
                db.commit()
                db.refresh(link)
                return link
            except IntegrityError:
                db.rollback()
                raise ValueError(f"Custom code '{link_in.custom_code}' already exists.")

        # Otherwise generate a code with retries
        max_retries = 5
        for _ in range(max_retries):
            code = LinkService.generate_code()
            link = Link(
                code=code,
                long_url=str(link_in.long_url),
                created_by=creator,
                expires_at=link_in.expires_at,
                tags=link_in.tags
            )
            db.add(link)
            try:
                db.commit()
                db.refresh(link)
                return link
            except IntegrityError:
                db.rollback()
                continue
        
        raise RuntimeError("Failed to generate a unique short code after several retries.")

    @staticmethod
    def get_link_by_code(db: Session, code: str) -> Optional[Link]:
        # Check cache first
        cache_key = f"link:{code}"
        cached_data = RedisClient.get(cache_key)
        
        if cached_data:
            try:
                data = json.loads(cached_data)
                # Reconstruct a Link object (or a mock that looks like it)
                return Link(
                    id=data["id"],
                    code=data["code"],
                    long_url=data["long_url"],
                    expires_at=datetime.fromisoformat(data["expires_at"]).replace(tzinfo=timezone.utc) if data.get("expires_at") else None
                )
            except Exception:
                # If cache is malformed, fallback to DB
                pass

        # Fallback to DB
        link = db.execute(select(Link).where(Link.code == code)).scalar_one_or_none()
        
        if link:
            # Populate cache
            link_data = {
                "id": link.id,
                "code": link.code,
                "long_url": link.long_url,
                "expires_at": link.expires_at.isoformat() if link.expires_at else None
            }
            RedisClient.set(cache_key, json.dumps(link_data), ex=3600)
            
        return link

    @staticmethod
    def check_rate_limit(code: str, limit: int = 10, window: int = 60) -> bool:
        """
        Simple fixed-window rate limiter using Redis.
        Returns True if allowed, False if rate limited.
        """
        key = f"ratelimit:redirect:{code}"
        count = RedisClient.incr(key, ex=window)
        
        if count is None:
            # Redis is down, allow it (graceful degradation)
            return True
            
        return count <= limit

    @staticmethod
    def log_click_async(link_id: int, ip_hash: str, user_agent: Optional[str] = None, referrer: Optional[str] = None):
        """
        Enqueue click event for async processing.
        Falls back to synchronous logging if queue is unavailable.
        """
        try:
            from app.tasks import log_click_event
            # Enqueue async task
            task = log_click_event.delay(link_id, ip_hash, user_agent, referrer)
            print(f"Click event enqueued: task_id={task.id}")
            return task
        except Exception as e:
            print(f"Failed to enqueue click event, falling back to sync: {e}")
            # Fallback to synchronous logging
            return LinkService.log_click_sync(link_id, ip_hash, user_agent, referrer)

    @staticmethod
    def log_click_sync(db: Session, link_id: int, ip_hash: str, user_agent: Optional[str] = None, referrer: Optional[str] = None) -> ClickEvent:
        """
        Synchronous click logging fallback.
        """
        click = ClickEvent(
            link_id=link_id,
            ip_hash=ip_hash,
            user_agent=user_agent,
            referrer=referrer
        )
        db.add(click)
        db.commit()
        return click

    @staticmethod
    def list_links(db: Session, creator: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[Link]:
        query = select(Link)
        if creator:
            query = query.where(Link.created_by == creator)
        return list(db.execute(query.offset(skip).limit(limit)).scalars().all())

    @staticmethod
    def search_links(db: Session, query_text: str, creator: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[Link]:
        """
        Search links using PostgreSQL full-text search.
        Searches in code, long_url, and tags using search_vector column.
        """
        from sqlalchemy import text

        
        # Use the precomputed search_vector column with GIN index for fast search
        search_query = text("""
            SELECT * FROM links 
            WHERE (
                search_vector @@ plainto_tsquery('english', :query)
            )
            {creator_filter}
            ORDER BY created_at DESC
            OFFSET :skip
            LIMIT :limit
        """.format(
            creator_filter="AND created_by = :creator" if creator else ""
        ))

        params = {"query": query_text, "skip": skip, "limit": limit}
        if creator:
            params["creator"] = creator
            
        result = db.execute(search_query, params)

        rows = result.fetchall()

        
        if not rows:
            raise Exception("No search results found")
        return [Link(**row._mapping) for row in result]

    @staticmethod
    def search_links_simple(db: Session, query_text: str, creator: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[Link]:
        print("came here 1")

        """
        Simple case-insensitive search using ILIKE.
        Fallback when FTS is not available.
        """
        search_pattern = f"%{query_text}%"
        query = select(Link).where(
            or_(
                Link.code.ilike(search_pattern),
                Link.long_url.ilike(search_pattern),
            )
        )
        print("came here 2")

        if creator:
            query = query.where(Link.created_by == creator)
        print("came here ")
        return list(db.execute(query.offset(skip).limit(limit)).scalars().all())
