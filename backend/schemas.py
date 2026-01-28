from pydantic import BaseModel
from datetime import date

class LeaveRequest(BaseModel):
    employee_name: str
    reason: str
    from_date: date
    to_date: date
