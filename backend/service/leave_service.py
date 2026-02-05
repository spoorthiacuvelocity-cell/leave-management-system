from datetime import date
from sqlalchemy.orm import Session

from models.leave_request import LeaveRequest


class LeaveService:

    @staticmethod
    def calculate_leave_days(start_date: date, end_date: date) -> int:
        """
        Calculate total leave days (basic version).
        Later we will exclude weekends & holidays.
        """
        if end_date < start_date:
            raise ValueError("End date cannot be before start date")

        return (end_date - start_date).days + 1


    @staticmethod
    def apply_leave(
        db: Session,
        user_id: int,
        leave_type: str,
        start_date: date,
        end_date: date,
        reason: str | None = None
    ) -> LeaveRequest:
        """
        Create a new leave request
        """

        number_of_days = LeaveService.calculate_leave_days(start_date, end_date)

        leave = LeaveRequest(
            user_id=user_id,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            number_of_days=number_of_days,
            status="PENDING",
            reason=reason
        )

        db.add(leave)
        db.commit()
        db.refresh(leave)

        return leave
