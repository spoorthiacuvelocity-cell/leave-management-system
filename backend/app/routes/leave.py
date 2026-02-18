from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import date
from backend.database.postgres import get_db
from backend.app.models.leave_request import LeaveRequest
from backend.app.models.leave_balance import LeaveBalance
from backend.app.models.user import User
from backend.app.models.leave_logs import LeaveLog
from backend.app.models.leave_types import LeaveType
from backend.app.schemas.leave_schema import LeaveCreate
from backend.app.utils.auth_utils import get_current_user
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

    # ✅ 1. Overlapping Leave Check
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

    # ✅ 2. Fetch Leave Type Rules
    leave_type_config = db.query(LeaveType).filter(
        LeaveType.leave_name == request.leave_type
    ).first()

    if not leave_type_config:
        raise HTTPException(status_code=400, detail="Invalid leave type")

    # ✅ 3. Notice Period Check
    if leave_type_config.notice_period_days and leave_type_config.notice_period_days > 0:
        today = date.today()
        days_difference = (request.start_date - today).days

        if days_difference < leave_type_config.notice_period_days:
            raise HTTPException(
                status_code=400,
                detail=f"{request.leave_type} requires {leave_type_config.notice_period_days} days notice"
            )

    # ✅ 4. Validate Date Range
    leave_days = (request.end_date - request.start_date).days + 1
    if leave_days <= 0:
        raise HTTPException(status_code=400, detail="Invalid date range")

    # ✅ 5. Max Consecutive Leaves Check
    if leave_type_config.max_consecutive_leaves:
        if leave_days > leave_type_config.max_consecutive_leaves:
            raise HTTPException(
                status_code=400,
                detail=f"Maximum {leave_type_config.max_consecutive_leaves} consecutive leaves allowed"
            )

    # ✅ 6. Gender Specific Check
    if leave_type_config.gender_specific:
        if current_user.gender != leave_type_config.gender_specific:
            raise HTTPException(
                status_code=400,
                detail=f"{request.leave_type} leave is only for {leave_type_config.gender_specific}"
            )

    # ✅ 7. Proof Required Check
    if leave_type_config.proof_required:
        if leave_type_config.proof_required_after_days:
            if leave_days > leave_type_config.proof_required_after_days:
                if not request.proof_document:
                    raise HTTPException(
                        status_code=400,
                        detail="Proof document required for this leave"
                    )

    # ✅ 8. Quarterly Balance Check
    year = request.start_date.year
    quarter = get_quarter(request.start_date)

    balance = db.query(LeaveBalance).filter(
        LeaveBalance.user_id == current_user.id,
        LeaveBalance.leave_type == request.leave_type,
        LeaveBalance.year == year,
        LeaveBalance.quarter == quarter
    ).first()

    leaves_taken = float(balance.leaves_taken) if balance else 0

    if leave_type_config.leaves_per_quarter:
        if leaves_taken + leave_days > float(leave_type_config.leaves_per_quarter):
            raise HTTPException(
                status_code=400,
                detail="Quarterly leave limit exceeded"
            )

    # ✅ 9. Create Leave
    leave = LeaveRequest(
        leave_type=request.leave_type,
        start_date=request.start_date,
        end_date=request.end_date,
        reason=request.reason,
        proof_document=request.proof_document,
        user_id=current_user.id,
        status="Pending"
    )

    db.add(leave)
    db.commit()
    db.refresh(leave)

    # ✅ 10. Add Log
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
