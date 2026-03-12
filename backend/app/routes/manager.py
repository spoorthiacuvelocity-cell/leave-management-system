from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Body
from sqlalchemy.orm import Session

from backend.database.postgres import get_db
from backend.app.models.leave_request import LeaveRequest
from backend.app.models.leave_logs import LeaveLog
from backend.app.models.user import User
from backend.app.utils.auth_utils import get_current_user
from backend.app.utils.email_utils import send_email
from backend.app.service.approval_service import ApprovalService

router = APIRouter(
    prefix="/manager",
    tags=["Manager"]
)


# ================= APPROVE LEAVE =================
@router.put("/leave/{leave_id}/approve")
async def manager_approve_leave(
    leave_id: int,
    remarks: str = Body(None),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role.upper() != "MANAGER":
        raise HTTPException(status_code=403, detail="Manager access required")

    leave = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    employee = db.query(User).filter(
        User.id == leave.user_id,
        User.manager_id == current_user.id
    ).first()

    if not employee:
        raise HTTPException(status_code=403, detail="Not your team member")

    result = ApprovalService.approve_leave(
        db,
        leave_id,
        approver_role="MANAGER",
        approver_id=current_user.id,
        remarks=remarks
    )

    log = LeaveLog(
        leave_id=leave_id,
        action=f"Approved by Manager. Remarks: {remarks}" if remarks else "Approved by Manager",
        performed_by=current_user.id
    )

    db.add(log)
    db.commit()

    # Send email notification
    if background_tasks:
        background_tasks.add_task(
            send_email,
            db,
            employee.email,
            "Leave Approved",
            f"""
Hello {employee.name},

Your leave from {leave.start_date} to {leave.end_date} has been approved.

Remarks: {remarks if remarks else 'No remarks provided.'}

Regards,
HR Team
"""
        )

    return result


# ================= REJECT LEAVE =================
@router.put("/leave/{leave_id}/reject")
async def manager_reject_leave(
    leave_id: int,
    remarks: str = Body(None),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role.upper() != "MANAGER":
        raise HTTPException(status_code=403, detail="Manager access required")

    leave = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    employee = db.query(User).filter(
        User.id == leave.user_id,
        User.manager_id == current_user.id
    ).first()

    if not employee:
        raise HTTPException(status_code=403, detail="Not your team member")

    result = ApprovalService.reject_leave(
        db,
        leave_id,
        approver_role="MANAGER",
        approver_id=current_user.id,
        remarks=remarks
    )

    log = LeaveLog(
        leave_id=leave_id,
        action=f"Rejected by Manager. Remarks: {remarks}" if remarks else "Rejected by Manager",
        performed_by=current_user.id
    )

    db.add(log)
    db.commit()

    if background_tasks:
        background_tasks.add_task(
            send_email,
            db,
            employee.email,
            "Leave Rejected",
            f"""
Hello {employee.name},

Your leave from {leave.start_date} to {leave.end_date} has been rejected.

Remarks: {remarks if remarks else 'No remarks provided.'}

Regards,
HR Team
"""
        )

    return result


# ================= TEAM LEAVES =================
@router.get("/team")
def get_team_leaves(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role.upper() != "MANAGER":
        raise HTTPException(status_code=403, detail="Not authorized")

    leaves = (
        db.query(LeaveRequest, User.name)
        .join(User, LeaveRequest.user_id == User.id)
        .filter(
            User.manager_id == current_user.id,
            LeaveRequest.status.ilike("pending")
        )
        .all()
    )

    result = []

    for leave, name in leaves:

        leave_dict = {
            "id": leave.id,
            "leave_type": leave.leave_type,
            "start_date": leave.start_date,
            "end_date": leave.end_date,
            "number_of_days": leave.number_of_days,
            "status": leave.status,
            "reason": leave.reason,
            "employee_name": name,
            "proof_document": leave.proof_document
        }

        result.append(leave_dict)

    return result