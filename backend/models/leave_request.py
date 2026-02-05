from sqlalchemy import (
    Column, Integer, String, Date, DateTime, Text, Boolean, ForeignKey
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database.postgres import Base


class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    leave_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    leave_type = Column(String(30), nullable=False)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    number_of_days = Column(Integer, nullable=False)

    status = Column(String(20), default="PENDING")
    reason = Column(Text)

    applied_on = Column(DateTime(timezone=True), server_default=func.now())

    approved_by = Column(Integer, ForeignKey("users.user_id"))
    approved_on = Column(DateTime(timezone=True))

    rejected_on = Column(DateTime(timezone=True))
    cancelled_on = Column(DateTime(timezone=True))

    proof_uploaded = Column(Boolean, default=False)
    proof_document_path = Column(String(255))

    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    approver = relationship("User", foreign_keys=[approved_by])
