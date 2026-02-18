from pydantic import BaseModel, EmailStr


class RegisterSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
    gender: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str
