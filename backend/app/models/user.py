from sqlalchemy import Column, Integer, String, ForeignKey
from backend.database.postgres import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    gender = Column(String, nullable=True)

    # 🔥 Team-based manager system
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
