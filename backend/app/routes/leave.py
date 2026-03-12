from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, UploadFile, File, Form
from sqlalchemy.orm import Session
from datetime import date
import os
import uuid

from backend.database.postgres import get_db
from backend.app.models.leave_request import LeaveRequest
from backend.app.models.leave_balance import LeaveBalance
from backend.app.models.user import User
from backend.app.utils.auth_utils import get_current_user

router = APIRouter(
    prefix="/leave",
    tags=["Leave"]
)


# ================= GET LEAVE TYPES =================
@router.get("/types")
def get_leave_types(current_user: User = Depends(get_current_user)):

    types = ["CASUAL", "SICK", "EARNED", "LOSS_OF_PAY"]

    if current_user.gender.upper() == "FEMALE":
        types.extend(["MATERNITY", "PERIODS"])

    if current_user.gender.upper() == "MALE":
        types.append("PATERNITY")

    return types


# ================= GET MY LEAVES =================
@router.get("/my")
def get_my_leaves(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    leaves = db.query(LeaveRequest).filter(
        LeaveRequest.user_id == current_user.id
    ).order_by(LeaveRequest.start_date.desc()).all()

    return leaves


# ================= GET LEAVE BALANCE =================
@router.get("/balance")
def get_leave_balance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    leave_types = ["CASUAL", "SICK", "EARNED", "LOSS_OF_PAY"]

    if current_user.gender.upper() == "MALE":
        leave_types.append("PATERNITY")

    if current_user.gender.upper() == "FEMALE":
        leave_types.extend(["MATERNITY", "PERIODS"])

    balances = []

    for leave_type in leave_types:

        balance = db.query(LeaveBalance).filter(
            LeaveBalance.user_id == current_user.id,
            LeaveBalance.leave_type == leave_type
        ).first()

        if balance:

            balances.append({
                "leave_type": balance.leave_type,
                "leaves_taken": float(balance.leaves_taken),
                "remaining_leaves": float(balance.remaining_leaves)
            })

        else:

            balances.append({
                "leave_type": leave_type,
                "leaves_taken": 0,
                "remaining_leaves": 0
            })

    return balances


# ================= APPLY LEAVE =================
@router.post("/apply")
async def apply_leave(
    leave_type: str = Form(...),
    start_date: date = Form(...),
    end_date: date = Form(...),
    reason: str = Form(None),
    proof_document: UploadFile = File(None),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    today = date.today()

    # Block leave during notice period
    if current_user.resignation_status == "notice_period":
        if current_user.last_working_day and today <= current_user.last_working_day:
            raise HTTPException(
                status_code=400,
                detail="You are in notice period. Leave cannot be applied."
            )

    if current_user.resignation_status == "resigned":
        raise HTTPException(
            status_code=403,
            detail="You are no longer an active employee."
        )

    # Gender restrictions
    if current_user.gender.upper() == "MALE" and leave_type in ["MATERNITY", "PERIODS"]:
        raise HTTPException(
            status_code=400,
            detail="You are not eligible for this leave type."
        )

    if current_user.gender.upper() == "FEMALE" and leave_type == "PATERNITY":
        raise HTTPException(
            status_code=400,
            detail="You are not eligible for this leave type."
        )

    # Date validation
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="Invalid date range")

    leave_days = (end_date - start_date).days + 1

    # Sick leave rules
    if leave_type == "SICK":

        if start_date != today:
            raise HTTPException(
                status_code=400,
                detail="Sick leave can only be applied for today."
            )

        if leave_days > 2 and not proof_document:
            raise HTTPException(
                status_code=400,
                detail="Medical proof required for sick leave more than 2 days."
            )

    # Maternity/Paternity proof
    if leave_type in ["MATERNITY", "PATERNITY"]:
        if not proof_document:
            raise HTTPException(
                status_code=400,
                detail="Proof document required."
            )

    # ================= LEAVE OVERLAP CHECK =================
    overlapping_leave = db.query(LeaveRequest).filter(
        LeaveRequest.user_id == current_user.id,
        LeaveRequest.status.in_(["Pending", "Approved"]),
        LeaveRequest.start_date <= end_date,
        LeaveRequest.end_date >= start_date
    ).first()

    if overlapping_leave:
        raise HTTPException(
            status_code=400,
            detail="Leave request overlaps with an existing leave"
        )

    current_year = start_date.year
    current_quarter = (start_date.month - 1) // 3 + 1

    balance = db.query(LeaveBalance).filter(
        LeaveBalance.user_id == current_user.id,
        LeaveBalance.leave_type == leave_type,
        LeaveBalance.year == current_year,
        LeaveBalance.quarter == current_quarter
    ).first()

    # ================= AUTO CREATE BALANCE =================
    if not balance:

        default_leaves = {
            "CASUAL": 6,
            "SICK": 6,
            "EARNED": 12,
            "LOSS_OF_PAY": 0,
            "PATERNITY": 15,
            "MATERNITY": 180,
            "PERIODS": 12
        }

        total = default_leaves.get(leave_type, 0)

        balance = LeaveBalance(
            user_id=current_user.id,
            leave_type=leave_type,
            year=current_year,
            quarter=current_quarter,
            leaves_taken=0,
            remaining_leaves=total
        )

        db.add(balance)
        db.commit()
        db.refresh(balance)

    if leave_days > float(balance.remaining_leaves):
        raise HTTPException(
            status_code=400,
            detail="Insufficient leave balance"
        )

    # ================= SAVE FILE =================
    file_path = None

    if proof_document:

        os.makedirs("uploads", exist_ok=True)

        unique_name = f"{uuid.uuid4()}_{proof_document.filename}"
        file_location = f"uploads/{unique_name}"

        with open(file_location, "wb") as buffer:
            buffer.write(await proof_document.read())

        file_path = file_location

    # ================= CREATE LEAVE =================
    leave = LeaveRequest(
        leave_type=leave_type,
        start_date=start_date,
        end_date=end_date,
        reason=reason,
        proof_document=file_path,
        user_id=current_user.id,
        status="Pending",
        number_of_days=leave_days
    )

    db.add(leave)
    db.commit()
    db.refresh(leave)

    return {"message": "Leave applied successfully"}


# ================= MANAGER VIEW EMPLOYEE BALANCE =================
@router.get("/manager/employee-balance/{employee_id}")
def manager_view_employee_balance(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "MANAGER":
        raise HTTPException(status_code=403, detail="Access denied")

    balances = db.query(LeaveBalance).filter(
        LeaveBalance.user_id == employee_id
    ).all()

    return balances


# ================= CANCEL LEAVE =================
@router.put("/cancel/{leave_id}")
def cancel_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    leave = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    if leave.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if leave.status == "Cancelled":
        raise HTTPException(status_code=400, detail="Leave already cancelled")

    leave.status = "Cancelled"

    db.commit()

    return {"message": "Leave cancelled successfully"}