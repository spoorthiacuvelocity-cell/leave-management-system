from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from backend.database.postgres import Base


class LeaveBalance(Base):
    __tablename__ = "leave_balances"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    leave_type = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)
    leaves_taken = Column(Numeric(4, 1), default=0)
