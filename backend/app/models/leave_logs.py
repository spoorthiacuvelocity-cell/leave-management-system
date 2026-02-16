from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from backend.database.postgres import Base

class LeaveLog(Base):
    __tablename__ = "leave_logs"

    id = Column(Integer, primary_key=True, index=True)
    leave_id = Column(Integer, ForeignKey("leave_requests.id"))
    action = Column(String)
    performed_by = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(TIMESTAMP, server_default=func.now())
