'''
Used to validate requests/responses
'''

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class PostCreate(BaseModel):
    content: str

class PostResponse(BaseModel):
    id: int
    user_id: int
    content: str
    media_url: Optional[str] = None
    timestamp: datetime

    class Config:
        orm_mode = True