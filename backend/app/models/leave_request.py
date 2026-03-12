from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
from backend.database.postgres import Base


class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)

    leave_type = Column(String, nullable=False)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    reason = Column(String)

    status = Column(String, default="Pending")

    user_id = Column(Integer, ForeignKey("users.id"))

    proof_document = Column(String, nullable=True)

    number_of_days = Column(Integer, nullable=False)

    remarks = Column(Text, nullable=True)

    # Approval tracking
    approved_by = Column(Integer, nullable=True)
    approved_by_role = Column(String, nullable=True)
    approved_on = Column(DateTime(timezone=True), nullable=True)

    # Time tracking
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )