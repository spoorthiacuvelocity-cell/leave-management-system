from pydantic import BaseModel
from typing import Optional

class ConfigUpdate(BaseModel):
    leaves_per_quarter: Optional[float] = None
    max_consecutive_leaves: Optional[int] = None
    notice_period_days: Optional[int] = None
    proof_required: Optional[bool] = None
    proof_required_after_days: Optional[int] = None
    # 🔥 EMAIL SETTINGS
    smtp_email: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_server: Optional[str] = None
    smtp_port: Optional[int] = None
