from sqlalchemy import Column, Integer, Date, ForeignKey, Enum, String
from sqlalchemy.orm import relationship
import enum

from backend.database.postgres import Base


class LeaveStatus(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(String)

    status = Column(Enum(LeaveStatus), default=LeaveStatus.PENDING)

    # 🔥 NEW FIELDS
    approved_by_role = Column(String, nullable=True)  # PROJECT_MANAGER / ADMIN
    approved_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = relationship("User", foreign_keys=[user_id])
    approver = relationship("User", foreign_keys=[approved_by_id])
