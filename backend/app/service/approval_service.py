from datetime import datetime
from sqlalchemy.orm import Session

from backend.app.models.leave_request import LeaveRequest


class ApprovalService:

    @staticmethod
    def approve_leave(db: Session, leave_id: int, approver_id: int):
        leave = db.query(LeaveRequest).filter(
            LeaveRequest.leave_id == leave_id
        ).first()

        if not leave:
            raise ValueError("Leave request not found")

        leave.status = "APPROVED"
        leave.approved_by = approver_id
        leave.approved_on = datetime.utcnow()

        db.commit()
        return leave


    @staticmethod
    def reject_leave(db: Session, leave_id: int, approver_id: int):
        leave = db.query(LeaveRequest).filter(
            LeaveRequest.leave_id == leave_id
        ).first()

        if not leave:
            raise ValueError("Leave request not found")

        leave.status = "REJECTED"
        leave.approved_by = approver_id
        leave.rejected_on = datetime.utcnow()

        db.commit()
        return leave


    @staticmethod
    def cancel_leave(db: Session, leave_id: int):
        leave = db.query(LeaveRequest).filter(
            LeaveRequest.leave_id == leave_id
        ).first()

        if not leave:
            raise ValueError("Leave request not found")

        leave.status = "CANCELLED"
        leave.cancelled_on = datetime.utcnow()

        db.commit()
        return leave
