from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import func
import csv
from fastapi.responses import StreamingResponse
import io
from backend.app.utils.auth_utils import hash_password
from backend.app.schemas.auth_schema import RegisterSchema
from backend.app.models.configuration import Configuration
from backend.database.postgres import get_db
from backend.app.models.leave_request import LeaveRequest
from backend.app.models.leave_logs import LeaveLog
from backend.app.models.user import User
from backend.app.utils.auth_utils import get_current_user
from backend.app.utils.email_utils import send_email
from backend.app.service.approval_service import ApprovalService
from backend.app.models.leave_balance import LeaveBalance
router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# ================= GET ALL LEAVES =================
@router.get("/leaves")
def get_all_leaves(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role.upper() != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")

    leaves = db.query(LeaveRequest).all()

    result = []

    for leave in leaves:
        result.append({
    "id": leave.id,
    "user_id": leave.user_id,
    "leave_type": leave.leave_type,
    "start_date": leave.start_date,
    "end_date": leave.end_date,
    "status": leave.status,
    "reason": leave.reason,
    "number_of_days": leave.number_of_days,
    "remarks": leave.remarks,
    "approved_by_role": leave.approved_by_role,
    "approved_on": leave.approved_on,
    "proof_document": leave.proof_document
})

    return result

# ================= APPROVE LEAVE =================
@router.put("/leave/{leave_id}/approve")
async def approve_leave(
    leave_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role.upper() != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")

    # Get leave
    leave = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    # Approve leave using service
    result = ApprovalService.approve_leave(
        db,
        leave_id,
        approver_role="ADMIN",
        approver_id=current_user.id
    )

    # 🔥 Deduct Leave Balance After Approval
    current_year = leave.start_date.year
    current_quarter = (leave.start_date.month - 1) // 3 + 1

    balance = db.query(LeaveBalance).filter(
        LeaveBalance.user_id == leave.user_id,
        LeaveBalance.leave_type == leave.leave_type,
        LeaveBalance.year == current_year,
        LeaveBalance.quarter == current_quarter
    ).first()

    if balance:
        balance.remaining_leaves -= leave.number_of_days
        balance.leaves_taken += leave.number_of_days

    # Log action
    log = LeaveLog(
        leave_id=leave_id,
        action="Approved by Admin",
        performed_by=current_user.id
    )

    db.add(log)
    db.commit()

    # Send email
    leave_owner = db.query(User).filter(
        User.id == leave.user_id
    ).first()

    if leave_owner:
        background_tasks.add_task(
            send_email,
            db,
            leave_owner.email,
            "Leave Approved",
            f"""
Your leave from {leave.start_date} to {leave.end_date}
has been approved by Admin.
"""
        )

    return result


# ================= REJECT LEAVE =================
@router.put("/leave/{leave_id}/reject")
async def reject_leave(
    leave_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role.upper() != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")

    leave = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    result = ApprovalService.reject_leave(
        db,
        leave_id,
        approver_role="ADMIN",
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
            f"""
Your leave from {leave.start_date} to {leave.end_date} 
has been rejected by Admin.
"""
        )

    return result
@router.get("/export-leaves")
def export_leaves(db: Session = Depends(get_db)):

    leaves = db.query(LeaveRequest).all()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Employee", "Leave Type", "From", "To", "Status"])

    for l in leaves:
        writer.writerow([l.user_id, l.leave_type, l.start_date, l.end_date, l.status])

    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=leaves.csv"}
    )
@router.get("/leave-reports")
def leave_reports(
    month: int = None,
    employee_id: int = None,
    leave_type: str = None,
    db: Session = Depends(get_db)
):

    query = db.query(LeaveRequest)

    if month:
        query = query.filter(func.extract('month', LeaveRequest.start_date) == month)

    if employee_id:
        query = query.filter(LeaveRequest.user_id == employee_id)

    if leave_type:
        query = query.filter(
        func.lower(LeaveRequest.leave_type) == leave_type.lower()
    )
    return query.all()
@router.get("/export-filtered")
def export_filtered(
    month: int | None = None,
    employee_id: int | None = None,
    leave_type: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    query = db.query(LeaveRequest)

    if month is not None:
        query = query.filter(
            func.extract("month", LeaveRequest.start_date) == month
        )

    if employee_id is not None:
        query = query.filter(
            LeaveRequest.user_id == employee_id
        )

    if leave_type is not None:
        query = query.filter(
            func.lower(LeaveRequest.leave_type) == leave_type.lower()
        )

    leaves = query.all()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Leave ID",
        "Employee ID",
        "Leave Type",
        "Start Date",
        "End Date",
        "Number of Days",
        "Status",
        "Reason"
    ])

    for leave in leaves:
        writer.writerow([
            leave.id,
            leave.user_id,
            leave.leave_type,
            leave.start_date,
            leave.end_date,
            leave.number_of_days,
            leave.status,
            leave.reason
        ])

    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=leave_report.csv"
        }
    )
@router.get("/leave-stats")
def leave_stats(db: Session = Depends(get_db)):

    results = db.query(
        func.extract("month", LeaveRequest.start_date).label("month"),
        func.count(LeaveRequest.id).label("total")
    ).group_by("month").order_by("month").all()

    months = []
    counts = []

    for r in results:
        months.append(int(r.month))
        counts.append(r.total)

    return {
        "months": months,
        "counts": counts
    }
from datetime import date, timedelta
from pydantic import BaseModel


class ResignationRequest(BaseModel):
    user_id: int
    notice_days: int
    reason: str | None = None


# ================= MARK USER RESIGNED =================

@router.post("/mark-resigned")
def mark_user_resigned(
    data: ResignationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role.upper() != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")

    user = db.query(User).filter(User.id == data.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    start_date = date.today()
    end_date = start_date + timedelta(days=data.notice_days)

    user.resignation_status = "notice_period"
    user.resignation_date = start_date
    user.resignation_approval_date = start_date
    user.last_working_day = end_date
    user.resignation_reason = data.reason

    db.commit()

    return {
        "message": "User placed in notice period",
        "notice_start": start_date,
        "last_working_day": end_date
    }
# ================= GET ALL EMPLOYEES =================
@router.get("/employees")
def get_all_employees(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role.upper() != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")

    users = db.query(User).filter(User.role != "ADMIN").all()

    result = []

    for user in users:
        result.append({
            "id": user.id,
            "name": user.name,
            "role": user.role
        })

    return result
# ================= REGISTER EMPLOYEE / MANAGER =================
@router.post("/register-employee")
def register_employee(
    request: RegisterSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role.upper() != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")

    existing_user = db.query(User).filter(
        User.email == request.email
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(request.password)

    new_user = User(
        name=request.name,
        email=request.email,
        password=hashed_password,
        role=request.role.upper(),
        gender=request.gender.upper(),
        manager_id=int(request.manager_id) if request.manager_id else None
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Employee registered successfully"}