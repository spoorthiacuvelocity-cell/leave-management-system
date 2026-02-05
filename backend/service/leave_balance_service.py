from sqlalchemy.orm import Session
from sqlalchemy import func

from models.leave_request import LeaveRequest


class LeaveBalanceService:

    @staticmethod
    def get_used_leaves(
        db: Session,
        user_id: int,
        leave_type: str
    ) -> int:

        total = db.query(
            func.coalesce(func.sum(LeaveRequest.number_of_days), 0)
        ).filter(
            LeaveRequest.user_id == user_id,
            LeaveRequest.leave_type == leave_type,
            LeaveRequest.status == "APPROVED"
        ).scalar()

        return total
