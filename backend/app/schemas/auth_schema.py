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
from pydantic import BaseModel, EmailStr


class ForgotPasswordSchema(BaseModel):
    email: EmailStr


class ResetPasswordSchema(BaseModel):
    token: str
    new_password: str