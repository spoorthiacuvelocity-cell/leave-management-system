from datetime import date, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException

from backend.app.models.leave_balance import LeaveBalance
from backend.app.models.leave_request import LeaveRequest
from backend.app.models.configuration import Configuration
from backend.app.models.holidays import Holiday


class LeaveService:

    # ================= WORKING DAY CALCULATION =================
    @staticmethod
    def calculate_leave_days(db: Session, start_date: date, end_date: date) -> int:
        """
        Calculate working leave days excluding weekends and holidays
        """

        if end_date < start_date:
            raise ValueError("End date cannot be before start date")

        total_days = 0
        current_date = start_date

        # Fetch holidays in date range
        holidays = db.query(Holiday).filter(
            Holiday.date >= start_date,
            Holiday.date <= end_date
        ).all()

        holiday_dates = {holiday.date for holiday in holidays}

        while current_date <= end_date:
            # Monday=0, Sunday=6
            if current_date.weekday() < 5:  # Skip Saturday(5) & Sunday(6)
                if current_date not in holiday_dates:
                    total_days += 1

            current_date += timedelta(days=1)

        return total_days


    # ================= GET CONFIG VALUE =================
    @staticmethod
    def get_config_value(db: Session, key: str):
        config = db.query(Configuration).filter(
            Configuration.config_parameter == key
        ).first()

        if not config:
            return None

        return config.config_value


    # ================= APPLY LEAVE =================
    @staticmethod
    async def apply_leave(
        db: Session,
        user_id: int,
        leave_type: str,
        start_date: date,
        end_date: date,
        reason: str | None = None,
        proof_document: str | None = None
    ) -> LeaveRequest:

        number_of_days = LeaveService.calculate_leave_days(
            db, start_date, end_date
        )

        if number_of_days <= 0:
            raise HTTPException(
                status_code=400,
                detail="Selected dates contain no working days"
            )

        # ================= CONFIG VALIDATIONS =================

        # 1️⃣ Maximum consecutive leave
        max_consecutive = LeaveService.get_config_value(
            db, "maximum_consecutive_leave"
        )

        if max_consecutive:
            max_consecutive = int(max_consecutive)
            if number_of_days > max_consecutive:
                raise HTTPException(
                    status_code=400,
                    detail=f"Cannot apply more than {max_consecutive} consecutive leave days"
                )

        # 2️⃣ Proof required
        proof_required = LeaveService.get_config_value(db, "proof_required")
        proof_after_days = LeaveService.get_config_value(
            db, "proof_required_after_days"
        )

        if proof_required and proof_required.lower() == "true":
            if proof_after_days:
                proof_after_days = int(proof_after_days)

                if number_of_days > proof_after_days and not proof_document:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Proof required for leave more than {proof_after_days} days"
                    )

        # ================= BALANCE CHECK =================

        leave_balance = db.query(LeaveBalance).filter(
            LeaveBalance.user_id == user_id,
            LeaveBalance.leave_type == leave_type
        ).first()

        if not leave_balance:
            raise HTTPException(
                status_code=400,
                detail="Leave balance not found for this leave type"
            )

        if leave_balance.remaining_leaves < number_of_days:
            raise HTTPException(
                status_code=400,
                detail="Insufficient leave balance"
            )

        # ================= CREATE LEAVE =================

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
