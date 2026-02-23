from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from backend.database.postgres import get_db
from backend.app.models.user import User
from backend.app.utils.auth_utils import get_current_user

router = APIRouter(
    prefix="/resignation",
    tags=["Resignation"]
)

# ✅ Employee submits resignation
@router.post("/apply")
def apply_resignation(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "employee":
        raise HTTPException(status_code=403, detail="Only employees can resign")

    if current_user.resignation_status == "PENDING":
        raise HTTPException(status_code=400, detail="Resignation already submitted")

    current_user.resignation_status = "PENDING"
    current_user.resignation_date = date.today()

    db.commit()

    return {"message": "Resignation submitted successfully"}


# ✅ Manager approves resignation
@router.put("/approve/{user_id}")
def approve_resignation(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Only managers can approve resignation")

    employee = db.query(User).filter(User.id == user_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="User not found")

    if employee.resignation_status != "PENDING":
        raise HTTPException(status_code=400, detail="No pending resignation")

    employee.resignation_status = "APPROVED"
    employee.resignation_approval_date = date.today()

    db.commit()

    return {"message": "Resignation approved successfully"}
# ✅ Manager rejects resignation
@router.put("/reject/{user_id}")
def reject_resignation(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Only managers can reject resignation")

    employee = db.query(User).filter(User.id == user_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="User not found")

    if employee.resignation_status != "PENDING":
        raise HTTPException(status_code=400, detail="No pending resignation to reject")

    employee.resignation_status = None
    employee.resignation_date = None
    employee.resignation_approval_date = None

    db.commit()

    return {"message": "Resignation rejected successfully"}
# ✅ Manager view pending resignations
@router.get("/pending")
def get_pending_resignations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Only managers can view pending resignations")

    # Get employees under this manager
    team_members = db.query(User).filter(
        User.manager_id == current_user.id,
        User.resignation_status == "PENDING"
    ).all()

    return team_members