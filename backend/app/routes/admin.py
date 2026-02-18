from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime
from backend.app.models.leave_logs import LeaveLog
from backend.database.postgres import get_db
from backend.app.models.leave_request import LeaveRequest
from backend.app.models.leave_balance import LeaveBalance
from backend.app.models.user import User
from backend.app.utils.auth_utils import get_current_user
from backend.app.utils.email_utils import send_email
from backend.app.models.leave_types import LeaveType
from backend.app.utils.email_service import send_email

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

# ================= APPROVE LEAVE =================
@router.put("/leave/{leave_id}/approve")
async def approve_leave(
    leave_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    leave = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    if leave.status != "pending":
        raise HTTPException(
            status_code=400,
            detail="Only pending leave can be approved"
        )

    leave.status = "approved"
    leave.approved_by_role = "admin"
    leave.approved_by_id = current_user.id

    db.commit()

    leave_owner = db.query(User).filter(
        User.id == leave.user_id
    ).first()

    if leave_owner:
        background_tasks.add_task(
            send_email,
            db,  # IMPORTANT
            leave_owner.email,
            "Leave Approved",
            "Your leave has been approved."
        )

    return {"message": "Leave approved successfully"}

# ================= REJECT LEAVE =================
@router.put("/leave/{leave_id}/reject")
def reject_leave(
    leave_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    leave = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    if leave.status != "pending":
        raise HTTPException(
            status_code=400,
            detail="Only pending leave can be rejected"
        )

    leave.status = "rejected"
    leave.approved_by_role = "admin"
    leave.approved_by_id = current_user.id
    leave.approved_at = datetime.utcnow()

    log = LeaveLog(
        leave_id=leave.id,
        action="Rejected",
        performed_by=current_user.id
    )

    db.add(log)
    db.commit()

    # Send email in background
    leave_owner = db.query(User).filter(User.id == leave.user_id).first()

    background_tasks.add_task(
        send_email,
        leave_owner.email,
        "Leave Rejected",
        "Your leave has been rejected by Admin."
    )

    return {"message": "Leave rejected successfully by admin"}
