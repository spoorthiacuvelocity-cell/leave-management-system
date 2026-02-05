from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# =========================
# Base schema
# =========================
class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: Optional[str] = None
    role: str


# =========================
# Create user
# =========================
class UserCreate(UserBase):
    pass


# =========================
# Response schema
# =========================
class UserResponse(UserBase):
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
