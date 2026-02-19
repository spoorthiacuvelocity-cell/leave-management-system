from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import date

from backend.database.postgres import get_db
from backend.app.models.leave_request import LeaveRequest
from backend.app.models.leave_balance import LeaveBalance
from backend.app.models.leave_logs import LeaveLog
from backend.app.models.configuration import Configuration
from backend.app.models.user import User
from backend.app.schemas.leave_schema import LeaveCreate
from backend.app.utils.auth_utils import get_current_user

router = APIRouter(
    prefix="/leave",
    tags=["Leave"]
)


# ================= HELPER FUNCTION =================
def get_config(db: Session, key: str):
    config = db.query(Configuration).filter(
        Configuration.config_parameter == key
    ).first()
    return config.config_value if config else None


# ================= APPLY LEAVE =================
@router.post("/apply")
async def apply_leave(
    request: LeaveCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # 🔥 Only employee & manager can apply
    if current_user.role not in ["employee", "manager"]:
        raise HTTPException(
            status_code=403,
            detail="Only employees and managers can apply leave"
        )

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

    # ✅ 2. Validate Date Range
    leave_days = (request.end_date - request.start_date).days + 1
    if leave_days <= 0:
        raise HTTPException(status_code=400, detail="Invalid date range")

    # ✅ 3. Notice Period Check
    notice_period = get_config(db, "notice_period_per_days")
    if notice_period:
        today = date.today()
        days_difference = (request.start_date - today).days

        if days_difference < int(notice_period):
            raise HTTPException(
                status_code=400,
                detail=f"Minimum {notice_period} days notice required"
            )

    # ✅ 4. Maximum Consecutive Leave Check
    max_consecutive = get_config(db, "maximum_consecutive_leave")
    if max_consecutive and leave_days > int(max_consecutive):
        raise HTTPException(
            status_code=400,
            detail=f"Maximum {max_consecutive} consecutive leaves allowed"
        )

    # 🔥 Leave-type specific gender rule
    gender_specific = get_config(db, f"{request.leave_type}_gender_specific")

    if gender_specific:
        if current_user.gender.lower() != gender_specific.lower():
            raise HTTPException(
                status_code=400,
                detail=f"{request.leave_type} is only for {gender_specific}"
            )

   # 🔥 Leave-type specific proof rule
    proof_required = get_config(db, f"{request.leave_type}_proof_required")
    proof_after_days = get_config(db, f"{request.leave_type}_proof_required_after_days")

    if proof_required and proof_required.lower() == "true":

        if proof_after_days:
            if leave_days > int(proof_after_days):
                if not request.proof_document:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Proof required for {request.leave_type}"
                    )
        else:
            # If no days limit defined but proof_required true
            if not request.proof_document:
                raise HTTPException(
                    status_code=400,
                    detail=f"Proof required for {request.leave_type}"
                )


    # ✅ 7. Leave Balance Check
    # Get current year and quarter
    current_year = request.start_date.year
    current_quarter = (request.start_date.month - 1) // 3 + 1

    # Get allowed leaves per quarter from config
    leaves_per_quarter = get_config(db, "leaves_per_quarter")

    if not leaves_per_quarter:
        raise HTTPException(status_code=400, detail="Leave limit not configured")

    leaves_per_quarter = float(leaves_per_quarter)

    # Fetch existing balance record
    balance = db.query(LeaveBalance).filter(
        LeaveBalance.user_id == current_user.id,
        LeaveBalance.leave_type == request.leave_type,
        LeaveBalance.year == current_year,
        LeaveBalance.quarter == current_quarter
    ).first()

    leaves_taken = float(balance.leaves_taken) if balance else 0

    if leaves_taken + leave_days > leaves_per_quarter:
        raise HTTPException(
        status_code=400,
        detail="Quarterly leave limit exceeded"
    )


    # ✅ 8. Create Leave Request
    leave = LeaveRequest(
        leave_type=request.leave_type,
        start_date=request.start_date,
        end_date=request.end_date,
        reason=request.reason,
        proof_document=request.proof_document,
        user_id=current_user.id,
        status="Pending",
        number_of_days=leave_days
    )

    db.add(leave)
    db.commit()
    db.refresh(leave)

    # ✅ 9. Add Log
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

    # Admin sees everything
    if current_user.role == "admin":
        return db.query(LeaveRequest).all()

    # Manager sees team + own leave
    if current_user.role == "manager":

        team_members = db.query(User).filter(
            User.manager_id == current_user.id
        ).all()

        team_ids = [member.id for member in team_members]

        # Add manager's own ID
        team_ids.append(current_user.id)

        return db.query(LeaveRequest).filter(
            LeaveRequest.user_id.in_(team_ids)
        ).all()

    # Employee sees only own leave
    if current_user.role == "employee":
        return db.query(LeaveRequest).filter(
            LeaveRequest.user_id == current_user.id
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

    if leave.status == "Cancelled":
        raise HTTPException(status_code=400, detail="Leave already cancelled")

    if leave.status == "Rejected":
        raise HTTPException(status_code=400, detail="Cannot cancel rejected leave")

    # Restore balance if already approved
    if leave.status == "Approved":
        balance = db.query(LeaveBalance).filter(
            LeaveBalance.user_id == current_user.id,
            LeaveBalance.leave_type == leave.leave_type
        ).first()

        if balance:
            balance.remaining_leaves += leave.number_of_days

    leave.status = "Cancelled"

    log = LeaveLog(
        leave_id=leave.id,
        action="Cancelled",
        performed_by=current_user.id
    )

    db.add(log)
    db.commit()

    return {"message": "Leave cancelled successfully"}
