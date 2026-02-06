from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from backend.database.postgres import Base


class LeaveBalance(Base):
    __tablename__ = "leave_balance"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    total_leaves = Column(Integer, default=10)
    used_leaves = Column(Integer, default=0)
    remaining_leaves = Column(Integer, default=10)

    user = relationship("User", backref="leave_balance")
