from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import date
from backend.database.postgres import get_db
from backend.app.models.configuration import Configuration
from backend.app.models.leave_request import LeaveRequest
from backend.app.models.leave_balance import LeaveBalance
from backend.app.models.user import User
from backend.app.models.leave_logs import LeaveLog
from backend.app.schemas.leave_schema import LeaveCreate
from backend.app.utils.auth_utils import get_current_user
from backend.app.utils.email_utils import send_email

router = APIRouter(
    prefix="/leave",
    tags=["Leave"]
)


# ================= HELPER =================
def get_quarter(input_date):
    month = input_date.month
    if month <= 3:
        return 1
    elif month <= 6:
        return 2
    elif month <= 9:
        return 3
    else:
        return 4


# ================= APPLY LEAVE =================
@router.post("/apply")
async def apply_leave(
    request: LeaveCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    overlapping_leave = db.query(LeaveRequest).filter(
        LeaveRequest.user_id == current_user.id,
        LeaveRequest.status.in_(["Pending", "Approved"]),
        LeaveRequest.start_date <= request.end_date,
        LeaveRequest.end_date >= request.start_date
    ).first()

    if overlapping_leave:
        raise HTTPException(
            status_code=400,
            detail="You already have leave during this period"
        )

    config = db.query(Configuration).filter(
        Configuration.leave_type == request.leave_type
    ).first()

    if not config:
        raise HTTPException(status_code=400, detail="Invalid leave type")

    if config.notice_period_days and config.notice_period_days > 0:
        today = date.today()
        days_difference = (request.start_date - today).days

        if days_difference < config.notice_period_days:
            raise HTTPException(
                status_code=400,
                detail=f"{config.leave_type} requires {config.notice_period_days} days notice"
            )

    leave_days = (request.end_date - request.start_date).days + 1
    if leave_days <= 0:
        raise HTTPException(status_code=400, detail="Invalid date range")

    year = request.start_date.year
    quarter = get_quarter(request.start_date)

    balance = db.query(LeaveBalance).filter(
        LeaveBalance.user_id == current_user.id,
        LeaveBalance.leave_type == request.leave_type,
        LeaveBalance.year == year,
        LeaveBalance.quarter == quarter
    ).first()

    leaves_taken = float(balance.leaves_taken) if balance else 0

    if leaves_taken + leave_days > float(config.leaves_per_quarter):
        raise HTTPException(
            status_code=400,
            detail="Quarterly leave limit exceeded"
        )

    leave = LeaveRequest(
        leave_type=request.leave_type,
        start_date=request.start_date,
        end_date=request.end_date,
        reason=request.reason,
        user_id=current_user.id,
        status="Pending"
    )

    db.add(leave)
    db.commit()
    db.refresh(leave)

    # -------- Send Email To Manager --------
    manager = db.query(User).filter(
        User.id == current_user.manager_id
    ).first()

    if manager:
        background_tasks.add_task(
            send_email,
            db,  # IMPORTANT
            manager.email,
            "New Leave Request",
            f"{current_user.name} applied for leave from {request.start_date} to {request.end_date}"
        )

    # -------- Send Confirmation To Employee --------
    background_tasks.add_task(
        send_email,
        db,  # IMPORTANT
        current_user.email,
        "Leave Application Submitted",
        f"Your leave from {request.start_date} to {request.end_date} has been submitted."
    )

    log = LeaveLog(
        leave_id=leave.id,
        action="Applied",
        performed_by=current_user.id
    )
    db.add(log)
    db.commit()

    return {"message": "Leave applied successfully"}

# ================= VIEW ALL LEAVES =================
@router.get("/all")
def get_all_leaves(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "admin":
        return db.query(LeaveRequest).all()

    if current_user.role == "manager":
        team_members = db.query(User).filter(
            User.manager_id == current_user.id
        ).all()

        team_ids = [member.id for member in team_members]

        return db.query(LeaveRequest).filter(
            LeaveRequest.user_id.in_(team_ids)
        ).all()

    raise HTTPException(status_code=403, detail="Not authorized")


# ================= CANCEL LEAVE =================
@router.put("/cancel/{leave_id}")
async def cancel_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    leave = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    if leave.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if leave.status != "Pending":
        raise HTTPException(status_code=400, detail="Only pending leave can be cancelled")

    leave.status = "Cancelled"

    log = LeaveLog(
        leave_id=leave.id,
        action="Cancelled",
        performed_by=current_user.id
    )

    db.add(log)
    db.commit()

    return {"message": "Leave cancelled successfully"}
