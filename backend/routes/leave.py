from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import timedelta
from database import SessionLocal
from schemas import LeaveRequest
from models import Leave
from utils import is_invalid_leave_day


print("LeaveRequest fields:", LeaveRequest.__fields__)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/apply-leave")
def apply_leave(leave: LeaveRequest, db: Session = Depends(get_db)):

    current_date = leave.from_date

    while current_date <= leave.to_date:
        if is_invalid_leave_day(current_date):
            raise HTTPException(
                status_code=400,
                detail=f"Leave cannot be applied on {current_date}. It is a holiday or weekend."
            )
        current_date += timedelta(days=1)

    new_leave = Leave(
        employee_name=leave.employee_name,
        reason=leave.reason,
        from_date=leave.from_date,
        to_date=leave.to_date
    )

    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)

    return {
        "message": "Leave applied successfully",
        "leave_id": new_leave.id
    }
    
@router.get("/leaves")
def get_all_leaves(db: Session = Depends(get_db)):
    return db.query(Leave).all()
