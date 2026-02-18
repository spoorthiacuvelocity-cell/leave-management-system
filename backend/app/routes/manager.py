from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime
from backend.database.postgres import get_db
from backend.app.models.leave_request import LeaveRequest
from backend.app.models.leave_balance import LeaveBalance
from backend.app.models.leave_logs import LeaveLog
from backend.app.models.user import User
from backend.app.utils.auth_utils import get_current_user
from backend.app.utils.email_utils import send_email
from backend.app.models.leave_types import LeaveType

router = APIRouter(
    prefix="/manager",
    tags=["Manager"]
)

@router.put("/leave/{leave_id}/approve")
async def manager_approve_leave(
    leave_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Manager access required")

    leave = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    if leave.status != "pending":
        raise HTTPException(status_code=400, detail="Only pending leave can be approved")

    # Ensure this employee belongs to manager
    employee = db.query(User).filter(
        User.id == leave.user_id,
        User.manager_id == current_user.id
    ).first()

    if not employee:
        raise HTTPException(status_code=403, detail="Not your team member")

    # Calculate leave days
    leave_days = (leave.end_date - leave.start_date).days + 1

    year = leave.start_date.year
    quarter = (leave.start_date.month - 1) // 3 + 1

    balance = db.query(LeaveBalance).filter(
        LeaveBalance.user_id == leave.user_id,
        LeaveBalance.year == year,
        LeaveBalance.quarter == quarter,
        LeaveBalance.leave_type == leave.leave_type
    ).first()

    if not balance:
        raise HTTPException(status_code=400, detail="Leave balance not found")

    if balance.remaining_leaves < leave_days:
        raise HTTPException(status_code=400, detail="Insufficient leave balance")

    balance.used_leaves += leave_days
    balance.remaining_leaves -= leave_days

    leave.status = "approved"
    leave.approved_by_role = "manager"
    leave.approved_by_id = current_user.id
    leave.approved_at = datetime.utcnow()

    log = LeaveLog(
        leave_id=leave.id,
        action="Approved by Manager",
        performed_by=current_user.id
    )

    db.add(log)
    db.commit()

    # 📩 Send email to employee
    background_tasks.add_task(
        send_email,
        employee.email,
        "Leave Approved",
        f"Your leave from {leave.start_date} to {leave.end_date} has been approved by Manager."
    )

    return {"message": "Leave approved successfully by Manager"}
@router.put("/leave/{leave_id}/reject")
async def manager_reject_leave(
    leave_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Manager access required")

    leave = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    if leave.status != "pending":
        raise HTTPException(status_code=400, detail="Only pending leave can be rejected")

    employee = db.query(User).filter(
        User.id == leave.user_id,
        User.manager_id == current_user.id
    ).first()

    if not employee:
        raise HTTPException(status_code=403, detail="Not your team member")

    leave.status = "rejected"
    leave.approved_by_role = "manager"
    leave.approved_by_id = current_user.id
    leave.approved_at = datetime.utcnow()

    log = LeaveLog(
        leave_id=leave.id,
        action="Rejected by Manager",
        performed_by=current_user.id
    )

    db.add(log)
    db.commit()

    # 📩 Email employee
    background_tasks.add_task(
        send_email,
        employee.email,
        "Leave Rejected",
        f"Your leave from {leave.start_date} to {leave.end_date} has been rejected by Manager."
    )

    return {"message": "Leave rejected successfully by Manager"}
