from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.database.postgres import get_db
from backend.app.models.leave_request import LeaveRequest
from backend.app.models.leave_balance import LeaveBalance
from backend.app.models.user import User
from backend.app.utils.auth_utils import get_current_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    total_applied = db.query(func.count(LeaveRequest.id)).filter(
        LeaveRequest.user_id == current_user.id
    ).scalar()

    approved = db.query(func.count(LeaveRequest.id)).filter(
        LeaveRequest.user_id == current_user.id,
        LeaveRequest.status.ilike("approved")
    ).scalar()

    rejected = db.query(func.count(LeaveRequest.id)).filter(
        LeaveRequest.user_id == current_user.id,
        LeaveRequest.status.ilike("rejected")
    ).scalar()

    pending = db.query(func.count(LeaveRequest.id)).filter(
        LeaveRequest.user_id == current_user.id,
        LeaveRequest.status.ilike("pending")
    ).scalar()

    balance = db.query(LeaveBalance).filter(
        LeaveBalance.user_id == current_user.id
    ).all()

    total_remaining = sum(b.remaining_leaves for b in balance) if balance else 0

    return {
        "total_applied": total_applied,
        "approved": approved,
        "rejected": rejected,
        "pending": pending,
        "remaining_balance": total_remaining
    }
