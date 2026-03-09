from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from backend.app.schemas.resignation import ResignationApply
from backend.database.postgres import get_db
from backend.app.models.user import User
from backend.app.utils.auth_utils import get_current_user

router = APIRouter(
    prefix="/resignation",
    tags=["Resignation"]
)

# ================= EMPLOYEE APPLY =================
@router.post("/apply")
def apply_resignation(
    resignation: ResignationApply,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role.upper() != "EMPLOYEE":
        raise HTTPException(status_code=403, detail="Only employees can resign")

    # 🔥 Fetch fresh user from DB (IMPORTANT FIX)
    employee = db.query(User).filter(User.id == current_user.id).first()

    if employee.resignation_status == "PENDING":
        raise HTTPException(status_code=400, detail="Resignation already submitted")

    employee.resignation_status = "PENDING"
    employee.resignation_reason = resignation.reason
    employee.last_working_day = resignation.last_working_day
    employee.resignation_date = date.today()

    db.commit()
    db.refresh(employee)

    return {"message": "Resignation submitted successfully"}

# ================= ADMIN APPROVES =================
@router.put("/approve/{user_id}")
def approve_resignation(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role.lower() != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can approve resignation"
        )

    employee = db.query(User).filter(User.id == user_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="User not found")

    if employee.resignation_status != "PENDING":
        raise HTTPException(status_code=400, detail="No pending resignation")

    employee.resignation_status = "APPROVED"
    employee.resignation_approval_date = date.today()

    db.commit()

    return {"message": "Resignation approved successfully"}


# ================= ADMIN REJECTS =================
@router.put("/reject/{user_id}")
def reject_resignation(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role.lower() != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can reject resignation"
        )

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


# ================= ADMIN VIEW PENDING =================
@router.get("/pending")
def get_pending_resignations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role.lower() != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can view pending resignations"
        )

    pending_employees = db.query(User).filter(
        User.resignation_status == "PENDING"
    ).all()

    return [
        {
            "id": emp.id,
            "name": emp.name,
            "email": emp.email,
            "reason": emp.resignation_reason,
            "last_working_day": emp.last_working_day,
            "resignation_date": emp.resignation_date,
        }
        for emp in pending_employees
    ]
@router.get("/my")
def get_my_resignation(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    employee = db.query(User).filter(User.id == current_user.id).first()

    return {
        "status": employee.resignation_status,
        "reason": employee.resignation_reason,
        "last_working_day": employee.last_working_day,
        "resignation_date": employee.resignation_date
    }