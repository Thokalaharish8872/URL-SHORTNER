from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, HttpUrl, Field

class LinkBase(BaseModel):
    long_url: HttpUrl
    expires_at: Optional[datetime] = None
    tags: Optional[List[str]] = Field(default_factory=list)

class LinkCreate(LinkBase):
    custom_code: Optional[str] = Field(None, min_length=3, max_length=64)

class LinkRead(LinkBase):
    id: int
    code: str
    created_at: datetime
    created_by: str

    class Config:
        from_attributes = True

class ClickEventRead(BaseModel):
    id: int
    link_id: int
    clicked_at: datetime
    user_agent: Optional[str]
    referrer: Optional[str]
    ip_hash: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: str
    password: str


class UserRead(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
