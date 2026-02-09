from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.postgres import get_db
from backend.app.models.leave_request import LeaveRequest, LeaveStatus
from backend.app.models.leave_balance import LeaveBalance
from backend.app.models.user import User
from backend.app.utils.auth_utils import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

# ---------------- APPROVE LEAVE ----------------
@router.put("/leave/{leave_id}/approve")
def approve_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Admin check
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")

    leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    if leave.status != LeaveStatus.PENDING:
        raise HTTPException(status_code=400, detail="Leave already processed")

    # ❗ Priority check: Project Manager approval
    if leave.approved_by_role == "PROJECT_MANAGER":
        raise HTTPException(
            status_code=403,
            detail="Leave already approved by Project Manager"
        )

    # Calculate leave days
    leave_days = (leave.end_date - leave.start_date).days + 1

    balance = db.query(LeaveBalance).filter(
        LeaveBalance.user_id == leave.user_id
    ).first()

    if not balance:
        raise HTTPException(status_code=400, detail="Leave balance not found")

    if balance.remaining_leaves < leave_days:
        raise HTTPException(
            status_code=400,
            detail="Insufficient leave balance"
        )

    # Deduct leave balance
    balance.used_leaves += leave_days
    balance.remaining_leaves -= leave_days

    # Approve leave
    leave.status = LeaveStatus.APPROVED
    leave.approved_by_role = "ADMIN"
    leave.approved_by_id = current_user.id

    db.commit()

    return {"message": "Leave approved successfully by Admin"}


# ---------------- REJECT LEAVE ----------------
@router.put("/leave/{leave_id}/reject")
def reject_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")

    leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    if leave.status != LeaveStatus.PENDING:
        raise HTTPException(status_code=400, detail="Leave already processed")

    leave.status = LeaveStatus.REJECTED
    leave.approved_by_role = "ADMIN"
    leave.approved_by_id = current_user.id

    db.commit()

    return {"message": "Leave rejected successfully by Admin"}
