from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.database.postgres import get_db
from backend.app.models.leave_request import LeaveRequest
from backend.app.models.user import User
from backend.app.utils.auth_utils import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total = db.query(func.count(LeaveRequest.id)).count()

    approved = db.query(func.count(LeaveRequest.id)).filter(
        LeaveRequest.status == "Approved"
    ).count()

    pending = db.query(func.count(LeaveRequest.id)).filter(
        LeaveRequest.status == "Pending"
    ).count()

    rejected = db.query(func.count(LeaveRequest.id)).filter(
        LeaveRequest.status == "Rejected"
    ).count()

    return {
        "total": total,
        "approved": approved,
        "pending": pending,
        "rejected": rejected
    }
from sqlalchemy import extract

@router.get("/monthly-trend")
def get_monthly_trend(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    results = db.query(
        extract("month", LeaveRequest.start_date).label("month"),
        func.count(LeaveRequest.id)
    ).group_by("month").all()

    trend = {int(month): count for month, count in results}

    # Ensure all 12 months exist
    final = []
    for m in range(1, 13):
        final.append(trend.get(m, 0))

    return final