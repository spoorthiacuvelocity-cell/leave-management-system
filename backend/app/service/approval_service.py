from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from backend.app.models.leave_request import LeaveRequest
from backend.app.models.leave_balance import LeaveBalance


class ApprovalService:

    @staticmethod
    def approve_leave(db: Session, leave_id: int, approver_role: str, approver_id: int):

        leave = db.query(LeaveRequest).filter(
            LeaveRequest.id == leave_id
        ).first()

        if not leave:
            raise HTTPException(status_code=404, detail="Leave request not found")

        if leave.status.lower() != "pending":
            raise HTTPException(status_code=400, detail="Leave already processed")

        year = leave.start_date.year
        quarter = (leave.start_date.month - 1) // 3 + 1

        balance = db.query(LeaveBalance).filter(
            LeaveBalance.user_id == leave.user_id,
            LeaveBalance.leave_type == leave.leave_type,
            LeaveBalance.year == year,
            LeaveBalance.quarter == quarter
        ).first()

        if not balance:
            balance = LeaveBalance(
                user_id=leave.user_id,
                leave_type=leave.leave_type,
                year=year,
                quarter=quarter,
                leaves_taken=0
            )
            db.add(balance)

        leave_days = leave.number_of_days or 0
        balance.leaves_taken += leave_days


        leave.status = "Approved"
        leave.approved_by_role = approver_role
        leave.approved_by_id = approver_id
        leave.approved_at = datetime.utcnow()

        db.commit()

        return {"message": "Leave approved successfully"}

    @staticmethod
    def reject_leave(db: Session, leave_id: int, approver_role: str, approver_id: int):

        leave = db.query(LeaveRequest).filter(
            LeaveRequest.id == leave_id
        ).first()

        if not leave:
            raise HTTPException(status_code=404, detail="Leave request not found")

        if leave.status.lower() != "pending":
            raise HTTPException(status_code=400, detail="Leave already processed")

        leave.status = "Rejected"
        leave.approved_by_role = approver_role
        leave.approved_by_id = approver_id
        leave.approved_at = datetime.utcnow()

        db.commit()

        return {"message": "Leave rejected successfully"}

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

        # If approved, restore quarterly balance
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

        leave.status = "Cancelled"

        db.commit()

        return {"message": "Leave cancelled successfully"}
