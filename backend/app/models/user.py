from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from backend.database.postgres import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    phone_number: Column[str] = Column(String(15))
    role = Column(String(20), nullable=False)  # EMPLOYEE / ADMIN

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
