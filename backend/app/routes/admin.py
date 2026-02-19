from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from backend.database.postgres import get_db
from backend.app.models.leave_request import LeaveRequest
from backend.app.models.leave_logs import LeaveLog
from backend.app.models.user import User
from backend.app.utils.auth_utils import get_current_user
from backend.app.utils.email_utils import send_email
from backend.app.service.approval_service import ApprovalService

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


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

    result = ApprovalService.approve_leave(
        db,
        leave_id,
        approver_role="admin",
        approver_id=current_user.id
    )

    log = LeaveLog(
        leave_id=leave_id,
        action="Approved by Admin",
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
            "Leave Approved",
            f"Your leave from {leave.start_date} to {leave.end_date} has been approved by Admin."
        )

    return result


@router.put("/leave/{leave_id}/reject")
async def reject_leave(
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

    result = ApprovalService.reject_leave(
        db,
        leave_id,
        approver_role="admin",
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
            f"Your leave from {leave.start_date} to {leave.end_date} has been rejected by Admin."
        )

    return result
