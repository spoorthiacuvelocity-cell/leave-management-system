from pydantic import BaseModel, EmailStr
from typing import Optional

class RegisterSchema(BaseModel):
    name: str
    email: str
    password: str
    role: str
    gender: str
    manager_id: Optional[int] = None

class LoginSchema(BaseModel):
    email: EmailStr
    password: str
