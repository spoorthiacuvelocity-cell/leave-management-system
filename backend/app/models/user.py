from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from backend.database.postgres import Base
class User(Base):
    __tablename__ = "users"
    is_active = Column(Boolean, default=True, nullable=False)
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    gender = Column(String, nullable=True)
    resignation_date = Column(Date, nullable=True)
    resignation_reason = Column(String, nullable=True)
    last_working_day = Column(Date, nullable=True)
    resignation_approval_date = Column(Date, nullable=True)
    resignation_status = Column(String(20), nullable=True)
    # 🔥 Team-based manager system
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
