from pydantic import BaseModel
from datetime import date
from typing import Optional

class ResignationApply(BaseModel):
    reason: str
    last_working_day: date


class ResignationResponse(BaseModel):
    resignation_status: Optional[str]
    resignation_reason: Optional[str]
    last_working_day: Optional[date]
    resignation_date: Optional[date]
    resignation_approval_date: Optional[date]