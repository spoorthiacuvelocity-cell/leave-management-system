from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.postgres import get_db
from backend.app.models.leave_request import LeaveRequest, LeaveStatus
from backend.app.models.user import User
from backend.app.utils.auth_utils import get_current_user

router = APIRouter(
    prefix="/manager",
    tags=["Project Manager"]
)

@router.put("/leave/{leave_id}/approve")
def pm_approve_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "PROJECT_MANAGER":
        raise HTTPException(status_code=403, detail="Project Manager access required")

    leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    if leave.status != LeaveStatus.PENDING:
        raise HTTPException(status_code=400, detail="Leave already processed")

    leave.status = LeaveStatus.APPROVED
    leave.approved_by_role = "PROJECT_MANAGER"
    leave.approved_by_id = current_user.id

    db.commit()

    return {"message": "Leave approved by Project Manager"}
