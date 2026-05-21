from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
import traceback

from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone

from app.db import get_db
from app.schemas import LinkCreate, LinkRead, UserCreate, UserRead, Token
from app.services import LinkService, AuthService
from app.config import settings
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


app = FastAPI(title="Upsk SDF URL Shortener")


import uuid

@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        request_id = str(uuid.uuid4())
        # Log the error with request_id for internal debugging
        print(f"Error ID: {request_id}")
        print(traceback.format_exc())
        
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred. Please contact support.",
                    "request_id": request_id
                }
            },
        )



@app.get("/health")
def health_check():
    return {"status": "ok"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = AuthService.validate_session(db, token)
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired session",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id

@app.post("/register", response_model=UserRead)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    
    try:
        if db is None:
            raise HTTPException(status_code=503, detail="Database unavailable")
        return AuthService.create_user(db, user_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")
    user = AuthService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = AuthService.create_access_token(db, data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/logout")
def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")
    AuthService.logout(db, token)
    return {"message": "Successfully logged out"}

@app.post("/links", response_model=LinkRead)
def create_link(link_in: LinkCreate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user)):
    print(f"Creating link for user_id: {current_user_id} with data: {link_in}")
    try:
        if db is None:
            raise HTTPException(status_code=503, detail="Database unavailable")
        return LinkService.create_link(db, link_in, str(current_user_id))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/links", response_model=List[LinkRead])
def list_links(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user)):
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")
    return LinkService.list_links(db, creator=str(current_user_id), skip=skip, limit=limit)

@app.get("/links/search", response_model=List[LinkRead])
def search_links(q: str = "", skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user)):
    """Search links by code, URL, or tags using PostgreSQL full-text search."""
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")
    if not q:
        raise HTTPException(status_code=400, detail="Search query 'q' is required")
    try:
        # Try FTS first
        return LinkService.search_links(db, query_text=q, creator=str(current_user_id), skip=skip, limit=limit)
    except Exception:
        # Fallback to simple ILIKE search
        return LinkService.search_links_simple(db, query_text=q, creator=str(current_user_id), skip=skip, limit=limit)

@app.get("/{code}")
def redirect_to_link(code: str, request: Request, db: Session = Depends(get_db)):
    # Check rate limit first (the twist)
    if not LinkService.check_rate_limit(code):
        raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")

    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")
    link = LinkService.get_link_by_code(db, code)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    # Check for expiration
    if link.expires_at and link.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=410, detail="Link has expired")
    
    # Log the click asynchronously (simple hash for IP for privacy)
    ip_hash = hash(request.client.host) if request.client else "unknown"
    LinkService.log_click_sync(
    db=db,
    link_id=link.id,
    ip_hash=str(ip_hash),
    user_agent=request.headers.get("user-agent"),
    referrer=request.headers.get("referer")
)
    
    return RedirectResponse(url=link.long_url)
