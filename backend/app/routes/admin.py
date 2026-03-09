from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from backend.database.postgres import get_db
from backend.app.models.leave_request import LeaveRequest
from backend.app.models.leave_logs import LeaveLog
from backend.app.models.user import User
from backend.app.utils.auth_utils import get_current_user
from backend.app.utils.email_utils import send_email
from backend.app.service.approval_service import ApprovalService
from backend.app.models.leave_balance import LeaveBalance
router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# ================= GET ALL LEAVES =================
@router.get("/leaves")
def get_all_leaves(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role.upper() != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")

    leaves = db.query(LeaveRequest).all()

    result = []

    for leave in leaves:
        result.append({
            "id": leave.id,
            "user_id": leave.user_id,
            "leave_type": leave.leave_type,
            "start_date": leave.start_date,
            "end_date": leave.end_date,
            "status": leave.status,
            "reason": leave.reason,
            "number_of_days": leave.number_of_days,
            "remarks": leave.remarks,
            "approved_by_role": leave.approved_by_role,
            "approved_on": leave.approved_on
        })

    return result

# ================= APPROVE LEAVE =================
@router.put("/leave/{leave_id}/approve")
async def approve_leave(
    leave_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role.upper() != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")

    # Get leave
    leave = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    # Approve leave using service
    result = ApprovalService.approve_leave(
        db,
        leave_id,
        approver_role="ADMIN",
        approver_id=current_user.id
    )

    # 🔥 Deduct Leave Balance After Approval
    current_year = leave.start_date.year
    current_quarter = (leave.start_date.month - 1) // 3 + 1

    balance = db.query(LeaveBalance).filter(
        LeaveBalance.user_id == leave.user_id,
        LeaveBalance.leave_type == leave.leave_type,
        LeaveBalance.year == current_year,
        LeaveBalance.quarter == current_quarter
    ).first()

    if balance:
        balance.remaining_leaves -= leave.number_of_days
        balance.leaves_taken += leave.number_of_days

    # Log action
    log = LeaveLog(
        leave_id=leave_id,
        action="Approved by Admin",
        performed_by=current_user.id
    )

    db.add(log)
    db.commit()

    # Send email
    leave_owner = db.query(User).filter(
        User.id == leave.user_id
    ).first()

    if leave_owner:
        background_tasks.add_task(
            send_email,
            db,
            leave_owner.email,
            "Leave Approved",
            f"""
Your leave from {leave.start_date} to {leave.end_date}
has been approved by Admin.
"""
        )

    return result


# ================= REJECT LEAVE =================
@router.put("/leave/{leave_id}/reject")
async def reject_leave(
    leave_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role.upper() != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")

    leave = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    result = ApprovalService.reject_leave(
        db,
        leave_id,
        approver_role="ADMIN",
        approver_id=current_user.id
    )

    log = LeaveLog(
        leave_id=leave_id,
        action="Rejected by Admin",
        performed_by=current_user.id
    )
    db.add(log)
    db.commit()

    leave_owner = db.query(User).filter(
        User.id == leave.user_id
    ).first()

    if leave_owner:
        background_tasks.add_task(
            send_email,
            db,
            leave_owner.email,
            "Leave Rejected",
            f"""
Your leave from {leave.start_date} to {leave.end_date} 
has been rejected by Admin.
"""
        )

    return result