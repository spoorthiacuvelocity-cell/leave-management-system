from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import pytz

from backend.app.models.leave_request import LeaveRequest
from backend.app.models.leave_balance import LeaveBalance
from backend.app.models.user import User   # 🔹 added


# 🔥 IST timezone
ist = pytz.timezone("Asia/Kolkata")


class ApprovalService:

    # ================= APPROVE =================
    @staticmethod
    def approve_leave(db: Session, leave_id: int, approver_role: str, approver_id: int, remarks: str = None):

        leave = db.query(LeaveRequest).filter(
            LeaveRequest.id == leave_id
        ).first()

        if not leave:
            raise HTTPException(status_code=404, detail="Leave request not found")

        if leave.status.lower() != "pending":
            raise HTTPException(status_code=400, detail="Leave already processed")

        # 🔹 Check if manager is approving only their employees
        if approver_role.upper() == "MANAGER":

            employee = db.query(User).filter(
                User.id == leave.user_id
            ).first()

            if not employee or employee.manager_id != approver_id:
                raise HTTPException(
                    status_code=403,
                    detail="You can only approve leaves of your assigned employees"
                )

        year = leave.start_date.year
        quarter = (leave.start_date.month - 1) // 3 + 1

        balance = db.query(LeaveBalance).filter(
            LeaveBalance.user_id == leave.user_id,
            LeaveBalance.leave_type == leave.leave_type,
            LeaveBalance.year == year,
            LeaveBalance.quarter == quarter
        ).first()

        if not balance:
            raise HTTPException(
                status_code=400,
                detail="Leave balance not initialized for this quarter"
            )

        leave_days = leave.number_of_days or 0

        if leave_days > balance.remaining_leaves:
            raise HTTPException(
                status_code=400,
                detail="Insufficient leave balance at approval stage"
            )

        # ✅ Deduct Leave
        balance.leaves_taken += leave_days
        balance.remaining_leaves -= leave_days

        # ✅ Update Leave Tracking
        leave.status = "Approved"
        leave.approved_by = approver_id
        leave.approved_by_role = approver_role
        leave.approved_on = datetime.now(ist)
        leave.remarks = remarks

        db.commit()
        db.refresh(leave)

        return {"message": "Leave approved successfully"}

    # ================= REJECT =================
    @staticmethod
    def reject_leave(db: Session, leave_id: int, approver_role: str, approver_id: int, remarks: str = None):

        leave = db.query(LeaveRequest).filter(
            LeaveRequest.id == leave_id
        ).first()

        if not leave:
            raise HTTPException(status_code=404, detail="Leave request not found")

        if leave.status.lower() != "pending":
            raise HTTPException(status_code=400, detail="Leave already processed")

        # 🔹 Manager hierarchy check
        if approver_role.upper() == "MANAGER":

            employee = db.query(User).filter(
                User.id == leave.user_id
            ).first()

            if not employee or employee.manager_id != approver_id:
                raise HTTPException(
                    status_code=403,
                    detail="You can only reject leaves of your assigned employees"
                )

        leave.status = "Rejected"
        leave.approved_by = approver_id
        leave.approved_by_role = approver_role
        leave.approved_on = datetime.now(ist)
        leave.remarks = remarks

        db.commit()
        db.refresh(leave)

        return {"message": "Leave rejected successfully"}

    # ================= CANCEL =================
    @staticmethod
    def cancel_leave(db: Session, leave_id: int, user_id: int):

        leave = db.query(LeaveRequest).filter(
            LeaveRequest.id == leave_id
        ).first()

        if not leave:
            raise HTTPException(status_code=404, detail="Leave request not found")

        if leave.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")

        if leave.status == "Rejected":
            raise HTTPException(status_code=400, detail="Cannot cancel rejected leave")

        if leave.status == "Cancelled":
            raise HTTPException(status_code=400, detail="Leave already cancelled")

        # ✅ Restore balance if already approved
        if leave.status == "Approved":

            year = leave.start_date.year
            quarter = (leave.start_date.month - 1) // 3 + 1

            balance = db.query(LeaveBalance).filter(
                LeaveBalance.user_id == leave.user_id,
                LeaveBalance.leave_type == leave.leave_type,
                LeaveBalance.year == year,
                LeaveBalance.quarter == quarter
            ).first()

            if balance:
                balance.leaves_taken -= leave.number_of_days
                balance.remaining_leaves += leave.number_of_days

        leave.status = "Cancelled"

        db.commit()

        return {"message": "Leave cancelled successfully"}