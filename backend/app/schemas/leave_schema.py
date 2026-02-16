from pydantic import BaseModel
from datetime import date
from typing import Optional

class LeaveCreate(BaseModel):
    leave_type: str
    start_date: date
    end_date: date
    reason: Optional[str] = None
    proof_document: Optional[str] = None  # NEW FIELD
