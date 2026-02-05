from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


# =========================
# Base leave schema
# =========================
class LeaveBase(BaseModel):
    leave_type: str
    start_date: date
    end_date: date
    reason: Optional[str] = None


# =========================
# Apply leave
# =========================
class LeaveCreate(LeaveBase):
    pass


# =========================
# Approve / Reject leave
# =========================
class LeaveAction(BaseModel):
    status: str  # APPROVED / REJECTED
    approver_id: int


# =========================
# Leave response
# =========================
class LeaveResponse(LeaveBase):
    leave_id: int
    user_id: int
    number_of_days: int
    status: str

    applied_on: datetime
    approved_on: Optional[datetime]
    rejected_on: Optional[datetime]
    cancelled_on: Optional[datetime]

    proof_uploaded: bool
    proof_document_path: Optional[str]

    class Config:
        orm_mode = True

