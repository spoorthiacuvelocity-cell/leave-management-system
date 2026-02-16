from sqlalchemy import Column, Integer, String, Date, ForeignKey
from backend.database.postgres import Base

class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)
    leave_type = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(String)
    status = Column(String, default="Pending")  
    user_id = Column(Integer, ForeignKey("users.id"))
    proof_document = Column(String, nullable=True)

