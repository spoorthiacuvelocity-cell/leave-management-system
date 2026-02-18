from sqlalchemy import Column, Integer, String, Boolean, Numeric, TIMESTAMP
from sqlalchemy.sql import func
from backend.database import Base

class LeaveType(Base):
    __tablename__ = "leave_types"

    leave_type_id = Column(Integer, primary_key=True, index=True)
    leave_name = Column(String(50), unique=True, nullable=False)
    leaves_per_quarter = Column(Numeric(3,1))
    max_consecutive_leaves = Column(Integer)
    notice_period_days = Column(Integer, default=0)
    proof_required = Column(Boolean, default=False)
    proof_required_after_days = Column(Integer)
    gender_specific = Column(String(10))
    created_at = Column(TIMESTAMP, server_default=func.now())
