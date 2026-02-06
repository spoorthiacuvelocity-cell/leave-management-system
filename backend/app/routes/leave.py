from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.postgres import get_db
from backend.app.models.leave_request import LeaveRequest
from backend.app.schemas.leave_schema import LeaveCreate
from backend.app.models.user import User
from backend.app.utils.auth_utils import get_current_user

router = APIRouter(
    prefix="/leave",
    tags=["Leave"]
)


# ---------------- APPLY LEAVE (EMPLOYEE ONLY) ----------------
@router.post("/apply", status_code=status.HTTP_201_CREATED)
def apply_leave(
    leave_data: LeaveCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Role check
    if current_user.role != "EMPLOYEE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only employees can apply for leave"
        )

    leave = LeaveRequest(
        user_id=current_user.id,
        start_date=leave_data.start_date,
        end_date=leave_data.end_date,
        reason=leave_data.reason,
        status="PENDING"
    )

    db.add(leave)
    db.commit()
    db.refresh(leave)

    return {
        "message": "Leave applied successfully",
        "leave_id": leave.id,
        "status": leave.status
    }


# ---------------- VIEW MY LEAVES ----------------
@router.get("/my-leaves")
def get_my_leaves(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    leaves = db.query(LeaveRequest).filter(
        LeaveRequest.user_id == current_user.id
    ).all()

    return leaves
