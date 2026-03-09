from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import date
from fastapi import UploadFile, File, Form
import os
from backend.database.postgres import get_db
from backend.app.models.leave_request import LeaveRequest
from backend.app.models.leave_balance import LeaveBalance
from backend.app.models.leave_logs import LeaveLog
from backend.app.models.configuration import Configuration
from backend.app.models.user import User
from backend.app.schemas.leave_schema import LeaveCreate
from backend.app.utils.auth_utils import get_current_user

router = APIRouter(
    prefix="/leave",
    tags=["Leave"]
)


# ================= HELPER FUNCTION =================
def get_config(db: Session, key: str):
    config = db.query(Configuration).filter(
        Configuration.config_parameter == key
    ).first()
    return config.config_value if config else None


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

    # 🚨 BLOCK IF RESIGNATION PENDING
    if current_user.resignation_status == "PENDING":
        raise HTTPException(
            status_code=400,
            detail="Your resignation is pending approval. Leave not allowed."
        )

    # 🚨 BLOCK IF IN NOTICE PERIOD
    if current_user.resignation_status == "APPROVED":
        if current_user.last_working_day and today <= current_user.last_working_day:
            raise HTTPException(
                status_code=400,
                detail="You are in your notice period. You cannot apply leave."
            )

    # 🚨 GENDER RESTRICTION
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

    # 🚨 SICK LEAVE RULE
    if leave_type == "SICK":

        if start_date != today:
            raise HTTPException(
                status_code=400,
                detail="Sick leave can only be applied for today."
            )

        total_days = (end_date - start_date).days + 1

        if total_days > 2 and not proof_document:
            raise HTTPException(
                status_code=400,
                detail="Medical proof required for sick leave more than 2 days."
            )

    # 🚨 PROOF REQUIRED FOR MATERNITY & PATERNITY
    if leave_type in ["MATERNITY", "PATERNITY"]:
        if not proof_document:
            raise HTTPException(
                status_code=400,
                detail="Proof document is required for this leave type."
            )

    # ================= OVERLAPPING CHECK =================
    overlapping_leave = db.query(LeaveRequest).filter(
        LeaveRequest.user_id == current_user.id,
        LeaveRequest.status.in_(["Pending", "Approved"]),
        LeaveRequest.start_date <= end_date,
        LeaveRequest.end_date >= start_date
    ).first()

    if overlapping_leave:
        raise HTTPException(status_code=400, detail="Leave already exists")

    leave_days = (end_date - start_date).days + 1
    if leave_days <= 0:
        raise HTTPException(status_code=400, detail="Invalid date range")

    # ================= BALANCE CHECK =================
    current_year = start_date.year
    current_quarter = (start_date.month - 1) // 3 + 1

    balance = db.query(LeaveBalance).filter(
        LeaveBalance.user_id == current_user.id,
        LeaveBalance.leave_type == leave_type,
        LeaveBalance.year == current_year,
        LeaveBalance.quarter == current_quarter
    ).first()

    if not balance:
        raise HTTPException(status_code=400, detail="Leave balance not found")

    if balance.remaining_leaves < leave_days:
        raise HTTPException(status_code=400, detail="Insufficient leave balance")

    # ================= SAVE FILE =================
    file_path = None

    if proof_document:
        os.makedirs("uploads", exist_ok=True)

        file_location = f"uploads/{proof_document.filename}"

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
# ================= MY LEAVES =================
@router.get("/my")
def get_my_leaves(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(LeaveRequest).filter(
        LeaveRequest.user_id == current_user.id
    ).all()


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

    if leave.status != "Pending":
        raise HTTPException(status_code=400, detail="Cannot cancel processed leave")

    leave.status = "Cancelled"

    log = LeaveLog(
        leave_id=leave.id,
        action="Cancelled",
        performed_by=current_user.id
    )

    db.add(log)
    db.commit()

    return {"message": "Leave cancelled successfully"}


# ================= LEAVE BALANCE =================
@router.get("/balance")
def get_leave_balance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_year = date.today().year
    current_quarter = (date.today().month - 1) // 3 + 1

    balances = db.query(LeaveBalance).filter(
        LeaveBalance.user_id == current_user.id,
        LeaveBalance.year == current_year,
        LeaveBalance.quarter == current_quarter
    ).all()

    result = {}

    for balance in balances:

        leave_type = balance.leave_type.upper()

        # 🚨 Gender-based filtering
        if current_user.gender.upper() == "MALE":
            if leave_type in ["MATERNITY", "PERIODS"]:
                continue

        if current_user.gender.upper() == "FEMALE":
            if leave_type == "PATERNITY":
                continue

        result[leave_type.lower()] = {
            "year": balance.year,
            "quarter": balance.quarter,
            "taken": balance.leaves_taken,
            "remaining": balance.remaining_leaves
        }

    return result
# ================= LEAVE TYPES =================
@router.get("/types")
def get_leave_types():
    return [
        "CASUAL",
        "SICK",
        "EARNED",
        "LOSS_OF_PAY",
        "MATERNITY",
        "PATERNITY",
        "PERIODS"
    ]