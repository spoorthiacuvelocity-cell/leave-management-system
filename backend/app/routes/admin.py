from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from backend.app.models.leave_logs import LeaveLog
from backend.database.postgres import get_db
from backend.app.models.leave_request import LeaveRequest, LeaveStatus
from backend.app.models.leave_balance import LeaveBalance
from backend.app.models.user import User
from backend.app.utils.auth_utils import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

# ================= APPROVE LEAVE =================
@router.put("/leave/{leave_id}/approve")
def approve_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # -------- Admin Check --------
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    # -------- Get Leave --------
    leave = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    # -------- Only Pending Can Be Approved --------
    if leave.status != LeaveStatus.PENDING:
        raise HTTPException(
            status_code=400,
            detail="Only pending leave can be approved"
        )

    # -------- Prevent Double Approval --------
    if leave.approved_by_role:
        raise HTTPException(
            status_code=400,
            detail="Leave already processed"
        )

    # -------- Calculate Leave Days --------
    leave_days = (leave.end_date - leave.start_date).days + 1

    # -------- Get Correct Balance (Year + Quarter Safe) --------
    year = leave.start_date.year
    quarter = (leave.start_date.month - 1) // 3 + 1

    balance = db.query(LeaveBalance).filter(
        LeaveBalance.user_id == leave.user_id,
        LeaveBalance.year == year,
        LeaveBalance.quarter == quarter,
        LeaveBalance.leave_type == leave.leave_type
    ).first()

    if not balance:
        raise HTTPException(
            status_code=400,
            detail="Leave balance record not found"
        )

    if balance.remaining_leaves < leave_days:
        raise HTTPException(
            status_code=400,
            detail="Insufficient leave balance"
        )

    # -------- Deduct Balance --------
    balance.used_leaves += leave_days
    balance.remaining_leaves -= leave_days

    # -------- Update Leave --------
    leave.status = LeaveStatus.APPROVED
    leave.approved_by_role = "admin"
    leave.approved_by_id = current_user.id
    leave.approved_at = datetime.utcnow()

    # -------- Add Log --------
    log = LeaveLog(
        leave_id=leave.id,
        action="Approved",
        performed_by=current_user.id
    )

    db.add(log)
    db.commit()
    await send_email(
    subject="Leave Approved",
    recipients=[leave_owner.email],
    body="Your leave has been approved."
)

    return {"message": "Leave approved successfully by admin"}


# ================= REJECT LEAVE =================
@router.put("/leave/{leave_id}/reject")
def reject_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # -------- Admin Check --------
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    leave = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    # -------- Only Pending Can Be Rejected --------
    if leave.status != LeaveStatus.PENDING:
        raise HTTPException(
            status_code=400,
            detail="Only pending leave can be rejected"
        )

    leave.status = LeaveStatus.REJECTED
    leave.approved_by_role = "admin"
    leave.approved_by_id = current_user.id
    leave.approved_at = datetime.utcnow()

    # -------- Add Log --------
    log = LeaveLog(
        leave_id=leave.id,
        action="Rejected",
        performed_by=current_user.id
    )

    db.add(log)
    db.commit()

    return {"message": "Leave rejected successfully by admin"}
    await send_email(
    subject="Leave Rejected",
    recipients=[leave_owner.email],
    body="Your leave has been rejected."
)
