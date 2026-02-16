from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.postgres import get_db
from backend.app.models.leave_request import LeaveRequest, LeaveStatus
from backend.app.models.leave_balance import LeaveBalance
from backend.app.models.user import User
from backend.app.utils.auth_utils import get_current_user

router = APIRouter(
    prefix="/manager",
    tags=["manager"]
)

# ---------------- APPROVE TEAM LEAVE ----------------
@router.put("/leave/{leave_id}/approve")
def approve_team_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "manager":
        raise HTTPException(status_code=403, detail="manager access required")

    leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    employee = db.query(User).filter(User.id == leave.user_id).first()

    # Manager can approve only their team member
    if employee.manager_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your team member")

    if leave.status != LeaveStatus.PENDING:
        raise HTTPException(status_code=400, detail="Leave already processed")

    leave.status = LeaveStatus.APPROVED
    leave.approved_by_role = "manager"
    leave.approved_by_id = current_user.id

    db.commit()
    await send_email(
    subject="Leave Approved",
    recipients=[leave_owner.email],
    body="Your leave has been approved."
)

    return {"message": "Leave approved by manager"}
