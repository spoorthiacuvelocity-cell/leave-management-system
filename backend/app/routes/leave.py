from fastapi import APIRouter, Depends, HTTPException
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
from fastapi.responses import StreamingResponse
import csv
import io
from backend.app.utils.email_service import send_email
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # -------- Overlapping Check --------
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

    # -------- Config Check --------
    config = db.query(Configuration).filter(
        Configuration.leave_type == request.leave_type
    ).first()

    if not config:
        raise HTTPException(status_code=400, detail="Invalid leave type")

    # -------- Gender Validation --------
    if config.gender_specific:
        if not current_user.gender:
            raise HTTPException(status_code=400, detail="User gender not defined")

        if current_user.gender.upper() != config.gender_specific.upper():
            raise HTTPException(
                status_code=403,
                detail=f"{request.leave_type} leave only for {config.gender_specific}"
            )

    # -------- Notice Period Validation --------
    if config.notice_period_days and config.notice_period_days > 0:
        today = date.today()
        days_difference = (request.start_date - today).days

        if days_difference < config.notice_period_days:
            raise HTTPException(
                status_code=400,
                detail=f"{config.leave_type} requires {config.notice_period_days} days notice"
            )

    # -------- Leave Days Calculation --------
    leave_days = (request.end_date - request.start_date).days + 1
    if leave_days <= 0:
        raise HTTPException(status_code=400, detail="Invalid date range")

    # -------- Max Consecutive Check --------
    if config.max_consecutive_leaves:
        if leave_days > config.max_consecutive_leaves:
            raise HTTPException(
                status_code=400,
                detail=f"Maximum consecutive leaves allowed is {config.max_consecutive_leaves}"
            )

    # -------- Quarterly Limit Check --------
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

    # -------- Create Leave --------
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
    

    await send_email(
    subject="Leave Application Submitted",
    recipients=[current_user.email],
    body=f"Your leave from {request.start_date} to {request.end_date} has been submitted."
)

    # -------- Log --------
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


# ================= VIEW MY LEAVES =================
@router.get("/my-leaves")
def get_my_leaves(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(LeaveRequest).filter(
        LeaveRequest.user_id == current_user.id
    ).all()


# ================= CANCEL LEAVE =================
@router.put("/cancel/{leave_id}")
def cancel_leave(
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


# ================= ADMIN APPLY FOR USER =================
@router.post("/admin/apply/{user_id}")
async def admin_apply_leave(
    user_id: int,
    request: LeaveCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    leave = LeaveRequest(
        leave_type=request.leave_type,
        start_date=request.start_date,
        end_date=request.end_date,
        reason=request.reason,
        user_id=user.id,
        status="Approved"
    )

    db.add(leave)
    db.commit()
# ================= ADMIN DASHBOARD =================
@router.get("/admin/dashboard")
def admin_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    return {
        "total_users": db.query(User).count(),
        "total_leaves": db.query(LeaveRequest).count(),
        "pending": db.query(LeaveRequest).filter(LeaveRequest.status == "Pending").count(),
        "approved": db.query(LeaveRequest).filter(LeaveRequest.status == "Approved").count(),
        "rejected": db.query(LeaveRequest).filter(LeaveRequest.status == "Rejected").count(),
    }


# ================= EXPORT CSV =================
@router.get("/admin/export")
def export_leaves(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    leaves = db.query(LeaveRequest).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "User", "Type", "Start", "End", "Status"])

    for leave in leaves:
        writer.writerow([
            leave.id,
            leave.user_id,
            leave.leave_type,
            leave.start_date,
            leave.end_date,
            leave.status
        ])

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=leaves.csv"}
    )
