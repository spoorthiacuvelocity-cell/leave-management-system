from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str
    gender: str
    manager_id: Optional[int] = None